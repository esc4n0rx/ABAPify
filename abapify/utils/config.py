#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitário para configuração do sistema.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List

import dotenv

from abapify.utils.exceptions import ConfigError
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


def load_config() -> Dict[str, str]:
    """
    Carrega as configurações do sistema a partir de variáveis de ambiente ou arquivo .env.

    Returns:
        Dict[str, str]: Configurações carregadas.

    Raises:
        ConfigError: Se ocorrer um erro ao carregar as configurações.
    """
    try:
        # Tenta carregar o arquivo .env se existir
        env_path = Path(".") / ".env"
        if env_path.exists():
            logger.info(f"Carregando configurações do arquivo: {env_path}")
            dotenv.load_dotenv(env_path)
        
        # Verifica se pelo menos uma chave de API está disponível
        if not any([
            os.environ.get("ARCEE_TOKEN"),
            os.environ.get("GROQ_API_KEY"),
            os.environ.get("OPENAI_API_KEY")
        ]):
            logger.warning(
                "Nenhuma chave de API encontrada! Configure ARCEE_TOKEN, GROQ_API_KEY ou OPENAI_API_KEY."
            )
        
        # Retorna um dicionário com as configurações relevantes
        config = {
            # LLM APIs
            "ARCEE_TOKEN": os.environ.get("ARCEE_TOKEN", ""),
            "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
            "DEFAULT_PROVIDER": os.environ.get("DEFAULT_PROVIDER", "arcee"),
            "DEFAULT_MODEL_ARCEE": os.environ.get("DEFAULT_MODEL_ARCEE", "auto"),
            "DEFAULT_MODEL_GROQ": os.environ.get(
                "DEFAULT_MODEL_GROQ", "meta-llama/llama-4-maverick-17b-128e-instruct"
            ),
            "DEFAULT_MODEL_OPENAI": os.environ.get("DEFAULT_MODEL_OPENAI", "gpt-4o"),
            "OUTPUT_DIR": os.environ.get("OUTPUT_DIR", "./output"),
            "DEFAULT_TEMPERATURE": os.environ.get("DEFAULT_TEMPERATURE", "0.7"),
            "DEFAULT_MAX_TOKENS": os.environ.get("DEFAULT_MAX_TOKENS", "4096"),
            
            # SAP Configuration - Nova seção
            "SAP_ENCRYPTION_KEY": os.environ.get("SAP_ENCRYPTION_KEY", ""),
            "SAP_DEFAULT_ENVIRONMENT": os.environ.get("SAP_DEFAULT_ENVIRONMENT", "DEV"),
            
            # SAP DEV Environment
            "SAP_DEV_ASHOST": os.environ.get("SAP_DEV_ASHOST", ""),
            "SAP_DEV_SYSNR": os.environ.get("SAP_DEV_SYSNR", ""),
            "SAP_DEV_CLIENT": os.environ.get("SAP_DEV_CLIENT", ""),
            "SAP_DEV_USER": os.environ.get("SAP_DEV_USER", ""),
            "SAP_DEV_PASSWD": os.environ.get("SAP_DEV_PASSWD", ""),
            "SAP_DEV_PASSWD_ENCRYPTED": os.environ.get("SAP_DEV_PASSWD_ENCRYPTED", ""),
            "SAP_DEV_SAPROUTER": os.environ.get("SAP_DEV_SAPROUTER", ""),
            "SAP_DEV_MSHOST": os.environ.get("SAP_DEV_MSHOST", ""),
            "SAP_DEV_MSSERV": os.environ.get("SAP_DEV_MSSERV", ""),
            "SAP_DEV_GROUP": os.environ.get("SAP_DEV_GROUP", ""),
            "SAP_DEV_BASE_URL": os.environ.get("SAP_DEV_BASE_URL", ""),
            "SAP_DEV_USE_SSL": os.environ.get("SAP_DEV_USE_SSL", "true"),
            "SAP_DEV_VERIFY_SSL": os.environ.get("SAP_DEV_VERIFY_SSL", "true"),
            "SAP_DEV_LANGUAGE": os.environ.get("SAP_DEV_LANGUAGE", "EN"),
            "SAP_DEV_CONNECTION_TYPE": os.environ.get("SAP_DEV_CONNECTION_TYPE", "RFC"),
            "SAP_DEV_TIMEOUT": os.environ.get("SAP_DEV_TIMEOUT", "30"),
            
            # SAP QAS Environment
            "SAP_QAS_ASHOST": os.environ.get("SAP_QAS_ASHOST", ""),
            "SAP_QAS_SYSNR": os.environ.get("SAP_QAS_SYSNR", ""),
            "SAP_QAS_CLIENT": os.environ.get("SAP_QAS_CLIENT", ""),
            "SAP_QAS_USER": os.environ.get("SAP_QAS_USER", ""),
            "SAP_QAS_PASSWD": os.environ.get("SAP_QAS_PASSWD", ""),
            "SAP_QAS_PASSWD_ENCRYPTED": os.environ.get("SAP_QAS_PASSWD_ENCRYPTED", ""),
            "SAP_QAS_SAPROUTER": os.environ.get("SAP_QAS_SAPROUTER", ""),
            "SAP_QAS_MSHOST": os.environ.get("SAP_QAS_MSHOST", ""),
            "SAP_QAS_MSSERV": os.environ.get("SAP_QAS_MSSERV", ""),
            "SAP_QAS_GROUP": os.environ.get("SAP_QAS_GROUP", ""),
            "SAP_QAS_BASE_URL": os.environ.get("SAP_QAS_BASE_URL", ""),
            "SAP_QAS_USE_SSL": os.environ.get("SAP_QAS_USE_SSL", "true"),
            "SAP_QAS_VERIFY_SSL": os.environ.get("SAP_QAS_VERIFY_SSL", "true"),
            "SAP_QAS_LANGUAGE": os.environ.get("SAP_QAS_LANGUAGE", "EN"),
            "SAP_QAS_CONNECTION_TYPE": os.environ.get("SAP_QAS_CONNECTION_TYPE", "RFC"),
            "SAP_QAS_TIMEOUT": os.environ.get("SAP_QAS_TIMEOUT", "30"),
            
            # SAP PRD Environment
            "SAP_PRD_ASHOST": os.environ.get("SAP_PRD_ASHOST", ""),
            "SAP_PRD_SYSNR": os.environ.get("SAP_PRD_SYSNR", ""),
            "SAP_PRD_CLIENT": os.environ.get("SAP_PRD_CLIENT", ""),
            "SAP_PRD_USER": os.environ.get("SAP_PRD_USER", ""),
            "SAP_PRD_PASSWD": os.environ.get("SAP_PRD_PASSWD", ""),
            "SAP_PRD_PASSWD_ENCRYPTED": os.environ.get("SAP_PRD_PASSWD_ENCRYPTED", ""),
            "SAP_PRD_SAPROUTER": os.environ.get("SAP_PRD_SAPROUTER", ""),
            "SAP_PRD_MSHOST": os.environ.get("SAP_PRD_MSHOST", ""),
            "SAP_PRD_MSSERV": os.environ.get("SAP_PRD_MSSERV", ""),
            "SAP_PRD_GROUP": os.environ.get("SAP_PRD_GROUP", ""),
            "SAP_PRD_BASE_URL": os.environ.get("SAP_PRD_BASE_URL", ""),
            "SAP_PRD_USE_SSL": os.environ.get("SAP_PRD_USE_SSL", "true"),
            "SAP_PRD_VERIFY_SSL": os.environ.get("SAP_PRD_VERIFY_SSL", "true"),
            "SAP_PRD_LANGUAGE": os.environ.get("SAP_PRD_LANGUAGE", "EN"),
            "SAP_PRD_CONNECTION_TYPE": os.environ.get("SAP_PRD_CONNECTION_TYPE", "RFC"),
            "SAP_PRD_TIMEOUT": os.environ.get("SAP_PRD_TIMEOUT", "30"),
        }
        
        return config
    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {str(e)}")
        raise ConfigError(f"Erro ao carregar configurações: {str(e)}")


def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Obtém um valor de configuração específico.

    Args:
        key: Chave da configuração.
        default: Valor padrão se a configuração não for encontrada.

    Returns:
        Optional[str]: Valor da configuração ou o valor padrão.
    """
    return os.environ.get(key, default)


def save_config(config: Dict[str, str]) -> None:
    """
    Salva configurações no arquivo .env.

    Args:
        config: Dicionário com as configurações a serem salvas.

    Raises:
        ConfigError: Se ocorrer um erro ao salvar as configurações.
    """
    try:
        env_path = Path(".") / ".env"
        
        # Carrega configurações existentes
        existing_config = {}
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        existing_config[key] = value
        
        # Atualiza com novas configurações
        existing_config.update(config)
        
        # Salva no arquivo
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("# Configurações do ABAPify\n")
            f.write("# =========================\n\n")
            
            # LLM Configuration
            f.write("# LLM Configuration\n")
            llm_keys = ["ARCEE_TOKEN", "GROQ_API_KEY", "OPENAI_API_KEY", "DEFAULT_PROVIDER", 
                        "DEFAULT_MODEL_ARCEE", "DEFAULT_MODEL_GROQ", "DEFAULT_MODEL_OPENAI",
                        "OUTPUT_DIR", "DEFAULT_TEMPERATURE", "DEFAULT_MAX_TOKENS"]
            for key in llm_keys:
                if key in existing_config:
                    f.write(f"{key}={existing_config[key]}\n")
            f.write("\n")
            
            # SAP Configuration
            f.write("# SAP Configuration\n")
            sap_general_keys = ["SAP_ENCRYPTION_KEY", "SAP_DEFAULT_ENVIRONMENT"]
            for key in sap_general_keys:
                if key in existing_config:
                    f.write(f"{key}={existing_config[key]}\n")
            f.write("\n")
            
            # SAP Environments
            for env in ["DEV", "QAS", "PRD"]:
                f.write(f"# SAP {env} Environment\n")
                env_keys = [
                    f"SAP_{env}_ASHOST", f"SAP_{env}_SYSNR", f"SAP_{env}_CLIENT", 
                    f"SAP_{env}_USER", f"SAP_{env}_PASSWD", f"SAP_{env}_PASSWD_ENCRYPTED",
                    f"SAP_{env}_SAPROUTER", f"SAP_{env}_MSHOST", f"SAP_{env}_MSSERV", 
                    f"SAP_{env}_GROUP", f"SAP_{env}_BASE_URL", f"SAP_{env}_USE_SSL",
                    f"SAP_{env}_VERIFY_SSL", f"SAP_{env}_LANGUAGE", f"SAP_{env}_CONNECTION_TYPE",
                    f"SAP_{env}_TIMEOUT"
                ]
                for key in env_keys:
                    if key in existing_config:
                        f.write(f"{key}={existing_config[key]}\n")
                f.write("\n")
            
            # Outras configurações
            other_keys = set(existing_config.keys()) - set(llm_keys) - set(sap_general_keys)
            for env in ["DEV", "QAS", "PRD"]:
                env_keys = [k for k in existing_config.keys() if k.startswith(f"SAP_{env}_")]
                other_keys -= set(env_keys)
            
            if other_keys:
                f.write("# Other Configuration\n")
                for key in sorted(other_keys):
                    f.write(f"{key}={existing_config[key]}\n")
        
        logger.info(f"Configurações salvas em: {env_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar configurações: {str(e)}")
        raise ConfigError(f"Erro ao salvar configurações: {str(e)}")


def list_config() -> Dict[str, str]:
    """
    Lista todas as configurações atuais.

    Returns:
        Dict[str, str]: Configurações atuais (sem valores sensíveis completos).
    """
    config = load_config()
    
    # Mascara valores sensíveis
    safe_config = {}
    for key, value in config.items():
        if any(sensitive in key.upper() for sensitive in ["TOKEN", "KEY", "PASSWD", "PASSWORD"]):
            if value:
                safe_config[key] = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                safe_config[key] = "NÃO CONFIGURADO"
        else:
            safe_config[key] = value
    
    return safe_config


def get_sap_environments() -> List[str]:
    """
    Obtém lista de ambientes SAP configurados.
    
    Returns:
        Lista de ambientes configurados.
    """
    environments = []
    
    for env in ["DEV", "QAS", "PRD"]:
        # Verifica se tem configuração mínima para o ambiente
        ashost = get_config_value(f"SAP_{env}_ASHOST")
        if ashost:
            environments.append(env)
    
    return environments