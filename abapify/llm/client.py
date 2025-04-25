#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cliente para comunicação com LLMs como Groq e OpenAI.
"""

import os
from typing import Dict, List, Optional, Union

from abapify.llm.providers.groq_provider import GroqProvider
from abapify.llm.providers.openai_provider import OpenAIProvider
from abapify.utils.exceptions import LLMProviderNotFoundError
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class LLMClient:
    """Cliente para comunicação com modelos de linguagem."""

    def __init__(self):
        """Inicializa o cliente LLM."""
        self._providers = {
            "groq": GroqProvider(),
            "openai": OpenAIProvider(),
        }
        self._default_provider = self._get_default_provider()

    def _get_default_provider(self) -> str:
        """
        Determina o provedor padrão com base nas variáveis de ambiente disponíveis.

        Returns:
            str: Nome do provedor padrão.
        """
        if os.environ.get("GROQ_API_KEY"):
            return "groq"
        elif os.environ.get("OPENAI_API_KEY"):
            return "openai"
        else:
            logger.warning(
                "Nenhuma chave de API encontrada. Configure GROQ_API_KEY ou OPENAI_API_KEY."
            )
            return "groq"  # Padrão para Groq

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Gera texto usando o modelo de linguagem.

        Args:
            system_prompt: Prompt de sistema para o modelo.
            user_prompt: Prompt do usuário.
            provider: Nome do provedor a ser utilizado.
            model_name: Nome do modelo a ser utilizado.
            temperature: Temperatura para geração de texto.
            max_tokens: Número máximo de tokens a serem gerados.

        Returns:
            str: Texto gerado pelo modelo.

        Raises:
            LLMProviderNotFoundError: Se o provedor especificado não for encontrado.
        """
        provider_name = provider or self._default_provider
        
        if provider_name not in self._providers:
            raise LLMProviderNotFoundError(f"Provedor não encontrado: {provider_name}")
        
        provider_instance = self._providers[provider_name]
        
        logger.info(f"Usando provedor: {provider_name}")
        
        return provider_instance.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )