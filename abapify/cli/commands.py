#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementação dos comandos da CLI.
"""

import os
from typing import List, Optional, Tuple

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from abapify.core.generator import AbapGenerator
from abapify.utils.config import get_config_value
from abapify.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


def _ensure_output_dir(output_dir: str) -> None:
    """Garante que o diretório de saída existe."""
    os.makedirs(output_dir, exist_ok=True)


def _save_code(code: str, output_dir: str, filename: str) -> str:
    """Salva o código gerado no arquivo de saída."""
    _ensure_output_dir(output_dir)
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    return file_path


def generate_alv(
    description: str, tables: Tuple[str, ...], output_dir: str, filename: str
) -> None:
    """Gera um relatório ALV."""
    try:
        console.print(f"[bold green]Gerando relatório ALV:[/] {description}")
        
        generator = AbapGenerator()
        code = generator.generate_alv(description, list(tables))
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Código gerado com sucesso:[/] {file_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar relatório ALV: {str(e)}")
        console.print(f"[bold red]Erro ao gerar relatório ALV:[/] {str(e)}")


def generate_report(
    description: str, tables: Tuple[str, ...], output_dir: str, filename: str
) -> None:
    """Gera um relatório ABAP."""
    try:
        console.print(f"[bold green]Gerando relatório ABAP:[/] {description}")
        
        generator = AbapGenerator()
        code = generator.generate_report(description, list(tables))
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Código gerado com sucesso:[/] {file_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar relatório ABAP: {str(e)}")
        console.print(f"[bold red]Erro ao gerar relatório ABAP:[/] {str(e)}")


def generate_class(
    description: str, methods: Tuple[str, ...], output_dir: str, filename: str
) -> None:
    """Gera uma classe ABAP."""
    try:
        console.print(f"[bold green]Gerando classe ABAP:[/] {description}")
        
        generator = AbapGenerator()
        code = generator.generate_class(description, list(methods))
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Código gerado com sucesso:[/] {file_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar classe ABAP: {str(e)}")
        console.print(f"[bold red]Erro ao gerar classe ABAP:[/] {str(e)}")


def generate_function_module(
    description: str, params: Tuple[str, ...], output_dir: str, filename: str
) -> None:
    """Gera um módulo de função ABAP."""
    try:
        console.print(f"[bold green]Gerando módulo de função ABAP:[/] {description}")
        
        generator = AbapGenerator()
        code = generator.generate_function_module(description, list(params))
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Código gerado com sucesso:[/] {file_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar módulo de função ABAP: {str(e)}")
        console.print(f"[bold red]Erro ao gerar módulo de função ABAP:[/] {str(e)}")


def generate_structure(
    description: str, fields: Tuple[str, ...], output_dir: str, filename: str
) -> None:
    """Gera uma estrutura ABAP."""
    try:
        console.print(f"[bold green]Gerando estrutura ABAP:[/] {description}")
        
        generator = AbapGenerator()
        code = generator.generate_structure(description, list(fields))
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Código gerado com sucesso:[/] {file_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar estrutura ABAP: {str(e)}")
        console.print(f"[bold red]Erro ao gerar estrutura ABAP:[/] {str(e)}")


def generate_test(target: str, output_dir: str, filename: str) -> None:
    """Gera um teste unitário ABAP."""
    try:
        console.print(f"[bold green]Gerando teste unitário ABAP:[/] {target}")
        
        generator = AbapGenerator()
        code = generator.generate_test(target)
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Código gerado com sucesso:[/] {file_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar teste unitário ABAP: {str(e)}")
        console.print(f"[bold red]Erro ao gerar teste unitário ABAP:[/] {str(e)}")


def generate_custom_program(output_dir: str, filename: Optional[str] = None) -> None:
    """Gera um programa ABAP customizado com assistente interativo."""
    try:
        console.print(Panel.fit(
            "[bold blue]Assistente de Programa Personalizado[/bold blue]",
            border_style="blue"
        ))
        
        # Coleta informações básicas
        console.print("\n[cyan]Especificação do Programa:[/cyan]")
        specification = Prompt.ask("Descrição detalhada do que o programa deve fazer")
        
        program_type = Prompt.ask(
            "Tipo de programa",
            choices=["Report", "Class", "Function Group", "Interface", "Enhancement"],
            default="Report"
        )
        
        # Funcionalidades principais
        console.print(f"\n[cyan]Funcionalidades Principais:[/cyan]")
        main_features = Prompt.ask("Liste as principais funcionalidades (separadas por vírgula)")
        
        # Entidades envolvidas
        entities = Prompt.ask("Tabelas/Entidades envolvidas (separadas por vírgula)", default="")
        
        # Integrações
        integrations = Prompt.ask("Integrações necessárias (APIs, RFCs, etc.)", default="Nenhuma")
        
        # Regras de negócio
        business_rules = Prompt.ask("Regras de negócio específicas", default="")
        
        # Requisitos avançados (opcional)
        advanced_config = Confirm.ask("\nDeseja configurar requisitos avançados?", default=False)
        
        performance_req = "Padrão"
        security_req = "Verificações de autorização padrão"
        usability_req = "Interface intuitiva"
        
        if advanced_config:
            performance_req = Prompt.ask("Requisitos de performance", default="Padrão")
            security_req = Prompt.ask("Requisitos de segurança", default="Verificações de autorização padrão")
            usability_req = Prompt.ask("Requisitos de usabilidade", default="Interface intuitiva")
        
        # Gera nome do arquivo se não fornecido
        if not filename:
            safe_spec = specification.lower().replace(' ', '_')[:30]
            filename = f"z_custom_{safe_spec}.abap"
        
        # Gera o código
        console.print(f"\n[bold yellow]Gerando programa personalizado...[/bold yellow]")
        
        generator = AbapGenerator()
        code = generator.generate_custom_program(
            specification=specification,
            program_type=program_type,
            main_features=main_features,
            entities=entities,
            integrations=integrations,
            business_rules=business_rules,
            performance_requirements=performance_req,
            security_requirements=security_req,
            usability_requirements=usability_req,
        )
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"\n[bold green]✅ Programa personalizado gerado com sucesso![/]")
        console.print(f"[green]Arquivo:[/] {file_path}")
        
    except Exception as e:
        logger.error(f"Erro ao gerar programa personalizado: {str(e)}")
        console.print(f"[bold red]Erro ao gerar programa personalizado:[/] {str(e)}")


def generate_enhancement(
    base_object: str, 
    enhancement_type: str, 
    functionality: str, 
    output_dir: str, 
    filename: str,
    enhancement_points: str = ""
) -> None:
    """Gera um enhancement ABAP."""
    try:
        console.print(f"[bold green]Gerando enhancement ABAP:[/] {enhancement_type}")
        
        generator = AbapGenerator()
        code = generator.generate_enhancement(
            base_object=base_object,
            enhancement_type=enhancement_type,
            functionality=functionality,
            enhancement_points=enhancement_points,
        )
        
        file_path = _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Código gerado com sucesso:[/] {file_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar enhancement ABAP: {str(e)}")
        console.print(f"[bold red]Erro ao gerar enhancement ABAP:[/] {str(e)}")