#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitário para configuração do sistema.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

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
            for key, value in existing_config.items():
                f.write(f"{key}={value}\n")
        
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
        if "TOKEN" in key or "KEY" in key:
            if value:
                safe_config[key] = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                safe_config[key] = "NÃO CONFIGURADO"
        else:
            safe_config[key] = value
    
    return safe_config