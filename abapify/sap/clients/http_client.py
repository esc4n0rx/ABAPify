#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cliente HTTP para APIs SAP (OData, REST, etc.).
"""

import json
import base64
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from abapify.sap.exceptions import SAPHTTPError, SAPConnectionError, SAPAuthenticationError
from abapify.sap.models import SAPConnectionConfig
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class HTTPClient:
    """Cliente HTTP para APIs SAP."""
    
    def __init__(self, config: SAPConnectionConfig):
        """
        Inicializa o cliente HTTP.
        
        Args:
            config: Configuração de conexão SAP.
        """
        self.config = config
        self.session = requests.Session()
        
        # Configuração de retry
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Headers padrão
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'ABAPify-SAP-Client/1.0'
        })
        
        # Configuração SSL
        self.session.verify = config.verify_ssl
        
        # Timeout
        self.timeout = config.timeout
        
        # Base URL
        self.base_url = config.base_url or ""
        
    def authenticate(self, username: str, password: str) -> None:
        """
        Configura autenticação básica.
        
        Args:
            username: Nome de usuário.
            password: Senha.
        """
        self.session.auth = HTTPBasicAuth(username, password)
        logger.info(f"Autenticação HTTP configurada para usuário: {username}")
    
    def authenticate_oauth(self, token: str) -> None:
        """
        Configura autenticação OAuth.
        
        Args:
            token: Token OAuth.
        """
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
        logger.info("Autenticação OAuth configurada")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Faz requisição HTTP.
        
        Args:
            method: Método HTTP (GET, POST, etc.).
            endpoint: Endpoint da API.
            **kwargs: Parâmetros adicionais para requests.
            
        Returns:
            Response object.
            
        Raises:
            SAPHTTPError: Se falhar na requisição.
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            logger.debug(f"Fazendo requisição {method} para: {url}")
            
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            logger.debug(f"Resposta recebida: {response.status_code}")
            
            # Verifica erros HTTP
            if response.status_code == 401:
                raise SAPAuthenticationError("Falha na autenticação HTTP")
            elif response.status_code >= 400:
                raise SAPHTTPError(
                    f"Erro HTTP {response.status_code}: {response.text}",
                    status_code=response.status_code,
                    endpoint=endpoint
                )
            
            return response
            
        except requests.exceptions.Timeout:
            raise SAPHTTPError(f"Timeout na requisição para {endpoint}", endpoint=endpoint)
        except requests.exceptions.ConnectionError:
            raise SAPConnectionError(f"Erro de conexão para {endpoint}")
        except requests.exceptions.RequestException as e:
            raise SAPHTTPError(f"Erro na requisição: {str(e)}", endpoint=endpoint)
    
    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Faz requisição GET.
        
        Args:
            endpoint: Endpoint da API.
            params: Parâmetros de query.
            
        Returns:
            Resposta em formato JSON.
        """
        response = self._make_request('GET', endpoint, params=params)
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'content': response.text}
    
    def post(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Faz requisição POST.
        
        Args:
            endpoint: Endpoint da API.
            data: Dados a serem enviados.
            
        Returns:
            Resposta em formato JSON.
        """
        response = self._make_request('POST', endpoint, json=data)
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'content': response.text}
    
    def put(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Faz requisição PUT.
        
        Args:
            endpoint: Endpoint da API.
            data: Dados a serem enviados.
            
        Returns:
            Resposta em formato JSON.
        """
        response = self._make_request('PUT', endpoint, json=data)
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'content': response.text}
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Faz requisição DELETE.
        
        Args:
            endpoint: Endpoint da API.
            
        Returns:
            Resposta em formato JSON.
        """
        response = self._make_request('DELETE', endpoint)
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'content': response.text}
    
    def get_metadata(self, service_name: str) -> Dict[str, Any]:
        """
        Obtém metadados de um serviço OData.
        
        Args:
            service_name: Nome do serviço OData.
            
        Returns:
            Metadados do serviço.
        """
        endpoint = f"/sap/opu/odata/sap/{service_name}/$metadata"
        
        # Para metadados, aceita XML
        headers = {'Accept': 'application/xml'}
        response = self._make_request('GET', endpoint, headers=headers)
        
        # Converte XML para dict se necessário
        try:
            import xmltodict
            return xmltodict.parse(response.text)
        except ImportError:
            logger.warning("xmltodict não disponível, retornando XML como texto")
            return {'content': response.text}
    
    def test_connection(self) -> bool:
        """
        Testa conectividade HTTP.
        
        Returns:
            True se conectado, False caso contrário.
        """
        try:
            # Tenta acessar endpoint de ping ou similar
            self.get('/sap/bc/ping')
            return True
        except Exception as e:
            logger.debug(f"Teste de conexão HTTP falhou: {str(e)}")
            return False