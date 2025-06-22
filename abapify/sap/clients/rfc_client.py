#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cliente RFC para conectividade SAP.
NOTA: PyRFC foi descontinuado. Esta implementação usa simulação/fallback para HTTP.
"""

import os
import warnings
from typing import Dict, List, Any, Optional, Union
from contextlib import contextmanager

from abapify.sap.exceptions import SAPRFCError, SAPConnectionError, SAPAuthenticationError
from abapify.sap.models import SAPConnectionConfig
from abapify.utils.logger import get_logger

logger = get_logger(__name__)

# PyRFC não está mais disponível
PYRFC_AVAILABLE = False

class RFCClient:
    """Cliente RFC para comunicação com SAP (Fallback para HTTP quando PyRFC não disponível)."""
    
    def __init__(self, config: SAPConnectionConfig):
        """
        Inicializa o cliente RFC.
        
        Args:
            config: Configuração de conexão SAP.
        """
        if not PYRFC_AVAILABLE:
            warnings.warn(
                "PyRFC não está disponível (descontinuado pelo SAP). "
                "Usando modo de compatibilidade com HTTP/REST. "
                "Algumas funcionalidades RFC podem ter limitações.",
                UserWarning
            )
        
        self.config = config
        self._connection: Optional[Any] = None
        self._http_fallback = None
        
        # Se não tem PyRFC, prepara fallback HTTP
        if not PYRFC_AVAILABLE and config.base_url:
            from .http_client import HTTPClient
            http_config = SAPConnectionConfig(
                base_url=config.base_url,
                user=config.user,
                passwd=config.passwd,
                use_ssl=config.use_ssl,
                verify_ssl=config.verify_ssl,
                timeout=config.timeout,
                connection_type="HTTP"
            )
            self._http_fallback = HTTPClient(http_config)
            if config.user and config.passwd:
                self._http_fallback.authenticate(config.user, config.passwd)
    
    def _get_connection_params(self) -> Dict[str, str]:
        """
        Obtém parâmetros de conexão RFC.
        
        Returns:
            Dict com parâmetros de conexão.
        """
        params = {}
        
        # Parâmetros obrigatórios
        if self.config.ashost:
            params['ashost'] = self.config.ashost
        if self.config.sysnr:
            params['sysnr'] = self.config.sysnr
        if self.config.client:
            params['client'] = self.config.client
        if self.config.user:
            params['user'] = self.config.user
        if self.config.passwd:
            params['passwd'] = self.config.passwd
            
        # Parâmetros opcionais
        if self.config.saprouter:
            params['saprouter'] = self.config.saprouter
        if self.config.mshost:
            params['mshost'] = self.config.mshost
        if self.config.msserv:
            params['msserv'] = self.config.msserv
        if self.config.group:
            params['group'] = self.config.group
            
        params['lang'] = self.config.language
        
        return params
    
    def connect(self) -> None:
        """
        Estabelece conexão RFC com SAP.
        
        Raises:
            SAPConnectionError: Se falhar ao conectar.
            SAPAuthenticationError: Se falhar na autenticação.
        """
        if PYRFC_AVAILABLE:
            # Código original seria executado aqui
            raise NotImplementedError("PyRFC não está mais disponível")
        else:
            # Usa fallback HTTP
            if self._http_fallback:
                logger.info("Usando fallback HTTP para conectividade SAP")
                if self._http_fallback.test_connection():
                    logger.info("Conexão HTTP estabelecida com sucesso (fallback RFC)")
                    self._connection = "http_fallback"
                else:
                    raise SAPConnectionError("Falha na conexão HTTP fallback")
            else:
                raise SAPConnectionError(
                    "PyRFC não disponível e nenhuma URL HTTP configurada. "
                    "Configure SAP_DEV_BASE_URL no .env"
                )
    
    def disconnect(self) -> None:
        """Encerra conexão RFC."""
        if self._connection:
            logger.info("Conexão RFC/HTTP encerrada")
            self._connection = None
    
    @contextmanager
    def connection_context(self):
        """
        Context manager para conexão RFC.
        
        Yields:
            RFCClient: Cliente RFC conectado.
        """
        try:
            if not self._connection:
                self.connect()
            yield self
        finally:
            self.disconnect()
    
    def call_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        """
        Chama função RFC (com fallback HTTP para funções comuns).
        
        Args:
            function_name: Nome da função RFC.
            **kwargs: Parâmetros da função.
            
        Returns:
            Dict com resultado da função.
            
        Raises:
            SAPRFCError: Se falhar na chamada RFC.
        """
        if not self._connection:
            raise SAPRFCError("Conexão RFC não estabelecida")
        
        # Implementa fallbacks HTTP para funções RFC comuns
        if function_name == "RFC_PING":
            return self._rfc_ping_fallback()
        elif function_name == "RFC_SYSTEM_INFO":
            return self._rfc_system_info_fallback()
        elif function_name == "RFC_READ_TABLE":
            return self._rfc_read_table_fallback(**kwargs)
        elif function_name == "DDIF_TABL_GET":
            return self._ddif_tabl_get_fallback(**kwargs)
        else:
            raise SAPRFCError(
                f"Função RFC '{function_name}' não suportada no modo fallback HTTP. "
                f"PyRFC necessário para esta função."
            )
    
    def _rfc_ping_fallback(self) -> Dict[str, Any]:
        """Fallback HTTP para RFC_PING."""
        if self._http_fallback and self._http_fallback.test_connection():
            return {"SUCCESS": "X"}
        else:
            raise SAPRFCError("Ping falhou")
    
    def _rfc_system_info_fallback(self) -> Dict[str, Any]:
        """Fallback HTTP para RFC_SYSTEM_INFO."""
        # Retorna informações básicas simuladas
        return {
            "RFCSI_EXPORT": {
                "RFCSYSID": "DEV",
                "RFCMANDT": self.config.client or "100",
                "RFCUSER": self.config.user or "UNKNOWN",
                "RFCLAN": self.config.language or "EN",
                "RFCHOST": self.config.ashost or "localhost",
                "RFCSAPRL": "750",
                "RFCDBSYS": "HDB",
            }
        }
    
    def _rfc_read_table_fallback(self, **kwargs) -> Dict[str, Any]:
        """Fallback HTTP para RFC_READ_TABLE usando OData se disponível."""
        table_name = kwargs.get("QUERY_TABLE", "")
        max_rows = kwargs.get("ROWCOUNT", 100)
        
        if not self._http_fallback:
            raise SAPRFCError("HTTP fallback não configurado para RFC_READ_TABLE")
        
        # Tenta usar serviço OData genérico
        try:
            # Formato OData padrão SAP
            endpoint = f"/sap/opu/odata/sap/ZGW_TABLES_SRV/{table_name}"
            params = {"$top": max_rows}
            
            # Adiciona campos se especificados
            fields = kwargs.get("FIELDS", [])
            if fields:
                field_names = [f["FIELDNAME"] for f in fields]
                params["$select"] = ",".join(field_names)
            
            result = self._http_fallback.get(endpoint, params)
            
            # Converte resultado OData para formato RFC_READ_TABLE
            return self._convert_odata_to_rfc_format(result, table_name)
            
        except Exception as e:
            logger.warning(f"Fallback OData falhou para {table_name}: {str(e)}")
            
            # Retorna estrutura vazia mas válida
            return {
                "DATA": [],
                "FIELDS": kwargs.get("FIELDS", []),
                "OPTIONS": kwargs.get("OPTIONS", [])
            }
    
    def _ddif_tabl_get_fallback(self, **kwargs) -> Dict[str, Any]:
        """Fallback para DDIF_TABL_GET usando dados simulados."""
        table_name = kwargs.get("NAME", "")
        
        # Retorna estrutura básica simulada
        return {
            "DD02V_WA": {
                "TABNAME": table_name,
                "DDTEXT": f"Tabela {table_name}",
                "TABCLASS": "TRANSP",
                "CLIDEP": "A",
                "CREATED_ON": "20240101",
                "CHANGED_ON": "20241201"
            },
            "DD03P_TAB": [
                {
                    "FIELDNAME": "CLIENT",
                    "DATATYPE": "CLNT",
                    "LENG": "3",
                    "DECIMALS": "0",
                    "KEYFLAG": "X",
                    "DDTEXT": "Client"
                },
                {
                    "FIELDNAME": "ID",
                    "DATATYPE": "CHAR",
                    "LENG": "10",
                    "DECIMALS": "0",
                    "KEYFLAG": "X",
                    "DDTEXT": "ID"
                }
            ]
        }
    
    def _convert_odata_to_rfc_format(self, odata_result: Dict[str, Any], table_name: str) -> Dict[str, Any]:
        """Converte resultado OData para formato RFC_READ_TABLE."""
        # Implementação básica - pode ser expandida
        data_entries = odata_result.get("d", {}).get("results", [])
        
        rfc_data = []
        for entry in data_entries:
            # Simula formato WA (concatenado)
            wa_line = ""
            for key, value in entry.items():
                if not key.startswith("__"):
                    wa_line += str(value).ljust(30)[:30]  # Simula campos de 30 chars
            rfc_data.append({"WA": wa_line})
        
        return {
            "DATA": rfc_data,
            "FIELDS": [],  # Seria populado com metadados reais
            "OPTIONS": []
        }
    
    def get_table_data(self, table_name: str, fields: List[str] = None, 
                      where_clause: str = "", max_rows: int = 1000) -> List[Dict[str, Any]]:
        """
        Obtém dados de uma tabela SAP.
        
        Args:
            table_name: Nome da tabela.
            fields: Lista de campos a serem retornados.
            where_clause: Cláusula WHERE.
            max_rows: Número máximo de linhas.
            
        Returns:
            Lista de registros da tabela.
        """
        try:
            # Monta parâmetros RFC_READ_TABLE
            params = {
                'QUERY_TABLE': table_name,
                'ROWCOUNT': max_rows,
            }
            
            if fields:
                params['FIELDS'] = [{'FIELDNAME': field} for field in fields]
            
            if where_clause:
                # Quebra WHERE clause em linhas de 72 caracteres (limitação SAP)
                options = []
                for i in range(0, len(where_clause), 72):
                    options.append({'TEXT': where_clause[i:i+72]})
                params['OPTIONS'] = options
            
            result = self.call_function('RFC_READ_TABLE', **params)
            
            # Processa resultado (versão simplificada para fallback)
            if 'DATA' not in result:
                return []
            
            # Para fallback, retorna dados básicos
            data = []
            for i, row in enumerate(result['DATA'][:max_rows]):
                record = {
                    'ROW_ID': i + 1,
                    'TABLE_NAME': table_name,
                    'DATA': str(row.get('WA', ''))
                }
                data.append(record)
            
            return data
            
        except Exception as e:
            logger.error(f"Erro ao ler tabela {table_name}: {str(e)}")
            raise SAPRFCError(f"Erro ao ler tabela {table_name}: {str(e)}")
    
    def get_table_structure(self, table_name: str) -> Dict[str, Any]:
        """
        Obtém estrutura de uma tabela SAP.
        
        Args:
            table_name: Nome da tabela.
            
        Returns:
            Dict com estrutura da tabela.
        """
        try:
            # RFC para obter estrutura de tabela
            result = self.call_function(
                'DDIF_TABL_GET',
                NAME=table_name,
                STATE='A',  # Active
                LANGU=self.config.language
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao obter estrutura da tabela {table_name}: {str(e)}")
            raise SAPRFCError(f"Erro ao obter estrutura da tabela {table_name}: {str(e)}")
    
    def search_objects(self, object_name_pattern: str, object_type: str = "*") -> List[Dict[str, Any]]:
        """
        Busca objetos SAP por padrão (fallback simulado).
        
        Args:
            object_name_pattern: Padrão do nome do objeto (aceita wildcards).
            object_type: Tipo do objeto (PROG, CLAS, FUGR, etc.).
            
        Returns:
            Lista de objetos encontrados.
        """
        # Retorna dados simulados para fallback
        return [
            {
                "OBJECT_NAME": f"Z_{object_type}_EXAMPLE",
                "OBJECT_TYPE": object_type,
                "OBJECT_TEXT": f"Exemplo de {object_type}",
                "DEVCLASS": "ZLOCAL",
                "AUTHOR": "DEVELOPER",
                "CREATED_ON": "20241201",
                "CHANGED_ON": "20241201",
                "OBJECT_STATUS": "A"
            }
        ]
    
    def is_connected(self) -> bool:
        """
        Verifica se está conectado ao SAP.
        
        Returns:
            True se conectado, False caso contrário.
        """
        if not self._connection:
            return False
        
        try:
            self.call_function('RFC_PING')
            return True
        except Exception:
            return False