#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analisador de metadados SAP.
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple

from abapify.sap.connection import SAPConnection
from abapify.sap.models import (
    SAPTable, SAPTableField, SAPObject, SAPRelationship, 
    SAPAnalysisResult, SAPConnectionConfig
)
from abapify.sap.exceptions import SAPMetadataError, SAPTableNotFoundError
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class MetadataAnalyzer:
    """Analisador de metadados e estruturas SAP."""
    
    def __init__(self, connection: SAPConnection):
        """
        Inicializa o analisador.
        
        Args:
            connection: Conexão SAP ativa.
        """
        self.connection = connection
        self._table_cache: Dict[str, SAPTable] = {}
        self._relationship_cache: Dict[str, List[SAPRelationship]] = {}
    
    def analyze_table(self, table_name: str, include_relationships: bool = True) -> SAPTable:
        """
        Analisa estrutura completa de uma tabela.
        
        Args:
            table_name: Nome da tabela.
            include_relationships: Se deve incluir análise de relacionamentos.
            
        Returns:
            Estrutura completa da tabela.
            
        Raises:
            SAPTableNotFoundError: Se tabela não for encontrada.
        """
        # Verifica cache
        if table_name in self._table_cache:
            logger.debug(f"Retornando tabela {table_name} do cache")
            return self._table_cache[table_name]
        
        try:
            logger.info(f"Analisando tabela: {table_name}")
            
            # Obtém estrutura via RFC
            structure_data = self.connection.get_table_structure(table_name)
            
            if not structure_data or 'DD02V_WA' not in structure_data:
                raise SAPTableNotFoundError(table_name)
            
            table_header = structure_data['DD02V_WA']
            table_fields_data = structure_data.get('DD03P_TAB', [])
            
            # Converte campos
            fields = []
            for field_data in table_fields_data:
                if field_data.get('FIELDNAME') and not field_data.get('FIELDNAME').startswith('.'):
                    field = SAPTableField(
                        name=field_data.get('FIELDNAME', ''),
                        data_type=field_data.get('DATATYPE', ''),
                        length=int(field_data.get('LENG', 0)),
                        decimals=int(field_data.get('DECIMALS', 0)),
                        description=field_data.get('DDTEXT', ''),
                        key_field=field_data.get('KEYFLAG') == 'X',
                        not_null=field_data.get('NOTNULL') == 'X',
                        domain=field_data.get('DOMNAME', ''),
                        data_element=field_data.get('ROLLNAME', '')
                    )
                    fields.append(field)
            
            # Cria objeto tabela
            table = SAPTable(
                name=table_name,
                description=table_header.get('DDTEXT', ''),
                table_type=table_header.get('TABCLASS', 'TRANSP'),
                delivery_class=table_header.get('CLIDEP', 'A'),
                fields=fields,
                created_on=self._parse_sap_date(table_header.get('CREATED_ON')),
                changed_on=self._parse_sap_date(table_header.get('CHANGED_ON'))
            )
            
            # Analisa relacionamentos se solicitado
            if include_relationships:
                relationships = self._analyze_table_relationships(table_name)
                table.foreign_keys = [rel.dict() for rel in relationships]
            
            # Adiciona ao cache
            self._table_cache[table_name] = table
            
            logger.info(f"Tabela {table_name} analisada: {len(fields)} campos")
            return table
            
        except SAPTableNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro ao analisar tabela {table_name}: {str(e)}")
            raise SAPMetadataError(f"Erro ao analisar tabela {table_name}: {str(e)}")
    
    def analyze_multiple_tables(self, table_names: List[str]) -> List[SAPTable]:
        """
        Analisa múltiplas tabelas.
        
        Args:
            table_names: Lista de nomes de tabelas.
            
        Returns:
            Lista de tabelas analisadas.
        """
        tables = []
        for table_name in table_names:
            try:
                table = self.analyze_table(table_name)
                tables.append(table)
            except SAPTableNotFoundError:
                logger.warning(f"Tabela {table_name} não encontrada, ignorando")
            except Exception as e:
                logger.error(f"Erro ao analisar tabela {table_name}: {str(e)}")
        
        return tables
    
    def _analyze_table_relationships(self, table_name: str) -> List[SAPRelationship]:
        """
        Analisa relacionamentos de uma tabela.
        
        Args:
            table_name: Nome da tabela.
            
        Returns:
            Lista de relacionamentos.
        """
        if table_name in self._relationship_cache:
            return self._relationship_cache[table_name]
        
        relationships = []
        
        try:
            with self.connection.rfc_connection() as rfc:
                # RFC para obter foreign keys
                result = rfc.call_function(
                    'DDIF_FORKEY_GET',
                    NAME=table_name,
                    STATE='A',
                    LANGU=self.connection.config.language
                )
                
                forkey_tab = result.get('DD08V_TAB', [])
                
                for fk in forkey_tab:
                    if fk.get('CHECKTABLE'):
                        relationship = SAPRelationship(
                            from_table=table_name,
                            to_table=fk.get('CHECKTABLE'),
                            from_fields=[fk.get('FIELDNAME', '')],
                            to_fields=[fk.get('CHECKFIELD', '')],
                            relationship_type='FOREIGN_KEY',
                            cardinality='N:1'
                        )
                        relationships.append(relationship)
                
        except Exception as e:
            logger.debug(f"Erro ao analisar relacionamentos de {table_name}: {str(e)}")
        
        self._relationship_cache[table_name] = relationships
        return relationships
    
    def find_related_tables(self, table_name: str, max_depth: int = 2) -> List[str]:
        """
        Encontra tabelas relacionadas.
        
        Args:
            table_name: Nome da tabela base.
            max_depth: Profundidade máxima de busca.
            
        Returns:
            Lista de nomes de tabelas relacionadas.
        """
        related_tables = set()
        tables_to_process = {table_name}
        processed_tables = set()
        
        for depth in range(max_depth):
            if not tables_to_process:
                break
            
            current_level_tables = tables_to_process.copy()
            tables_to_process.clear()
            
            for current_table in current_level_tables:
                if current_table in processed_tables:
                    continue
                
                processed_tables.add(current_table)
                
                # Obtém relacionamentos
                relationships = self._analyze_table_relationships(current_table)
                
                for rel in relationships:
                    related_table = rel.to_table
                    if related_table not in processed_tables:
                        related_tables.add(related_table)
                        if depth < max_depth - 1:
                            tables_to_process.add(related_table)
        
        return list(related_tables)
    
    def search_custom_tables(self, name_pattern: str = "Z*") -> List[str]:
        """
        Busca tabelas customizadas.
        
        Args:
            name_pattern: Padrão do nome.
            
        Returns:
            Lista de nomes de tabelas customizadas.
        """
        try:
            with self.connection.rfc_connection() as rfc:
                # Busca tabelas por padrão
                result = rfc.call_function(
                    'RFC_READ_TABLE',
                    QUERY_TABLE='DD02L',
                    FIELDS=[
                        {'FIELDNAME': 'TABNAME'},
                        {'FIELDNAME': 'DDTEXT'}
                    ],
                    OPTIONS=[
                        {'TEXT': f"TABNAME LIKE '{name_pattern}'"},
                        {'TEXT': "AND TABCLASS = 'TRANSP'"},
                        {'TEXT': "AND AS4LOCAL = 'A'"}
                    ],
                    ROWCOUNT=1000
                )
                
                tables = []
                if 'DATA' in result:
                    for row in result['DATA']:
                        table_name = row['WA'][:30].strip()  # TABNAME tem 30 chars
                        if table_name:
                            tables.append(table_name)
                
                logger.info(f"Encontradas {len(tables)} tabelas customizadas")
                return tables
                
        except Exception as e:
            logger.error(f"Erro ao buscar tabelas customizadas: {str(e)}")
            return []
    
    def analyze_custom_objects(self, name_pattern: str = "Z*") -> List[SAPObject]:
        """
        Analisa objetos customizados do SAP.
        
        Args:
            name_pattern: Padrão do nome.
            
        Returns:
            Lista de objetos customizados.
        """
        objects = []
        
        try:
            # Busca via conexão
            objects_data = self.connection.search_custom_objects(name_pattern)
            
            for obj_data in objects_data:
                obj = SAPObject(
                    name=obj_data.get('OBJECT_NAME', ''),
                    object_type=obj_data.get('OBJECT_TYPE', ''),
                    description=obj_data.get('OBJECT_TEXT', ''),
                    package=obj_data.get('DEVCLASS', ''),
                    author=obj_data.get('AUTHOR', ''),
                    created_on=self._parse_sap_date(obj_data.get('CREATED_ON')),
                    changed_on=self._parse_sap_date(obj_data.get('CHANGED_ON')),
                    status=obj_data.get('OBJECT_STATUS', '')
                )
                objects.append(obj)
            
            logger.info(f"Analisados {len(objects)} objetos customizados")
            
        except Exception as e:
            logger.error(f"Erro ao analisar objetos customizados: {str(e)}")
        
        return objects
    
    def detect_naming_patterns(self, objects: List[SAPObject]) -> Dict[str, Any]:
        """
        Detecta padrões de nomenclatura em objetos customizados.
        
        Args:
            objects: Lista de objetos para análise.
            
        Returns:
            Dict com padrões detectados.
        """
        patterns = {
            'prefixes': {},
            'suffixes': {},
            'naming_conventions': {},
            'package_patterns': {}
        }
        
        for obj in objects:
            # Analisa prefixos
            if len(obj.name) > 1:
                prefix = obj.name[:2]
                if prefix not in patterns['prefixes']:
                    patterns['prefixes'][prefix] = 0
                patterns['prefixes'][prefix] += 1
            
            # Analisa sufixos por tipo
            obj_type = obj.object_type
            if obj_type not in patterns['suffixes']:
                patterns['suffixes'][obj_type] = {}
            
            if '_' in obj.name:
                parts = obj.name.split('_')
                if len(parts) > 1:
                    suffix = parts[-1]
                    if suffix not in patterns['suffixes'][obj_type]:
                        patterns['suffixes'][obj_type][suffix] = 0
                    patterns['suffixes'][obj_type][suffix] += 1
            
            # Analisa padrões de pacote
            if obj.package:
                if obj.package not in patterns['package_patterns']:
                    patterns['package_patterns'][obj.package] = 0
                patterns['package_patterns'][obj.package] += 1
        
        return patterns
    
    def generate_full_analysis(self, table_names: List[str], 
                             include_custom_objects: bool = True) -> SAPAnalysisResult:
        """
        Gera análise completa de um conjunto de tabelas.
        
        Args:
            table_names: Lista de nomes de tabelas.
            include_custom_objects: Se deve incluir análise de objetos customizados.
            
        Returns:
            Resultado completo da análise.
        """
        logger.info(f"Iniciando análise completa de {len(table_names)} tabelas")
        
        # Analisa tabelas
        tables = self.analyze_multiple_tables(table_names)
        
        # Coleta todos os relacionamentos
        all_relationships = []
        for table in tables:
            relationships = self._analyze_table_relationships(table.name)
            all_relationships.extend(relationships)
        
        # Analisa objetos customizados se solicitado
        custom_objects = []
        patterns = {}
        
        if include_custom_objects:
            custom_objects = self.analyze_custom_objects()
            patterns = self.detect_naming_patterns(custom_objects)
        
        # Cria resultado
        result = SAPAnalysisResult(
            tables=tables,
            relationships=all_relationships,
            custom_objects=custom_objects,
            patterns=patterns,
            analysis_timestamp=datetime.now()
        )
        
        logger.info(f"Análise completa concluída: {len(tables)} tabelas, "
                   f"{len(all_relationships)} relacionamentos, "
                   f"{len(custom_objects)} objetos customizados")
        
        return result
    
    def _parse_sap_date(self, sap_date: Optional[str]) -> Optional[datetime]:
        """
        Converte data SAP para datetime.
        
        Args:
            sap_date: Data no formato SAP (YYYYMMDD).
            
        Returns:
            Objeto datetime ou None.
        """
        if not sap_date or len(sap_date) != 8:
            return None
        
        try:
            return datetime.strptime(sap_date, '%Y%m%d')
        except ValueError:
            return None
    
    def clear_cache(self) -> None:
        """Limpa cache de análise."""
        self._table_cache.clear()
        self._relationship_cache.clear()
        logger.info("Cache de análise limpo")