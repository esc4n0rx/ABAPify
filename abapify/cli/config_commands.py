#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comandos de configuração para a CLI do ABAPify.
"""

import os
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

from abapify.utils.config import save_config, list_config, get_config_value
from abapify.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


@click.group()
def config():
    """Comandos de configuração do ABAPify."""
    pass


@config.command("set")
@click.option(
    "--provider",
    type=click.Choice(["arcee", "groq", "openai"]),
    help="Define o provedor padrão de IA"
)
@click.option("--arcee-token", help="Token da API Arcee")
@click.option("--groq-key", help="Chave da API Groq")
@click.option("--openai-key", help="Chave da API OpenAI")
@click.option("--output-dir", help="Diretório padrão de saída")
@click.option("--temperature", type=float, help="Temperatura padrão (0.0-1.0)")
@click.option("--max-tokens", type=int, help="Máximo de tokens padrão")
def set_config(
    provider: Optional[str],
    arcee_token: Optional[str],
    groq_key: Optional[str],
    openai_key: Optional[str],
    output_dir: Optional[str],
    temperature: Optional[float],
    max_tokens: Optional[int]
):
    """Define configurações do ABAPify."""
    try:
        config_updates = {}
        
        if provider:
            config_updates["DEFAULT_PROVIDER"] = provider
            console.print(f"[green]Provedor padrão definido como:[/] {provider}")
        
        if arcee_token:
            config_updates["ARCEE_TOKEN"] = arcee_token
            console.print("[green]Token Arcee configurado[/]")
        
        if groq_key:
            config_updates["GROQ_API_KEY"] = groq_key
            console.print("[green]Chave Groq configurada[/]")
        
        if openai_key:
            config_updates["OPENAI_API_KEY"] = openai_key
            console.print("[green]Chave OpenAI configurada[/]")
        
        if output_dir:
            config_updates["OUTPUT_DIR"] = output_dir
            console.print(f"[green]Diretório de saída definido como:[/] {output_dir}")
        
        if temperature is not None:
            if 0.0 <= temperature <= 1.0:
                config_updates["DEFAULT_TEMPERATURE"] = str(temperature)
                console.print(f"[green]Temperatura padrão definida como:[/] {temperature}")
            else:
                console.print("[red]Erro: Temperatura deve estar entre 0.0 e 1.0[/]")
                return
        
        if max_tokens:
            config_updates["DEFAULT_MAX_TOKENS"] = str(max_tokens)
            console.print(f"[green]Máximo de tokens definido como:[/] {max_tokens}")
        
        if config_updates:
            save_config(config_updates)
            console.print("\n[bold green]Configurações salvas com sucesso![/]")
        else:
            console.print("[yellow]Nenhuma configuração foi alterada.[/]")
    
    except Exception as e:
        logger.error(f"Erro ao definir configurações: {str(e)}")
        console.print(f"[bold red]Erro ao definir configurações:[/] {str(e)}")


@config.command("show")
def show_config():
    """Exibe as configurações atuais."""
    try:
        config_data = list_config()
        
        table = Table(title="Configurações do ABAPify", show_header=True)
        table.add_column("Configuração", style="cyan", width=25)
        table.add_column("Valor", style="white")
        
        for key, value in config_data.items():
            # Formata o nome da configuração
            display_name = key.replace("_", " ").title()
            table.add_row(display_name, value or "[dim]Não configurado[/dim]")
        
        console.print(table)
    
    except Exception as e:
        logger.error(f"Erro ao exibir configurações: {str(e)}")
        console.print(f"[bold red]Erro ao exibir configurações:[/] {str(e)}")


@config.command("setup")
def setup_config():
    """Assistente interativo para configuração inicial."""
    console.print(Panel.fit(
        "[bold blue]Assistente de Configuração do ABAPify[/bold blue]",
        border_style="blue"
    ))
    
    try:
        config_updates = {}
        
        # Configuração do provedor
        console.print("\n[cyan]Escolha o provedor de IA padrão:[/cyan]")
        provider = Prompt.ask(
            "Provedor",
            choices=["arcee", "groq", "openai"],
            default="arcee"
        )
        config_updates["DEFAULT_PROVIDER"] = provider
        
        # Configuração das chaves de API
        console.print(f"\n[cyan]Configure as credenciais para {provider}:[/cyan]")
        
        if provider == "arcee":
            token = Prompt.ask("Token Arcee", password=True)
            if token:
                config_updates["ARCEE_TOKEN"] = token
        elif provider == "groq":
            key = Prompt.ask("Chave API Groq", password=True)
            if key:
                config_updates["GROQ_API_KEY"] = key
        elif provider == "openai":
            key = Prompt.ask("Chave API OpenAI", password=True)
            if key:
                config_updates["OPENAI_API_KEY"] = key
        
        # Outras configurações opcionais
        if Confirm.ask("\nDeseja configurar opções avançadas?", default=False):
            output_dir = Prompt.ask("Diretório de saída", default="./output")
            config_updates["OUTPUT_DIR"] = output_dir
            
            temperature = Prompt.ask("Temperatura (0.0-1.0)", default="0.7")
            try:
                temp_float = float(temperature)
                if 0.0 <= temp_float <= 1.0:
                    config_updates["DEFAULT_TEMPERATURE"] = temperature
            except ValueError:
                console.print("[yellow]Temperatura inválida, usando padrão (0.7)[/yellow]")
            
            max_tokens = Prompt.ask("Máximo de tokens", default="4096")
            try:
                config_updates["DEFAULT_MAX_TOKENS"] = str(int(max_tokens))
            except ValueError:
                console.print("[yellow]Valor inválido para tokens, usando padrão (4096)[/yellow]")
        
        # Salva as configurações
        save_config(config_updates)
        
        console.print("\n[bold green]✅ Configuração concluída com sucesso![/]")
        console.print("Execute [cyan]abapify config show[/cyan] para ver as configurações.")
    
    except Exception as e:
        logger.error(f"Erro no assistente de configuração: {str(e)}")
        console.print(f"[bold red]Erro no assistente de configuração:[/] {str(e)}")