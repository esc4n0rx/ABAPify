#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cliente principal de conectividade SAP.
"""

from typing import Dict, List, Any, Optional, Union
from contextlib import contextmanager

from abapify.sap.clients.rfc_client import RFCClient
from abapify.sap.clients.http_client import HTTPClient
from abapify.sap.auth import SAPAuthenticator
from abapify.sap.models import SAPConnectionConfig, SAPAnalysisResult
from abapify.sap.exceptions import SAPConnectionError, SAPAuthenticationError
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class SAPConnection:
    """Cliente principal de conectividade SAP."""
    
    def __init__(self, environment: str = "DEV", config: Optional[SAPConnectionConfig] = None):
        """
        Inicializa conexão SAP.
        
        Args:
            environment: Ambiente SAP (DEV, QAS, PRD).
            config: Configuração customizada (opcional).
        """
        self.environment = environment
        self.authenticator = SAPAuthenticator()
        
        # Usa config fornecida ou obtém do ambiente
        if config:
            self.config = config
        else:
            self.config = self.authenticator.get_connection_config(environment)
        
        # Valida configuração
        if not self.authenticator.validate_credentials(self.config):
            raise SAPConnectionError(f"Configuração inválida para ambiente {environment}")
        
        # Inicializa clientes
        self.rfc_client: Optional[RFCClient] = None
        self.http_client: Optional[HTTPClient] = None
        
        if self.config.connection_type == "RFC" or not self.config.connection_type:
            self.rfc_client = RFCClient(self.config)
        
        if self.config.connection_type == "HTTP" or self.config.base_url:
            self.http_client = HTTPClient(self.config)
            if self.config.user and self.config.passwd:
                self.http_client.authenticate(self.config.user, self.config.passwd)
    
    def test_connection(self) -> Dict[str, bool]:
        """
        Testa conectividade SAP.
        
        Returns:
            Dict com status de cada tipo de conexão.
        """
        results = {
            'rfc': False,
            'http': False
        }
        
        # Teste RFC
        if self.rfc_client:
            try:
                with self.rfc_client.connection_context():
                    results['rfc'] = self.rfc_client.is_connected()
                logger.info("Teste de conexão RFC: sucesso")
            except Exception as e:
                logger.error(f"Teste de conexão RFC falhou: {str(e)}")
                results['rfc'] = False
        
        # Teste HTTP
        if self.http_client:
            try:
                results['http'] = self.http_client.test_connection()
                if results['http']:
                    logger.info("Teste de conexão HTTP: sucesso")
                else:
                    logger.warning("Teste de conexão HTTP: falhou")
            except Exception as e:
                logger.error(f"Teste de conexão HTTP falhou: {str(e)}")
                results['http'] = False
        
        return results
    
    @contextmanager
    def rfc_connection(self):
        """
        Context manager para conexão RFC.
        
        Yields:
            RFCClient: Cliente RFC conectado.
        """
        if not self.rfc_client:
            raise SAPConnectionError("Cliente RFC não configurado")
        
        with self.rfc_client.connection_context() as connection:
            yield self.rfc_client
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Obtém informações do sistema SAP.
        
        Returns:
            Dict com informações do sistema.
        """
        if not self.rfc_client:
            raise SAPConnectionError("Cliente RFC necessário para obter informações do sistema")
        
        try:
            with self.rfc_connection() as rfc:
                # RFC para obter informações do sistema
                result = rfc.call_function('RFC_SYSTEM_INFO')
                
                system_info = {
                    'system_id': result.get('RFCSI_EXPORT', {}).get('RFCSYSID', ''),
                    'client': result.get('RFCSI_EXPORT', {}).get('RFCMANDT', ''),
                    'user': result.get('RFCSI_EXPORT', {}).get('RFCUSER', ''),
                    'language': result.get('RFCSI_EXPORT', {}).get('RFCLAN', ''),
                    'hostname': result.get('RFCSI_EXPORT', {}).get('RFCHOST', ''),
                    'system_release': result.get('RFCSI_EXPORT', {}).get('RFCSAPRL', ''),
                    'database_system': result.get('RFCSI_EXPORT', {}).get('RFCDBSYS', ''),
                }
                
                logger.info(f"Conectado ao sistema SAP: {system_info['system_id']}")
                return system_info
                
        except Exception as e:
            logger.error(f"Erro ao obter informações do sistema: {str(e)}")
            raise SAPConnectionError(f"Erro ao obter informações do sistema: {str(e)}")
    
    def get_table_data(self, table_name: str, fields: List[str] = None, 
                      where_clause: str = "", max_rows: int = 1000) -> List[Dict[str, Any]]:
        """
        Obtém dados de uma tabela SAP via RFC.
        
        Args:
            table_name: Nome da tabela.
            fields: Campos a serem retornados.
            where_clause: Cláusula WHERE.
            max_rows: Número máximo de linhas.
            
        Returns:
            Lista de registros da tabela.
        """
        if not self.rfc_client:
            raise SAPConnectionError("Cliente RFC necessário para ler dados de tabela")
        
        with self.rfc_connection() as rfc:
            return rfc.get_table_data(table_name, fields, where_clause, max_rows)
    
    def get_table_structure(self, table_name: str) -> Dict[str, Any]:
        """
        Obtém estrutura de uma tabela SAP via RFC.
        
        Args:
            table_name: Nome da tabela.
            
        Returns:
            Dict com estrutura da tabela.
        """
        if not self.rfc_client:
            raise SAPConnectionError("Cliente RFC necessário para obter estrutura de tabela")
        
        with self.rfc_connection() as rfc:
            return rfc.get_table_structure(table_name)
    
    def search_custom_objects(self, name_pattern: str = "Z*") -> List[Dict[str, Any]]:
        """
        Busca objetos customizados (Z/Y).
        
        Args:
            name_pattern: Padrão do nome (default: Z*).
            
        Returns:
            Lista de objetos encontrados.
        """
        if not self.rfc_client:
            raise SAPConnectionError("Cliente RFC necessário para buscar objetos")
        
        with self.rfc_connection() as rfc:
            # Busca diferentes tipos de objetos
            objects = []
            
            # Programas
            try:
                programs = rfc.search_objects(name_pattern, 'PROG')
                objects.extend(programs)
            except Exception as e:
                logger.debug(f"Erro ao buscar programas: {str(e)}")
            
            # Classes
            try:
                classes = rfc.search_objects(name_pattern, 'CLAS')
                objects.extend(classes)
            except Exception as e:
                logger.debug(f"Erro ao buscar classes: {str(e)}")
            
            # Function groups
            try:
                function_groups = rfc.search_objects(name_pattern, 'FUGR')
                objects.extend(function_groups)
            except Exception as e:
                logger.debug(f"Erro ao buscar function groups: {str(e)}")
            
            return objects
    
    def execute_odata_query(self, service_name: str, entity_set: str, 
                           filters: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Executa query OData via HTTP.
        
        Args:
            service_name: Nome do serviço OData.
            entity_set: Nome do entity set.
            filters: Filtros OData.
            
        Returns:
            Resultado da query.
        """
        if not self.http_client:
            raise SAPConnectionError("Cliente HTTP necessário para OData")
        
        # Monta endpoint OData
        endpoint = f"/sap/opu/odata/sap/{service_name}/{entity_set}"
        
        # Adiciona filtros se fornecidos
        params = {}
        if filters:
            filter_parts = []
            for field, value in filters.items():
                filter_parts.append(f"{field} eq '{value}'")
            if filter_parts:
                params['$filter'] = " and ".join(filter_parts)
        
        return self.http_client.get(endpoint, params=params)
    
    def close(self) -> None:
        """Encerra todas as conexões."""
        if self.rfc_client:
            self.rfc_client.disconnect()
        
        logger.info(f"Conexões SAP encerradas para ambiente {self.environment}")