#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração de logging para o ABAPify.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logger() -> logging.Logger:
    """
    Configura o logger global para o ABAPify.

    Returns:
        logging.Logger: Logger configurado.
    """
    # Cria o diretório de logs se não existir
    logs_dir = Path("./logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configura o logger raiz
    logger = logging.getLogger("abapify")
    logger.setLevel(logging.INFO)
    
    # Define o formato de log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Handler para arquivo
    file_handler = RotatingFileHandler(
        logs_dir / "abapify.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Adiciona os handlers ao logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Obtém um logger específico.

    Args:
        name: Nome do logger (opcional).

    Returns:
        logging.Logger: Logger específico.
    """
    logger_name = f"abapify.{name}" if name else "abapify"
    return logging.getLogger(logger_name)