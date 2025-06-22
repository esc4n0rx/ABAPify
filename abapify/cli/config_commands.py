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

from abapify.utils.config import save_config, list_config, get_config_value, get_sap_environments
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
        
        # Separar configurações por categoria
        llm_config = {k: v for k, v in config_data.items() 
                     if not k.startswith("SAP_") and k not in ["OUTPUT_DIR"]}
        sap_config = {k: v for k, v in config_data.items() if k.startswith("SAP_")}
        other_config = {k: v for k, v in config_data.items() 
                       if k in ["OUTPUT_DIR"] or (not k.startswith("SAP_") and k not in llm_config)}
        
        # Tabela LLM
        if llm_config:
            table_llm = Table(title="Configurações LLM", show_header=True)
            table_llm.add_column("Configuração", style="cyan", width=25)
            table_llm.add_column("Valor", style="white")
            
            for key, value in llm_config.items():
                display_name = key.replace("_", " ").title()
                table_llm.add_row(display_name, value or "[dim]Não configurado[/dim]")
            
            console.print(table_llm)
            console.print()
        
        # Tabela SAP
        if sap_config:
            table_sap = Table(title="Configurações SAP", show_header=True)
            table_sap.add_column("Configuração", style="yellow", width=30)
            table_sap.add_column("Valor", style="white")
            
            for key, value in sap_config.items():
                display_name = key.replace("SAP_", "").replace("_", " ").title()
                table_sap.add_row(display_name, value or "[dim]Não configurado[/dim]")
            
            console.print(table_sap)
            console.print()
        
        # Tabela outras configurações
        if other_config:
            table_other = Table(title="Outras Configurações", show_header=True)
            table_other.add_column("Configuração", style="green", width=25)
            table_other.add_column("Valor", style="white")
            
            for key, value in other_config.items():
                display_name = key.replace("_", " ").title()
                table_other.add_row(display_name, value or "[dim]Não configurado[/dim]")
            
            console.print(table_other)
    
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
        
        # Configuração do provedor LLM
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
        
        # Configuração SAP
        if Confirm.ask("\nDeseja configurar integração SAP?", default=True):
            setup_sap_config(config_updates)
        
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


@config.command("sap")
@click.option(
    "--environment",
    type=click.Choice(["DEV", "QAS", "PRD"]),
    help="Ambiente SAP a configurar"
)
def setup_sap_config_command(environment: Optional[str]):
    """Configuração específica para SAP."""
    console.print(Panel.fit(
        "[bold yellow]Configuração SAP[/bold yellow]",
        border_style="yellow"
    ))
    
    config_updates = {}
    
    if not environment:
        environment = Prompt.ask(
            "Ambiente SAP",
            choices=["DEV", "QAS", "PRD"],
            default="DEV"
        )
    
    setup_sap_environment(environment, config_updates)
    
    if config_updates:
        save_config(config_updates)
        console.print(f"\n[bold green]✅ Configuração SAP {environment} salva![/]")
    else:
        console.print("[yellow]Nenhuma configuração foi alterada.[/yellow]")


def setup_sap_config(config_updates: dict):
    """Assistente de configuração SAP."""
    console.print("\n[yellow]Configuração SAP[/yellow]")
    
    # Ambiente padrão
    default_env = Prompt.ask(
        "Ambiente SAP padrão",
        choices=["DEV", "QAS", "PRD"],
        default="DEV"
    )
    config_updates["SAP_DEFAULT_ENVIRONMENT"] = default_env
    
    # Configurar ambiente
    setup_sap_environment(default_env, config_updates)
    
    # Configurar outros ambientes
    if Confirm.ask(f"\nDeseja configurar outros ambientes além de {default_env}?", default=False):
        for env in ["DEV", "QAS", "PRD"]:
            if env != default_env:
                if Confirm.ask(f"Configurar ambiente {env}?", default=False):
                    setup_sap_environment(env, config_updates)


def setup_sap_environment(environment: str, config_updates: dict):
    """Configura um ambiente SAP específico."""
    console.print(f"\n[cyan]Configuração do ambiente {environment}:[/cyan]")
    
    prefix = f"SAP_{environment}_"
    
    # Tipo de conexão
    connection_type = Prompt.ask(
        "Tipo de conexão",
        choices=["RFC", "HTTP"],
        default="RFC"
    )
    config_updates[f"{prefix}CONNECTION_TYPE"] = connection_type
    
    if connection_type == "RFC":
        # Configuração RFC
        ashost = Prompt.ask(f"Host do servidor de aplicação ({environment})")
        if ashost:
            config_updates[f"{prefix}ASHOST"] = ashost
        
        sysnr = Prompt.ask(f"Número do sistema ({environment})")
        if sysnr:
            config_updates[f"{prefix}SYSNR"] = sysnr
        
        client = Prompt.ask(f"Cliente ({environment})")
        if client:
            config_updates[f"{prefix}CLIENT"] = client
        
        user = Prompt.ask(f"Usuário ({environment})")
        if user:
            config_updates[f"{prefix}USER"] = user
        
        password = Prompt.ask(f"Senha ({environment})", password=True)
        if password:
            # Criptografa a senha
            from abapify.sap.auth import SAPAuthenticator
            auth = SAPAuthenticator()
            encrypted_password = auth.save_encrypted_password(environment, password)
            config_updates[f"{prefix}PASSWD_ENCRYPTED"] = encrypted_password
        
        # Configurações opcionais RFC
        if Confirm.ask(f"Configurar SAP Router para {environment}?", default=False):
            saprouter = Prompt.ask(f"SAP Router ({environment})")
            if saprouter:
                config_updates[f"{prefix}SAPROUTER"] = saprouter
        
        if Confirm.ask(f"Configurar Message Server para {environment}?", default=False):
            mshost = Prompt.ask(f"Message Server Host ({environment})")
            if mshost:
                config_updates[f"{prefix}MSHOST"] = mshost
            
            msserv = Prompt.ask(f"Message Server Service ({environment})")
            if msserv:
                config_updates[f"{prefix}MSSERV"] = msserv
            
            group = Prompt.ask(f"Logon Group ({environment})")
            if group:
                config_updates[f"{prefix}GROUP"] = group
    
    elif connection_type == "HTTP":
        # Configuração HTTP
        base_url = Prompt.ask(f"URL base do SAP ({environment})")
        if base_url:
            config_updates[f"{prefix}BASE_URL"] = base_url
        
        user = Prompt.ask(f"Usuário ({environment})")
        if user:
            config_updates[f"{prefix}USER"] = user
        
        password = Prompt.ask(f"Senha ({environment})", password=True)
        if password:
            # Criptografa a senha
            from abapify.sap.auth import SAPAuthenticator
            auth = SAPAuthenticator()
            encrypted_password = auth.save_encrypted_password(environment, password)
            config_updates[f"{prefix}PASSWD_ENCRYPTED"] = encrypted_password
        
        use_ssl = Confirm.ask(f"Usar SSL para {environment}?", default=True)
        config_updates[f"{prefix}USE_SSL"] = "true" if use_ssl else "false"
        
        if use_ssl:
            verify_ssl = Confirm.ask(f"Verificar certificado SSL para {environment}?", default=True)
            config_updates[f"{prefix}VERIFY_SSL"] = "true" if verify_ssl else "false"
    
    # Configurações comuns
    language = Prompt.ask(f"Idioma ({environment})", default="EN")
    config_updates[f"{prefix}LANGUAGE"] = language
    
    timeout = Prompt.ask(f"Timeout em segundos ({environment})", default="30")
    config_updates[f"{prefix}TIMEOUT"] = timeout


@config.command("test-sap")
@click.option(
    "--environment",
    type=click.Choice(["DEV", "QAS", "PRD"]),
    help="Ambiente SAP a testar"
)
def test_sap_connection(environment: Optional[str]):
    """Testa conectividade SAP."""
    try:
        if not environment:
            environments = get_sap_environments()
            if not environments:
                console.print("[red]Nenhum ambiente SAP configurado.[/red]")
                console.print("Execute [cyan]abapify config sap[/cyan] para configurar.")
                return
            environment = Prompt.ask(
                "Ambiente SAP para testar",
                choices=environments,
                default=environments[0]
            )
        console.print(f"[cyan]Testando conectividade SAP {environment}...[/cyan]")
        # Importa e testa conexão
        from abapify.sap import SAPConnection
        with console.status(f"[cyan]Conectando ao SAP {environment}...[/cyan]"):
            connection = SAPConnection(environment=environment)
            results = connection.test_connection()
        # Exibe resultados
        table = Table(title=f"Teste de Conectividade SAP {environment}", show_header=True)
        table.add_column("Tipo", style="cyan")
        table.add_column("Status", style="white")
        for conn_type, status in results.items():
            status_text = "[green]✅ Conectado[/green]" if status else "[red]❌ Falhou[/red]"
            table.add_row(conn_type.upper(), status_text)
        console.print(table)
        # Se pelo menos uma conexão funcionou, obtém informações do sistema
        if any(results.values()):
            try:
                with console.status("[cyan]Obtendo informações do sistema...[/cyan]"):
                    system_info = connection.get_system_info()
                console.print(f"\n[bold green]Informações do Sistema SAP {environment}:[/bold green]")
                info_table = Table(show_header=False)
                info_table.add_column("Campo", style="cyan", width=20)
                info_table.add_column("Valor", style="white")
                for key, value in system_info.items():
                    display_key = key.replace('_', ' ').title()
                    info_table.add_row(display_key, str(value))
                console.print(info_table)
            except Exception as e:
                console.print(f"[yellow]Aviso: Não foi possível obter informações do sistema: {str(e)}[/yellow]")
        connection.close()
    except Exception as e:
        logger.error(f"Erro ao testar conexão SAP: {str(e)}")
        console.print(f"[bold red]Erro ao testar conexão SAP:[/] {str(e)}")


@config.command("list-sap-tables")
@click.option(
   "--environment",
   type=click.Choice(["DEV", "QAS", "PRD"]),
   help="Ambiente SAP"
)
@click.option(
   "--pattern",
   default="Z*",
   help="Padrão de busca para tabelas (default: Z*)"
)
@click.option(
   "--limit",
   type=int,
   default=50,
   help="Limite de resultados (default: 50)"
)
def list_sap_tables(environment: Optional[str], pattern: str, limit: int):
   """Lista tabelas customizadas do SAP."""
   try:
       if not environment:
           environments = get_sap_environments()
           if not environments:
               console.print("[red]Nenhum ambiente SAP configurado.[/red]")
               return
           
           environment = environments[0]
       
       console.print(f"[cyan]Buscando tabelas no SAP {environment}...[/cyan]")
       
       from abapify.sap import SAPConnection, MetadataAnalyzer
       
       with console.status(f"[cyan]Conectando e buscando tabelas...[/cyan]"):
           connection = SAPConnection(environment=environment)
           analyzer = MetadataAnalyzer(connection)
           
           tables = analyzer.search_custom_tables(pattern)[:limit]
       
       if tables:
           console.print(f"\n[bold green]Encontradas {len(tables)} tabelas com padrão '{pattern}':[/bold green]")
           
           table = Table(show_header=True)
           table.add_column("Nome da Tabela", style="cyan")
           table.add_column("Tipo", style="yellow")
           
           for table_name in tables:
               table.add_row(table_name, "Customizada")
           
           console.print(table)
       else:
           console.print(f"[yellow]Nenhuma tabela encontrada com padrão '{pattern}'[/yellow]")
       
       connection.close()
       
   except Exception as e:
       logger.error(f"Erro ao listar tabelas SAP: {str(e)}")
       console.print(f"[bold red]Erro ao listar tabelas SAP:[/] {str(e)}")
        