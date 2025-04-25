#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitário para configuração do sistema.
"""

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
        if not os.environ.get("GROQ_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
            logger.warning(
                "Nenhuma chave de API encontrada! Configure GROQ_API_KEY ou OPENAI_API_KEY."
            )
        
        # Retorna um dicionário com as configurações relevantes
        config = {
            "GROQ_API_KEY": os.environ.get("GROQ_API_KEY", ""),
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
            "DEFAULT_MODEL_GROQ": os.environ.get(
                "DEFAULT_MODEL_GROQ", "meta-llama/llama-4-maverick-17b-128e-instruct"
            ),
            "DEFAULT_MODEL_OPENAI": os.environ.get("DEFAULT_MODEL_OPENAI", "gpt-4o"),
            "OUTPUT_DIR": os.environ.get("OUTPUT_DIR", "./output"),
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