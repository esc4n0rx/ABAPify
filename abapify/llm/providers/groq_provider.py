#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementação do provedor Groq para geração de texto.
"""

import os
from typing import Dict, List, Optional

from groq import Groq

from abapify.utils.exceptions import LLMAPIError
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class GroqProvider:
    """Provedor Groq para geração de texto."""

    DEFAULT_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

    def __init__(self):
        """Inicializa o provedor Groq."""
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY não encontrada no ambiente")
        
        self.client = Groq(api_key=api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Gera texto usando o modelo Groq.

        Args:
            system_prompt: Prompt de sistema para o modelo.
            user_prompt: Prompt do usuário.
            model_name: Nome do modelo a ser utilizado.
            temperature: Temperatura para geração de texto.
            max_tokens: Número máximo de tokens a serem gerados.

        Returns:
            str: Texto gerado pelo modelo.

        Raises:
            LLMAPIError: Se ocorrer um erro na API do Groq.
        """
        try:
            model = model_name or self.DEFAULT_MODEL
            logger.info(f"Usando modelo Groq: {model}")
            
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_completion_tokens=max_tokens,
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro na API do Groq: {str(e)}")
            raise LLMAPIError(f"Erro na API do Groq: {str(e)}")