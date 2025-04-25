#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ABAPify - Gerador de código ABAP baseado em IA
"""

import os
import sys
from typing import List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

# Importa localmente para evitar erros de módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Agora importa os módulos do projeto
from abapify.cli.commands import (
    generate_alv,
    generate_class,
    generate_function_module,
    generate_report,
    generate_structure,
    generate_test,
)
from abapify.utils.config import load_config
from abapify.utils.logger import setup_logger

# Inicializa o console e logger
console = Console()
logger = setup_logger()


def print_header():
    """Exibe o cabeçalho do ABAPify."""
    console.print(Panel.fit(
        "[bold blue]ABAPify[/bold blue] - [cyan]Gerador de código ABAP baseado em IA[/cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print("")


def show_main_menu() -> int:
    """
    Exibe o menu principal e retorna a opção selecionada.
    
    Returns:
        int: Número da opção selecionada.
    """
    table = Table(show_header=False, box=None)
    
    table.add_row("[1]", "Gerar Relatório ALV")
    table.add_row("[2]", "Gerar Relatório Simples")
    table.add_row("[3]", "Gerar Classe ABAP")
    table.add_row("[4]", "Gerar Módulo de Função")
    table.add_row("[5]", "Gerar Estrutura")
    table.add_row("[6]", "Gerar Teste Unitário")
    table.add_row("[0]", "Sair")
    
    console.print(Panel(table, title="Selecione uma opção", border_style="cyan"))
    
    choice = Prompt.ask("Opção", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")
    return int(choice)


def handle_alv_generation():
    """Manipula o fluxo de geração de relatório ALV."""
    console.print("\n[bold cyan]Geração de Relatório ALV[/bold cyan]")
    
    description = Prompt.ask("[cyan]Descrição do relatório[/cyan]")
    
    tables = []
    console.print("[cyan]Tabelas a serem utilizadas[/cyan] (deixe vazio para finalizar)")
    
    while True:
        table = Prompt.ask("  Nome da tabela", default="")
        if not table:
            break
        tables.append(table)
    
    if not tables:
        console.print("[yellow]Aviso: Nenhuma tabela especificada[/yellow]")
    
    output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
    default_filename = f"z_alv_{description.lower().replace(' ', '_')[:20]}.abap"
    filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
    
    with console.status("[cyan]Gerando código ABAP...[/cyan]"):
        generate_alv(description, tuple(tables), output_dir, filename)


def handle_report_generation():
    """Manipula o fluxo de geração de relatório simples."""
    console.print("\n[bold cyan]Geração de Relatório Simples[/bold cyan]")
    
    description = Prompt.ask("[cyan]Descrição do relatório[/cyan]")
    
    tables = []
    console.print("[cyan]Tabelas a serem utilizadas[/cyan] (deixe vazio para finalizar)")
    
    while True:
        table = Prompt.ask("  Nome da tabela", default="")
        if not table:
            break
        tables.append(table)
    
    if not tables:
        console.print("[yellow]Aviso: Nenhuma tabela especificada[/yellow]")
    
    output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
    default_filename = f"z_report_{description.lower().replace(' ', '_')[:20]}.abap"
    filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
    
    with console.status("[cyan]Gerando código ABAP...[/cyan]"):
        generate_report(description, tuple(tables), output_dir, filename)


def handle_class_generation():
    """Manipula o fluxo de geração de classe ABAP."""
    console.print("\n[bold cyan]Geração de Classe ABAP[/bold cyan]")
    
    description = Prompt.ask("[cyan]Descrição/propósito da classe[/cyan]")
    
    methods = []
    console.print("[cyan]Métodos a serem implementados[/cyan] (deixe vazio para finalizar)")
    
    while True:
        method = Prompt.ask("  Nome do método", default="")
        if not method:
            break
        methods.append(method)
    
    if not methods:
        methods.append("constructor")
        console.print("[yellow]Adicionando método constructor por padrão[/yellow]")
    
    output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
    default_filename = f"zcl_{description.lower().replace(' ', '_')[:20]}.abap"
    filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
    
    with console.status("[cyan]Gerando código ABAP...[/cyan]"):
        generate_class(description, tuple(methods), output_dir, filename)


def handle_function_generation():
    """Manipula o fluxo de geração de módulo de função ABAP."""
    console.print("\n[bold cyan]Geração de Módulo de Função ABAP[/bold cyan]")
    
    description = Prompt.ask("[cyan]Descrição/propósito do módulo de função[/cyan]")
    
    params = []
    console.print("[cyan]Parâmetros do módulo[/cyan] (deixe vazio para finalizar)")
    console.print("  Formato: NOME:TIPO:DIREÇÃO (ex: VBELN:CHAR(10):I para importação)")
    
    while True:
        param = Prompt.ask("  Parâmetro", default="")
        if not param:
            break
        params.append(param)
    
    if not params:
        console.print("[yellow]Aviso: Nenhum parâmetro especificado[/yellow]")
    
    output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
    default_filename = f"z_fm_{description.lower().replace(' ', '_')[:20]}.abap"
    filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
    
    with console.status("[cyan]Gerando código ABAP...[/cyan]"):
        generate_function_module(description, tuple(params), output_dir, filename)


def handle_structure_generation():
    """Manipula o fluxo de geração de estrutura ABAP."""
    console.print("\n[bold cyan]Geração de Estrutura ABAP[/bold cyan]")
    
    description = Prompt.ask("[cyan]Descrição/propósito da estrutura[/cyan]")
    
    fields = []
    console.print("[cyan]Campos da estrutura[/cyan] (deixe vazio para finalizar)")
    console.print("  Formato: NOME:TIPO (ex: MATNR:CHAR(18))")
    
    while True:
        field = Prompt.ask("  Campo", default="")
        if not field:
            break
        fields.append(field)
    
    if not fields:
        console.print("[yellow]Aviso: Nenhum campo especificado[/yellow]")
    
    output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
    default_filename = f"zstruct_{description.lower().replace(' ', '_')[:20]}.abap"
    filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
    
    with console.status("[cyan]Gerando código ABAP...[/cyan]"):
        generate_structure(description, tuple(fields), output_dir, filename)


def handle_test_generation():
    """Manipula o fluxo de geração de teste unitário ABAP."""
    console.print("\n[bold cyan]Geração de Teste Unitário ABAP[/bold cyan]")
    
    target = Prompt.ask("[cyan]Nome da classe ou módulo a ser testado[/cyan]")
    
    output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
    default_filename = f"zcl_test_{target.lower().replace(' ', '_')[:20]}.abap"
    filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
    
    with console.status("[cyan]Gerando código ABAP...[/cyan]"):
        generate_test(target, output_dir, filename)


def main():
    """Função principal do ABAPify."""
    try:
        # Carrega configurações
        load_config()
        
        # Exibe cabeçalho
        print_header()
        
        # Loop principal
        while True:
            choice = show_main_menu()
            
            if choice == 0:
                console.print("[cyan]Encerrando ABAPify...[/cyan]")
                break
            elif choice == 1:
                handle_alv_generation()
            elif choice == 2:
                handle_report_generation()
            elif choice == 3:
                handle_class_generation()
            elif choice == 4:
                handle_function_generation()
            elif choice == 5:
                handle_structure_generation()
            elif choice == 6:
                handle_test_generation()
            
            console.print("")
            if not Confirm.ask("[cyan]Deseja realizar outra operação?[/cyan]", default=True):
                console.print("[cyan]Encerrando ABAPify...[/cyan]")
                break
    
    except KeyboardInterrupt:
        console.print("\n[cyan]Operação cancelada pelo usuário.[/cyan]")
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        console.print(f"[bold red]Erro inesperado:[/] {str(e)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())