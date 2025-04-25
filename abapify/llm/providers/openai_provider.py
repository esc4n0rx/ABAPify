#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementação do provedor OpenAI para geração de texto.
"""

import os
from typing import Dict, List, Optional

from openai import OpenAI

from abapify.utils.exceptions import LLMAPIError
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIProvider:
    """Provedor OpenAI para geração de texto."""

    DEFAULT_MODEL = "gpt-4o"

    def __init__(self):
        """Inicializa o provedor OpenAI."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY não encontrada no ambiente")
        
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Gera texto usando o modelo OpenAI.

        Args:
            system_prompt: Prompt de sistema para o modelo.
            user_prompt: Prompt do usuário.
            model_name: Nome do modelo a ser utilizado.
            temperature: Temperatura para geração de texto.
            max_tokens: Número máximo de tokens a serem gerados.

        Returns:
            str: Texto gerado pelo modelo.

        Raises:
            LLMAPIError: Se ocorrer um erro na API do OpenAI.
        """
        try:
            model = model_name or self.DEFAULT_MODEL
            logger.info(f"Usando modelo OpenAI: {model}")
            
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro na API do OpenAI: {str(e)}")
            raise LLMAPIError(f"Erro na API do OpenAI: {str(e)}")