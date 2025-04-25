#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para a interface de linha de comando.
"""

import os
import tempfile
from unittest import TestCase, mock

from click.testing import CliRunner

from abapify.cli.main import main


class TestCLI(TestCase):
    """Testes para a interface de linha de comando."""

    def setUp(self):
        """Configuração dos testes."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Limpeza após os testes."""
        # Limpa arquivos temporários
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    @mock.patch("abapify.cli.commands.AbapGenerator")
    def test_generate_alv(self, mock_generator):
        """Testa o comando generate-alv."""
        # Configura o mock
        instance = mock_generator.return_value
        instance.generate_alv.return_value = "REPORT Z_TEST."

        # Executa o comando
        result = self.runner.invoke(
            main,
            [
                "generate-alv",
                "--description",
                "Relatório de teste",
                "--tables",
                "MARA",
                "--output",
                self.temp_dir,
                "--filename",
                "test_alv.abap",
            ],
        )

        # Verifica se o comando foi executado com sucesso
        self.assertEqual(0, result.exit_code)
        
        # Verifica se o gerador foi chamado corretamente
        instance.generate_alv.assert_called_once_with(
            "Relatório de teste", ["MARA"]
        )
        
        # Verifica se o arquivo foi criado
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test_alv.abap")))

    @mock.patch("abapify.cli.commands.AbapGenerator")
    def test_generate_class(self, mock_generator):
        """Testa o comando generate-class."""
        # Configura o mock
        instance = mock_generator.return_value
        instance.generate_class.return_value = "CLASS ZCL_TEST DEFINITION."

        # Executa o comando
        result = self.runner.invoke(
            main,
            [
                "generate-class",
                "--description",
                "Classe de teste",
                "--methods",
                "constructor",
                "--methods",
                "process",
                "--output",
                self.temp_dir,
                "--filename",
                "test_class.abap",
            ],
        )

        # Verifica se o comando foi executado com sucesso
        self.assertEqual(0, result.exit_code)
        
        # Verifica se o gerador foi chamado corretamente
        instance.generate_class.assert_called_once_with(
            "Classe de teste", ["constructor", "process"]
        )
        
        # Verifica se o arquivo foi criado
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test_class.abap")))