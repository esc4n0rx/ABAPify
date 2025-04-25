#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interface de linha de comando principal para o ABAPify.
"""

import os
import sys
from typing import Optional

import click
from rich.console import Console
from rich.traceback import install

from abapify.cli.commands import (
    generate_alv,
    generate_class,
    generate_function_module,
    generate_report,
    generate_test,
    generate_structure,
)
from abapify.utils.config import load_config
from abapify.utils.logger import setup_logger

# Instala um formatador de exceções melhorado
install()

# Console para saída rica
console = Console()

# Configura o logger
logger = setup_logger()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """ABAPify - Gerador de código ABAP baseado em IA."""
    # Tenta carregar configurações
    try:
        load_config()
    except Exception as e:
        console.print(f"[bold red]Erro ao carregar configurações:[/] {str(e)}")
        sys.exit(1)


@main.command("generate-alv")
@click.option(
    "--description",
    "-d",
    required=True,
    help="Descrição do relatório ALV a ser gerado",
)
@click.option(
    "--tables",
    "-t",
    multiple=True,
    help="Tabelas a serem utilizadas no relatório",
)
@click.option(
    "--output",
    "-o",
    default="./output",
    help="Diretório de saída para o código gerado",
)
@click.option(
    "--filename",
    "-f",
    help="Nome do arquivo de saída (sem extensão)",
)
def alv_command(
    description: str, tables: tuple[str, ...], output: str, filename: Optional[str]
):
    """Gera um relatório ALV com base na descrição fornecida."""
    filename = filename or f"z_alv_{description.lower().replace(' ', '_')[:20]}.abap"
    generate_alv(description, tables, output, filename)


@main.command("generate-report")
@click.option(
    "--description",
    "-d",
    required=True,
    help="Descrição do relatório a ser gerado",
)
@click.option(
    "--tables",
    "-t",
    multiple=True,
    help="Tabelas a serem utilizadas no relatório",
)
@click.option(
    "--output",
    "-o",
    default="./output",
    help="Diretório de saída para o código gerado",
)
@click.option(
    "--filename",
    "-f",
    help="Nome do arquivo de saída (sem extensão)",
)
def report_command(
    description: str, tables: tuple[str, ...], output: str, filename: Optional[str]
):
    """Gera um relatório ABAP com base na descrição fornecida."""
    filename = filename or f"z_report_{description.lower().replace(' ', '_')[:20]}.abap"
    generate_report(description, tables, output, filename)


@main.command("generate-class")
@click.option(
    "--description",
    "-d",
    required=True,
    help="Descrição da classe a ser gerada",
)
@click.option(
    "--methods",
    "-m",
    multiple=True,
    help="Métodos a serem incluídos na classe",
)
@click.option(
    "--output",
    "-o",
    default="./output",
    help="Diretório de saída para o código gerado",
)
@click.option(
    "--filename",
    "-f",
    help="Nome do arquivo de saída (sem extensão)",
)
def class_command(
    description: str, methods: tuple[str, ...], output: str, filename: Optional[str]
):
    """Gera uma classe ABAP com base na descrição fornecida."""
    filename = filename or f"zcl_{description.lower().replace(' ', '_')[:20]}.abap"
    generate_class(description, methods, output, filename)


@main.command("generate-function")
@click.option(
    "--description",
    "-d",
    required=True,
    help="Descrição do módulo de função a ser gerado",
)
@click.option(
    "--params",
    "-p",
    multiple=True,
    help="Parâmetros a serem incluídos no módulo de função",
)
@click.option(
    "--output",
    "-o",
    default="./output",
    help="Diretório de saída para o código gerado",
)
@click.option(
    "--filename",
    "-f",
    help="Nome do arquivo de saída (sem extensão)",
)
def function_command(
    description: str, params: tuple[str, ...], output: str, filename: Optional[str]
):
    """Gera um módulo de função ABAP com base na descrição fornecida."""
    filename = filename or f"z_fm_{description.lower().replace(' ', '_')[:20]}.abap"
    generate_function_module(description, params, output, filename)


@main.command("generate-structure")
@click.option(
    "--description",
    "-d",
    required=True,
    help="Descrição da estrutura a ser gerada",
)
@click.option(
    "--fields",
    "-f",
    multiple=True,
    help="Campos a serem incluídos na estrutura",
)
@click.option(
    "--output",
    "-o",
    default="./output",
    help="Diretório de saída para o código gerado",
)
@click.option(
    "--filename",
    "-f",
    help="Nome do arquivo de saída (sem extensão)",
)
def structure_command(
    description: str, fields: tuple[str, ...], output: str, filename: Optional[str]
):
    """Gera uma estrutura ABAP com base na descrição fornecida."""
    filename = filename or f"zstruct_{description.lower().replace(' ', '_')[:20]}.abap"
    generate_structure(description, fields, output, filename)


@main.command("generate-test")
@click.option(
    "--target",
    "-t",
    required=True,
    help="Nome da classe ou módulo de função a ser testado",
)
@click.option(
    "--output",
    "-o",
    default="./output",
    help="Diretório de saída para o código gerado",
)
@click.option(
    "--filename",
    "-f",
    help="Nome do arquivo de saída (sem extensão)",
)
def test_command(target: str, output: str, filename: Optional[str]):
    """Gera um teste unitário ABAP para a classe ou módulo especificado."""
    filename = filename or f"zcl_test_{target.lower().replace(' ', '_')[:20]}.abap"
    generate_test(target, output, filename)


if __name__ == "__main__":
    main()