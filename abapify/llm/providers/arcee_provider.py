#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementação do provedor Arcee Conductor para geração de texto.
"""

import os
import requests
from typing import Dict, List, Optional

from abapify.utils.exceptions import LLMAPIError
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class ArceeProvider:
    """Provedor Arcee Conductor para geração de texto."""

    DEFAULT_MODEL = "auto"
    BASE_URL = "https://conductor.arcee.ai/v1"

    def __init__(self):
        """Inicializa o provedor Arcee."""
        api_key = os.environ.get("ARCEE_TOKEN")
        if not api_key:
            logger.warning("ARCEE_TOKEN não encontrada no ambiente")
        
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Gera texto usando o modelo Arcee Conductor.

        Args:
            system_prompt: Prompt de sistema para o modelo.
            user_prompt: Prompt do usuário.
            model_name: Nome do modelo a ser utilizado.
            temperature: Temperatura para geração de texto.
            max_tokens: Número máximo de tokens a serem gerados.

        Returns:
            str: Texto gerado pelo modelo.

        Raises:
            LLMAPIError: Se ocorrer um erro na API do Arcee.
        """
        try:
            model = model_name or self.DEFAULT_MODEL
            logger.info(f"Usando modelo Arcee: {model}")
            
            # Monta os dados da requisição
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            # Faz a requisição para a API
            response = self.session.post(
                f"{self.BASE_URL}/chat/completions",
                json=data,
                timeout=120
            )
            
            # Verifica se a requisição foi bem-sucedida
            response.raise_for_status()
            
            # Extrai a resposta
            result = response.json()
            
            if "choices" not in result or not result["choices"]:
                raise LLMAPIError("Resposta inválida da API do Arcee")
            
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede na API do Arcee: {str(e)}")
            raise LLMAPIError(f"Erro de rede na API do Arcee: {str(e)}")
        except Exception as e:
            logger.error(f"Erro na API do Arcee: {str(e)}")
            raise LLMAPIError(f"Erro na API do Arcee: {str(e)}")