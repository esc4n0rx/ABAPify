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
    generate_custom_program,
    generate_enhancement,
)
from abapify.cli.config_commands import config
from abapify.utils.config import load_config
from abapify.utils.logger import setup_logger

# Instala um formatador de exceções melhorado
install()

# Console para saída rica
console = Console()

# Configura o logger
logger = setup_logger()


@click.group()
@click.version_option(version="2.0.0")
def main():
    """ABAPify - Gerador de código ABAP baseado em IA - Enhanced Edition."""
    # Tenta carregar configurações
    try:
        load_config()
    except Exception as e:
        console.print(f"[bold red]Erro ao carregar configurações:[/] {str(e)}")
        console.print("[yellow]Execute 'abapify config setup' para configurar o sistema.[/yellow]")
        # Não sai para permitir comandos de configuração


# Adiciona comandos de configuração
main.add_command(config)


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
@click.option(
    "--sap-environment",
    type=click.Choice(["DEV", "QAS", "PRD"]),
    help="Ambiente SAP para análise de metadados",
)
@click.option(
    "--analyze-tables",
    is_flag=True,
    help="Analisa automaticamente as tabelas no SAP",
)
def alv_command(
    description: str, 
    tables: tuple[str, ...], 
    output: str, 
    filename: Optional[str],
    sap_environment: Optional[str],
    analyze_tables: bool
):
    """Gera um relatório ALV com base na descrição fornecida."""
    filename = filename or f"z_alv_{description.lower().replace(' ', '_')[:20]}.abap"
    
    # Se análise SAP está habilitada, usa geração SAP-aware
    if analyze_tables and tables:
        from abapify.cli.sap_commands import generate_sap_aware_alv
        generate_sap_aware_alv(
            description=description,
            tables=list(tables),
            output_dir=output,
            filename=filename,
            sap_environment=sap_environment or "DEV"
        )
    else:
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
@click.option(
    "--sap-environment",
    type=click.Choice(["DEV", "QAS", "PRD"]),
    help="Ambiente SAP para análise de metadados",
)
@click.option(
    "--analyze-tables",
    is_flag=True,
    help="Analisa automaticamente as tabelas no SAP",
)
def report_command(
    description: str, 
    tables: tuple[str, ...], 
    output: str, 
    filename: Optional[str],
    sap_environment: Optional[str],
    analyze_tables: bool
):
    """Gera um relatório ABAP com base na descrição fornecida."""
    filename = filename or f"z_report_{description.lower().replace(' ', '_')[:20]}.abap"
    
    # Se análise SAP está habilitada, usa geração SAP-aware
    if analyze_tables and tables:
        from abapify.cli.sap_commands import generate_sap_aware_report
        generate_sap_aware_report(
            description=description,
            tables=list(tables),
            output_dir=output,
            filename=filename,
            sap_environment=sap_environment or "DEV"
        )
    else:
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
    "-fn",
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


@main.command("generate-program")
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
def program_command(output: str, filename: Optional[str]):
    """Gera um programa ABAP personalizado usando assistente interativo."""
    generate_custom_program(output, filename)


@main.command("generate-enhancement")
@click.option(
    "--base-object",
    "-b",
    required=True,
    help="Objeto base a ser melhorado",
)
@click.option(
    "--type",
    "-t",
    required=True,
    type=click.Choice(["BADI", "Enhancement Point", "Customer Exit", "User Exit"]),
    help="Tipo de enhancement",
)
@click.option(
    "--functionality",
    "-func",
    required=True,
    help="Funcionalidade a ser adicionada",
)
@click.option(
    "--enhancement-points",
    "-ep",
    help="Pontos específicos de enhancement",
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
def enhancement_command(
    base_object: str,
    type: str,
    functionality: str,
    enhancement_points: Optional[str],
    output: str,
    filename: Optional[str]
):
    """Gera um enhancement ABAP."""
    filename = filename or f"z_enh_{base_object.lower().replace(' ', '_')[:15]}.abap"
    generate_enhancement(
        base_object=base_object,
        enhancement_type=type,
        functionality=functionality,
        output_dir=output,
        filename=filename,
        enhancement_points=enhancement_points or "",
    )


# Novos comandos SAP
@main.command("analyze-table")
@click.option(
    "--table-name",
    "-t",
    required=True,
    help="Nome da tabela a ser analisada",
)
@click.option(
    "--environment",
    "-e",
    type=click.Choice(["DEV", "QAS", "PRD"]),
    help="Ambiente SAP",
)
@click.option(
    "--include-relationships",
    is_flag=True,
    help="Incluir análise de relacionamentos",
)
@click.option(
    "--output",
    "-o",
    help="Arquivo de saída para salvar análise (JSON)",
)
def analyze_table_command(
    table_name: str,
    environment: Optional[str],
    include_relationships: bool,
    output: Optional[str]
):
    """Analisa estrutura de uma tabela SAP."""
    from abapify.cli.sap_commands import analyze_table_structure
    analyze_table_structure(
        table_name=table_name,
        environment=environment or "DEV",
        include_relationships=include_relationships,
        output_file=output
    )


@main.command("sap-generate")
@click.option(
    "--type",
    "-t",
    required=True,
    type=click.Choice(["alv", "report", "class"]),
    help="Tipo de código a gerar",
)
@click.option(
    "--description",
    "-d",
    required=True,
    help="Descrição do código a ser gerado",
)
@click.option(
    "--tables",
    "-tb",
    multiple=True,
    help="Tabelas a serem utilizadas",
)
@click.option(
    "--environment",
    "-e",
    type=click.Choice(["DEV", "QAS", "PRD"]),
    help="Ambiente SAP para análise",
)
@click.option(
    "--output",
    "-o",
    default="./output",
    help="Diretório de saída",
)
@click.option(
    "--filename",
    "-f",
    help="Nome do arquivo de saída",
)
def sap_generate_command(
    type: str,
    description: str,
    tables: tuple[str, ...],
    environment: Optional[str],
    output: str,
    filename: Optional[str]
):
    """Gera código ABAP com análise automática SAP."""
    from abapify.cli.sap_commands import generate_sap_aware_code
    generate_sap_aware_code(
        code_type=type,
        description=description,
        tables=list(tables),
        output_dir=output,
        filename=filename,
        sap_environment=environment or "DEV"
    )


if __name__ == "__main__":
    main()