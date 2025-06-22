#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de autenticação para SAP.
"""

import os
import base64
from typing import Dict, Optional, Tuple
from cryptography.fernet import Fernet

from abapify.sap.exceptions import SAPAuthenticationError
from abapify.sap.models import SAPConnectionConfig
from abapify.utils.config import get_config_value
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class SAPAuthenticator:
    """Gerenciador de autenticação SAP."""
    
    def __init__(self):
        """Inicializa o autenticador."""
        self._encryption_key = self._get_or_create_encryption_key()
        self._cipher_suite = Fernet(self._encryption_key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """
        Obtém ou cria chave de criptografia.
        
        Returns:
            Chave de criptografia.
        """
        key_env = get_config_value("SAP_ENCRYPTION_KEY")
        
        if key_env:
            try:
                return base64.urlsafe_b64decode(key_env.encode())
            except Exception:
                logger.warning("Chave de criptografia inválida, gerando nova")
        
        # Gera nova chave
        key = Fernet.generate_key()
        key_b64 = base64.urlsafe_b64encode(key).decode()
        
        logger.info("Nova chave de criptografia gerada. Adicione ao .env:")
        logger.info(f"SAP_ENCRYPTION_KEY={key_b64}")
        
        return key
   
    def encrypt_password(self, password: str) -> str:
        """
        Criptografa senha.
        
        Args:
            password: Senha em texto claro.
            
        Returns:
            Senha criptografada em base64.
        """
        try:
            encrypted = self._cipher_suite.encrypt(password.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Erro ao criptografar senha: {str(e)}")
            raise SAPAuthenticationError("Erro ao criptografar senha")
    
    def decrypt_password(self, encrypted_password: str) -> str:
        """
        Descriptografa senha.
        
        Args:
            encrypted_password: Senha criptografada em base64.
            
        Returns:
            Senha em texto claro.
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_password.encode())
            decrypted = self._cipher_suite.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Erro ao descriptografar senha: {str(e)}")
            raise SAPAuthenticationError("Erro ao descriptografar senha")
    
    def validate_credentials(self, config: SAPConnectionConfig) -> bool:
        """
        Valida credenciais SAP.
        
        Args:
            config: Configuração de conexão.
            
        Returns:
            True se credenciais são válidas.
        """
        required_fields = []
        
        if config.connection_type == "RFC":
            required_fields = ['ashost', 'sysnr', 'client', 'user', 'passwd']
        elif config.connection_type == "HTTP":
            required_fields = ['base_url', 'user', 'passwd']
        
        for field in required_fields:
            if not getattr(config, field, None):
                logger.error(f"Campo obrigatório ausente: {field}")
                return False
        
        return True
    
    def get_connection_config(self, environment: str = "DEV") -> SAPConnectionConfig:
        """
        Obtém configuração de conexão para um ambiente.
        
        Args:
            environment: Ambiente (DEV, QAS, PRD).
            
        Returns:
            Configuração de conexão.
        """
        env_prefix = f"SAP_{environment}_"
        
        # Obtém configurações do ambiente
        config_data = {}
        
        # RFC parameters
        config_data['ashost'] = get_config_value(f"{env_prefix}ASHOST")
        config_data['sysnr'] = get_config_value(f"{env_prefix}SYSNR")
        config_data['client'] = get_config_value(f"{env_prefix}CLIENT")
        config_data['user'] = get_config_value(f"{env_prefix}USER")
        config_data['saprouter'] = get_config_value(f"{env_prefix}SAPROUTER")
        config_data['mshost'] = get_config_value(f"{env_prefix}MSHOST")
        config_data['msserv'] = get_config_value(f"{env_prefix}MSSERV")
        config_data['group'] = get_config_value(f"{env_prefix}GROUP")
        
        # HTTP parameters
        config_data['base_url'] = get_config_value(f"{env_prefix}BASE_URL")
        config_data['use_ssl'] = get_config_value(f"{env_prefix}USE_SSL", "true").lower() == "true"
        config_data['verify_ssl'] = get_config_value(f"{env_prefix}VERIFY_SSL", "true").lower() == "true"
        
        # Common parameters
        config_data['language'] = get_config_value(f"{env_prefix}LANGUAGE", "EN")
        config_data['connection_type'] = get_config_value(f"{env_prefix}CONNECTION_TYPE", "RFC")
        config_data['timeout'] = int(get_config_value(f"{env_prefix}TIMEOUT", "30"))
        
        # Senha criptografada
        encrypted_password = get_config_value(f"{env_prefix}PASSWD_ENCRYPTED")
        if encrypted_password:
            try:
                config_data['passwd'] = self.decrypt_password(encrypted_password)
            except Exception:
                logger.error("Erro ao descriptografar senha SAP")
                config_data['passwd'] = None
        else:
            config_data['passwd'] = get_config_value(f"{env_prefix}PASSWD")
        
        # Remove valores None
        config_data = {k: v for k, v in config_data.items() if v is not None}
        
        return SAPConnectionConfig(**config_data)
    
    def save_encrypted_password(self, environment: str, password: str) -> str:
        """
        Salva senha criptografada para um ambiente.
        
        Args:
            environment: Ambiente (DEV, QAS, PRD).
            password: Senha em texto claro.
            
        Returns:
            Senha criptografada para salvar na configuração.
        """
        return self.encrypt_password(password)