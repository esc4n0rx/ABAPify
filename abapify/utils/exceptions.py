#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exceções personalizadas para o ABAPify.
"""


class AbapifyError(Exception):
    """Exceção base para o ABAPify."""

    pass


class ConfigError(AbapifyError):
    """Erro de configuração."""

    pass


class LLMAPIError(AbapifyError):
    """Erro na API do LLM."""

    pass


class LLMProviderNotFoundError(AbapifyError):
    """Provedor LLM não encontrado."""

    pass


class AbapGenerationError(AbapifyError):
    """Erro na geração de código ABAP."""

    pass


class OutputDirectoryError(AbapifyError):
    """Erro no diretório de saída."""

    pass