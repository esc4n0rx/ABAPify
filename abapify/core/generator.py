#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe principal para geração de código ABAP.
"""

from typing import Dict, List, Optional, Union

from abapify.llm.client import LLMClient
from abapify.prompts.enhanced_system_prompts import ENHANCED_SYSTEM_PROMPT, SIMPLE_SYSTEM_PROMPT
from abapify.prompts.user_prompts import (
    ALV_PROMPT_TEMPLATE,
    CLASS_PROMPT_TEMPLATE,
    FUNCTION_MODULE_PROMPT_TEMPLATE,
    REPORT_PROMPT_TEMPLATE,
    STRUCTURE_PROMPT_TEMPLATE,
    TEST_PROMPT_TEMPLATE,
    CUSTOM_PROGRAM_PROMPT_TEMPLATE,
    ENHANCEMENT_PROMPT_TEMPLATE,
)
from abapify.utils.config import get_config_value
from abapify.utils.logger import get_logger

logger = get_logger(__name__)


class AbapGenerator:
    """Gerador de código ABAP usando modelos de linguagem."""

    def __init__(self, model_name: Optional[str] = None, use_enhanced_prompts: bool = True):
        """
        Inicializa o gerador de código ABAP.

        Args:
            model_name: Nome do modelo a ser utilizado (opcional).
            use_enhanced_prompts: Se deve usar prompts aprimorados (padrão: True).
        """
        self.llm_client = LLMClient()
        self.model_name = model_name
        self.system_prompt = ENHANCED_SYSTEM_PROMPT if use_enhanced_prompts else SIMPLE_SYSTEM_PROMPT

    def _generate_code(self, prompt: str, temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """
        Método principal para gerar código ABAP.

        Args:
            prompt: Prompt para o modelo de linguagem.
            temperature: Temperatura para geração (opcional).
            max_tokens: Máximo de tokens (opcional).

        Returns:
            str: Código ABAP gerado.
        """
        try:
            # Usa configurações padrão se não especificado
            temp = temperature or float(get_config_value("DEFAULT_TEMPERATURE", "0.7"))
            tokens = max_tokens or int(get_config_value("DEFAULT_MAX_TOKENS", "4096"))
            
            response = self.llm_client.generate(
                system_prompt=self.system_prompt,
                user_prompt=prompt,
                model_name=self.model_name,
                temperature=temp,
                max_tokens=tokens,
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

    def generate_custom_program(
        self,
        specification: str,
        program_type: str = "Report",
        main_features: str = "",
        entities: str = "",
        integrations: str = "Nenhuma",
        business_rules: str = "",
        performance_requirements: str = "Padrão",
        security_requirements: str = "Verificações de autorização padrão",
        usability_requirements: str = "Interface intuitiva",
    ) -> str:
        """
        Gera um programa ABAP customizado baseado em especificação detalhada.

        Args:
            specification: Especificação completa do programa.
            program_type: Tipo do programa (Report, Class, Function Group, etc.).
            main_features: Funcionalidades principais.
            entities: Tabelas/entidades envolvidas.
            integrations: Integrações necessárias.
            business_rules: Regras de negócio específicas.
            performance_requirements: Requisitos de performance.
            security_requirements: Requisitos de segurança.
            usability_requirements: Requisitos de usabilidade.

        Returns:
            str: Código ABAP do programa customizado.
        """
        prompt = CUSTOM_PROGRAM_PROMPT_TEMPLATE.format(
            specification=specification,
            program_type=program_type,
            main_features=main_features,
            entities=entities,
            integrations=integrations,
            business_rules=business_rules,
            performance_requirements=performance_requirements,
            security_requirements=security_requirements,
            usability_requirements=usability_requirements,
        )
        logger.info(f"Gerando programa customizado: {program_type}")
        return self._generate_code(prompt, temperature=0.8, max_tokens=8192)

    def generate_enhancement(
        self,
        base_object: str,
        enhancement_type: str,
        functionality: str,
        enhancement_points: str = "",
    ) -> str:
        """
        Gera um enhancement ABAP.

        Args:
            base_object: Objeto base a ser melhorado.
            enhancement_type: Tipo de enhancement (BADI, Enhancement Point, etc.).
            functionality: Funcionalidade a ser adicionada.
            enhancement_points: Pontos específicos de enhancement.

        Returns:
            str: Código ABAP do enhancement.
        """
        prompt = ENHANCEMENT_PROMPT_TEMPLATE.format(
            base_object=base_object,
            enhancement_type=enhancement_type,
            functionality=functionality,
            enhancement_points=enhancement_points,
        )
        logger.info(f"Gerando enhancement: {enhancement_type} para {base_object}")
        return self._generate_code(prompt)