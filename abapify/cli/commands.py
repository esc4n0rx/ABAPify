#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementação dos comandos da CLI.
"""

import os
from typing import List, Optional, Tuple

from rich.console import Console

from abapify.core.generator import AbapGenerator
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