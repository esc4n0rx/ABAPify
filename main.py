#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ABAPify - Gerador de código ABAP baseado em IA
Enhanced Edition v2.0
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
    generate_custom_program,
    generate_enhancement,
)
from abapify.utils.config import load_config, list_config, get_sap_environments
from abapify.utils.logger import setup_logger

# Inicializa o console e logger
console = Console()
logger = setup_logger()


def print_header():
    """Exibe o cabeçalho do ABAPify."""
    console.print(Panel.fit(
        "[bold blue]ABAPify Enhanced Edition v2.0[/bold blue]\n"
        "[cyan]Gerador de código ABAP baseado em IA[/cyan]\n"
        "[dim]Powered by Arcee Conductor + SAP Integration[/dim]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print("")


def show_config_status():
    """Exibe o status das configurações."""
    try:
        config = list_config()
        provider = config.get("DEFAULT_PROVIDER", "Não configurado")
        
        # Verifica se há pelo menos uma API key configurada
        has_api_key = any([
            config.get("ARCEE_TOKEN") and config.get("ARCEE_TOKEN") != "NÃO CONFIGURADO",
            config.get("GROQ_API_KEY") and config.get("GROQ_API_KEY") != "NÃO CONFIGURADO",
            config.get("OPENAI_API_KEY") and config.get("OPENAI_API_KEY") != "NÃO CONFIGURADO",
        ])
        
        # Verifica configuração SAP
        sap_environments = get_sap_environments()
        has_sap = len(sap_environments) > 0
        
        # Status LLM
        if has_api_key:
            console.print(f"[green]✅ LLM Configurado - Provedor: {provider}[/green]")
        else:
            console.print("[red]❌ LLM não configurado - Execute a opção 9 para configurar[/red]")
        
        # Status SAP
        if has_sap:
            console.print(f"[green]✅ SAP Configurado - Ambientes: {', '.join(sap_environments)}[/green]")
        else:
            console.print("[yellow]⚠️  SAP não configurado - Funcionalidades básicas disponíveis[/yellow]")
        
    except Exception:
        console.print("[red]❌ Erro nas configurações - Execute a opção 9[/red]")


def show_main_menu() -> int:
    """
    Exibe o menu principal e retorna a opção selecionada.
    
    Returns:
        int: Número da opção selecionada.
    """
    table = Table(show_header=False, box=None)
    
    # Opções básicas
    table.add_row("[1]", "Gerar Relatório ALV")
    table.add_row("[2]", "Gerar Relatório Simples")
    table.add_row("[3]", "Gerar Classe ABAP")
    table.add_row("[4]", "Gerar Módulo de Função")
    table.add_row("[5]", "Gerar Estrutura")
    table.add_row("[6]", "Gerar Teste Unitário")
    table.add_row("[7]", "[bold yellow]Gerar Programa Personalizado[/bold yellow]")
    table.add_row("[8]", "Gerar Enhancement")
    
    # Opções SAP
    table.add_row("", "")  # Espaço
    table.add_row("", "[bold green]🚀 Funcionalidades SAP[/bold green]")
    table.add_row("[10]", "[bold green]Gerar com Análise SAP[/bold green]")
    table.add_row("[11]", "[green]Analisar Tabela SAP[/green]")
    table.add_row("[12]", "[green]Testar Conexão SAP[/green]")
    
    # Configurações
    table.add_row("", "")  # Espaço
    table.add_row("[9]", "[bold cyan]Configurações[/bold cyan]")
    table.add_row("[0]", "Sair")
    
    console.print(Panel(table, title="Selecione uma opção", border_style="cyan"))
    
    choice = Prompt.ask("Opção", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], default="0")
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


def handle_custom_program_generation():
   """Manipula o fluxo de geração de programa personalizado."""
   console.print("\n[bold yellow]Geração de Programa Personalizado[/bold yellow]")
   console.print("[dim]Este recurso permite criar programas ABAP complexos baseados em especificações detalhadas[/dim]")
   
   output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
   
   with console.status("[cyan]Iniciando assistente interativo...[/cyan]"):
       generate_custom_program(output_dir)


def handle_enhancement_generation():
   """Manipula o fluxo de geração de enhancement ABAP."""
   console.print("\n[bold cyan]Geração de Enhancement ABAP[/bold cyan]")
   
   base_object = Prompt.ask("[cyan]Objeto base a ser melhorado[/cyan]")
   
   enhancement_type = Prompt.ask(
       "[cyan]Tipo de enhancement[/cyan]",
       choices=["BADI", "Enhancement Point", "Customer Exit", "User Exit"],
       default="BADI"
   )
   
   functionality = Prompt.ask("[cyan]Funcionalidade a ser adicionada[/cyan]")
   
   enhancement_points = Prompt.ask("[cyan]Pontos específicos de enhancement[/cyan]", default="")
   
   output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
   default_filename = f"z_enh_{base_object.lower().replace(' ', '_')[:15]}.abap"
   filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
   
   with console.status("[cyan]Gerando código ABAP...[/cyan]"):
       generate_enhancement(
           base_object=base_object,
           enhancement_type=enhancement_type,
           functionality=functionality,
           output_dir=output_dir,
           filename=filename,
           enhancement_points=enhancement_points,
       )


def handle_sap_aware_generation():
   """Manipula geração com análise SAP automática."""
   console.print("\n[bold green]🚀 Geração com Análise SAP[/bold green]")
   console.print("[dim]Esta funcionalidade analisa automaticamente as tabelas no SAP para gerar código otimizado[/dim]")
   
   # Verifica se há ambientes SAP configurados
   sap_environments = get_sap_environments()
   if not sap_environments:
       console.print("[red]Erro: Nenhum ambiente SAP configurado![/red]")
       console.print("Execute [cyan]Configurações > Configurar SAP[/cyan] primeiro.")
       return
   
   # Seleção do ambiente
   environment = Prompt.ask(
       "[cyan]Ambiente SAP[/cyan]",
       choices=sap_environments,
       default=sap_environments[0]
   )
   
   # Tipo de código
   code_type = Prompt.ask(
       "[cyan]Tipo de código[/cyan]",
       choices=["alv", "report"],
       default="alv"
   )
   
   description = Prompt.ask("[cyan]Descrição[/cyan]")
   
   tables = []
   console.print("[cyan]Tabelas a serem analisadas[/cyan] (deixe vazio para finalizar)")
   
   while True:
       table = Prompt.ask("  Nome da tabela", default="")
       if not table:
           break
       tables.append(table)
   
   if not tables:
       console.print("[red]Erro: Pelo menos uma tabela deve ser especificada para análise SAP[/red]")
       return
   
   output_dir = Prompt.ask("[cyan]Diretório de saída[/cyan]", default="./output")
   default_filename = f"z_sap_{code_type}_{description.lower().replace(' ', '_')[:15]}.abap"
   filename = Prompt.ask("[cyan]Nome do arquivo[/cyan]", default=default_filename)
   
   try:
       from abapify.cli.sap_commands import generate_sap_aware_code
       
       with console.status(f"[cyan]Conectando ao SAP {environment} e analisando tabelas...[/cyan]"):
           generate_sap_aware_code(
               code_type=code_type,
               description=description,
               tables=tables,
               output_dir=output_dir,
               filename=filename,
               sap_environment=environment
           )
   except ImportError:
       console.print("[red]Erro: Módulo SAP não disponível. Verifique a instalação.[/red]")
   except Exception as e:
       console.print(f"[red]Erro na geração SAP-aware: {str(e)}[/red]")


def handle_analyze_table():
   """Manipula análise de tabela SAP."""
   console.print("\n[bold green]Análise de Tabela SAP[/bold green]")
   
   # Verifica ambientes SAP
   sap_environments = get_sap_environments()
   if not sap_environments:
       console.print("[red]Erro: Nenhum ambiente SAP configurado![/red]")
       return
   
   environment = Prompt.ask(
       "[cyan]Ambiente SAP[/cyan]",
       choices=sap_environments,
       default=sap_environments[0]
   )
   
   table_name = Prompt.ask("[cyan]Nome da tabela[/cyan]").upper()
   
   include_relationships = Confirm.ask(
       "[cyan]Incluir análise de relacionamentos?[/cyan]",
       default=True
   )
   
   save_analysis = Confirm.ask(
       "[cyan]Salvar análise em arquivo JSON?[/cyan]",
       default=False
   )
   
   output_file = None
   if save_analysis:
       output_file = Prompt.ask(
           "[cyan]Nome do arquivo de análise[/cyan]",
           default=f"analise_{table_name.lower()}.json"
       )
   
   try:
       from abapify.cli.sap_commands import analyze_table_structure
       analyze_table_structure(
           table_name=table_name,
           environment=environment,
           include_relationships=include_relationships,
           output_file=output_file
       )
   except ImportError:
       console.print("[red]Erro: Módulo SAP não disponível.[/red]")
   except Exception as e:
       console.print(f"[red]Erro na análise: {str(e)}[/red]")


def handle_test_sap_connection():
   """Manipula teste de conexão SAP."""
   console.print("\n[bold green]Teste de Conexão SAP[/bold green]")
   
   sap_environments = get_sap_environments()
   if not sap_environments:
       console.print("[red]Erro: Nenhum ambiente SAP configurado![/red]")
       return
   
   environment = Prompt.ask(
       "[cyan]Ambiente SAP para testar[/cyan]",
       choices=sap_environments,
       default=sap_environments[0]
   )
   
   try:
       from abapify.cli.config_commands import test_sap_connection
       test_sap_connection.callback(environment=environment)
   except ImportError:
       console.print("[red]Erro: Módulo SAP não disponível.[/red]")
   except Exception as e:
       console.print(f"[red]Erro no teste: {str(e)}[/red]")


def handle_configuration():
   """Manipula o menu de configurações."""
   console.print("\n[bold cyan]Menu de Configurações[/bold cyan]")
   
   config_table = Table(show_header=False, box=None)
   config_table.add_row("[1]", "Exibir configurações atuais")
   config_table.add_row("[2]", "Configurar provedor de IA")
   config_table.add_row("[3]", "Configurar chaves de API")
   config_table.add_row("[4]", "Configuração completa (assistente)")
   config_table.add_row("[5]", "[bold yellow]Configurar SAP[/bold yellow]")
   config_table.add_row("[6]", "[yellow]Testar conexão SAP[/yellow]")
   config_table.add_row("[0]", "Voltar ao menu principal")
   
   console.print(Panel(config_table, title="Opções de Configuração", border_style="cyan"))
   
   choice = Prompt.ask("Opção", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")
   
   if choice == "1":
       # Exibir configurações
       from abapify.cli.config_commands import show_config
       show_config.callback()
   
   elif choice == "2":
       # Configurar provedor
       from abapify.utils.config import save_config
       provider = Prompt.ask(
           "Provedor padrão",
           choices=["arcee", "groq", "openai"],
           default="arcee"
       )
       save_config({"DEFAULT_PROVIDER": provider})
       console.print(f"[green]Provedor configurado para: {provider}[/green]")
   
   elif choice == "3":
       # Configurar chaves de API
       from abapify.utils.config import save_config
       config_updates = {}
       
       console.print("[cyan]Configure as chaves de API (deixe vazio para manter atual):[/cyan]")
       
       arcee_token = Prompt.ask("Token Arcee", password=True, default="")
       if arcee_token:
           config_updates["ARCEE_TOKEN"] = arcee_token
       
       groq_key = Prompt.ask("Chave Groq", password=True, default="")
       if groq_key:
           config_updates["GROQ_API_KEY"] = groq_key
       
       openai_key = Prompt.ask("Chave OpenAI", password=True, default="")
       if openai_key:
           config_updates["OPENAI_API_KEY"] = openai_key
       
       if config_updates:
           save_config(config_updates)
           console.print("[green]Chaves de API atualizadas![/green]")
       else:
           console.print("[yellow]Nenhuma chave foi alterada.[/yellow]")
   
   elif choice == "4":
       # Configuração completa
       from abapify.cli.config_commands import setup_config
       setup_config.callback()
   
   elif choice == "5":
       # Configurar SAP
       from abapify.cli.config_commands import setup_sap_config_command
       setup_sap_config_command.callback()
   
   elif choice == "6":
       # Testar SAP
       handle_test_sap_connection()


def main():
   """Função principal do ABAPify."""
   try:
       # Carrega configurações
       load_config()
       
       # Exibe cabeçalho
       print_header()
       
       # Exibe status das configurações
       show_config_status()
       
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
           elif choice == 7:
               handle_custom_program_generation()
           elif choice == 8:
               handle_enhancement_generation()
           elif choice == 9:
               handle_configuration()
           elif choice == 10:
               handle_sap_aware_generation()
           elif choice == 11:
               handle_analyze_table()
           elif choice == 12:
               handle_test_sap_connection()
           
           console.print("")
           if choice not in [9, 11, 12] and not Confirm.ask("[cyan]Deseja realizar outra operação?[/cyan]", default=True):
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