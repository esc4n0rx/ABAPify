#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe principal para geração de código ABAP.
"""

from typing import Dict, List, Optional, Union

from abapify.llm.client import LLMClient
from abapify.prompts.system_prompts import SYSTEM_PROMPT
from abapify.prompts.user_prompts import (
    ALV_PROMPT_TEMPLATE,
    CLASS_PROMPT_TEMPLATE,
    FUNCTION_MODULE_PROMPT_TEMPLATE,
    REPORT_PROMPT_TEMPLATE,
    STRUCTURE_PROMPT_TEMPLATE,
    TEST_PROMPT_TEMPLATE,
)
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class AbapGenerator:
    """Gerador de código ABAP usando modelos de linguagem."""

    def __init__(self, model_name: Optional[str] = None):
        """
        Inicializa o gerador de código ABAP.

        Args:
            model_name: Nome do modelo a ser utilizado (opcional).
        """
        self.llm_client = LLMClient()
        self.model_name = model_name

    def _generate_code(self, prompt: str) -> str:
        """
        Método principal para gerar código ABAP.

        Args:
            prompt: Prompt para o modelo de linguagem.

        Returns:
            str: Código ABAP gerado.
        """
        try:
            response = self.llm_client.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
                model_name=self.model_name,
            )
            return response
        except Exception as e:
            logger.error(f"Erro ao gerar código: {str(e)}")
            raise

    def generate_alv(self, description: str, tables: List[str]) -> str:
        """
        Gera um relatório ALV.

        Args:
            description: Descrição do relatório ALV.
            tables: Lista de tabelas a serem utilizadas.

        Returns:
            str: Código ABAP do relatório ALV.
        """
        prompt = ALV_PROMPT_TEMPLATE.format(
            description=description, tables=", ".join(tables)
        )
        logger.info(f"Gerando relatório ALV: {description}")
        return self._generate_code(prompt)

    def generate_report(self, description: str, tables: List[str]) -> str:
        """
        Gera um relatório ABAP.

        Args:
            description: Descrição do relatório.
            tables: Lista de tabelas a serem utilizadas.

        Returns:
            str: Código ABAP do relatório.
        """
        prompt = REPORT_PROMPT_TEMPLATE.format(
            description=description, tables=", ".join(tables)
        )
        logger.info(f"Gerando relatório: {description}")
        return self._generate_code(prompt)

    def generate_class(self, description: str, methods: List[str]) -> str:
        """
        Gera uma classe ABAP.

        Args:
            description: Descrição da classe.
            methods: Lista de métodos a serem incluídos.

        Returns:
            str: Código ABAP da classe.
        """
        prompt = CLASS_PROMPT_TEMPLATE.format(
            description=description, methods=", ".join(methods)
        )
        logger.info(f"Gerando classe: {description}")
        return self._generate_code(prompt)

    def generate_function_module(self, description: str, params: List[str]) -> str:
        """
        Gera um módulo de função ABAP.

        Args:
            description: Descrição do módulo de função.
            params: Lista de parâmetros a serem incluídos.

        Returns:
            str: Código ABAP do módulo de função.
        """
        prompt = FUNCTION_MODULE_PROMPT_TEMPLATE.format(
            description=description, params=", ".join(params)
        )
        logger.info(f"Gerando módulo de função: {description}")
        return self._generate_code(prompt)

    def generate_structure(self, description: str, fields: List[str]) -> str:
        """
        Gera uma estrutura ABAP.

        Args:
            description: Descrição da estrutura.
            fields: Lista de campos a serem incluídos.

        Returns:
            str: Código ABAP da estrutura.
        """
        prompt = STRUCTURE_PROMPT_TEMPLATE.format(
            description=description, fields=", ".join(fields)
        )
        logger.info(f"Gerando estrutura: {description}")
        return self._generate_code(prompt)

    def generate_test(self, target: str) -> str:
        """
        Gera um teste unitário ABAP.

        Args:
            target: Nome da classe ou módulo a ser testado.

        Returns:
            str: Código ABAP do teste unitário.
        """
        prompt = TEST_PROMPT_TEMPLATE.format(target=target)
        logger.info(f"Gerando teste unitário: {target}")
        return self._generate_code(prompt)