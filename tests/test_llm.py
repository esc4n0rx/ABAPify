#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para o módulo LLM.
"""

import os
import unittest
from unittest import mock

from abapify.llm.client import LLMClient
from abapify.utils.exceptions import LLMProviderNotFoundError


class TestLLMClient(unittest.TestCase):
    """Testes para o cliente LLM."""

    @mock.patch.dict(os.environ, {"GROQ_API_KEY": "test_key"})
    def test_default_provider_groq(self):
        """Testa se o provedor padrão é Groq quando a chave está disponível."""
        client = LLMClient()
        self.assertEqual("groq", client._default_provider)

    @mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test_key", "GROQ_API_KEY": ""})
    def test_default_provider_openai(self):
        """Testa se o provedor padrão é OpenAI quando a chave está disponível."""
        client = LLMClient()
        self.assertEqual("openai", client._default_provider)

    @mock.patch.dict(os.environ, {"GROQ_API_KEY": "", "OPENAI_API_KEY": ""})
    def test_default_provider_fallback(self):
        """Testa se o provedor padrão é Groq quando nenhuma chave está disponível."""
        client = LLMClient()
        self.assertEqual("groq", client._default_provider)

    @mock.patch("abapify.llm.providers.groq_provider.GroqProvider")
    def test_generate_with_groq(self, mock_groq_provider):
        """Testa a geração de texto com o provedor Groq."""
        # Configura o mock
        instance = mock_groq_provider.return_value
        instance.generate.return_value = "Código ABAP gerado"

        # Cria o cliente e substitui o provedor
        client = LLMClient()
        client._providers["groq"] = instance
        client._default_provider = "groq"

        # Chama o método
        result = client.generate(
            system_prompt="Sistema",
            user_prompt="Usuário",
            temperature=0.5,
            max_tokens=2048,
        )

        # Verifica o resultado
        self.assertEqual("Código ABAP gerado", result)
        
        # Verifica se a chamada ao provedor foi feita corretamente
        instance.generate.assert_called_once_with(
            system_prompt="Sistema",
            user_prompt="Usuário",
            model_name=None,
            temperature=0.5,
            max_tokens=2048,
        )

    def test_invalid_provider(self):
        """Testa se uma exceção é lançada quando um provedor inválido é especificado."""
        client = LLMClient()
        
        with self.assertRaises(LLMProviderNotFoundError):
            client.generate(
                system_prompt="Sistema",
                user_prompt="Usuário",
                provider="provider_inexistente",
            )