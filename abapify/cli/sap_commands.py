#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comandos específicos para integração SAP.
"""

import json
import os
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from abapify.sap import SAPConnection, MetadataAnalyzer
from abapify.sap.models import SAPAnalysisResult
from abapify.core.generator import AbapGenerator
from abapify.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


def analyze_table_structure(
    table_name: str,
    environment: str = "DEV",
    include_relationships: bool = True,
    output_file: Optional[str] = None
) -> None:
    """
    Analisa estrutura de uma tabela SAP.
    
    Args:
        table_name: Nome da tabela.
        environment: Ambiente SAP.
        include_relationships: Se deve incluir relacionamentos.
        output_file: Arquivo para salvar análise.
    """
    try:
        console.print(f"[bold cyan]Analisando tabela {table_name} no ambiente {environment}[/bold cyan]")
        
        with console.status("[cyan]Conectando ao SAP...[/cyan]"):
            connection = SAPConnection(environment=environment)
            analyzer = MetadataAnalyzer(connection)
        
        with console.status(f"[cyan]Analisando estrutura da tabela {table_name}...[/cyan]"):
            table = analyzer.analyze_table(table_name, include_relationships)
        
        # Exibe informações da tabela
        console.print(f"\n[bold green]Tabela: {table.name}[/bold green]")
        console.print(f"[yellow]Descrição:[/yellow] {table.description}")
        console.print(f"[yellow]Tipo:[/yellow] {table.table_type}")
        console.print(f"[yellow]Classe de Entrega:[/yellow] {table.delivery_class}")
        
        # Tabela de campos
        fields_table = Table(title="Campos da Tabela", show_header=True)
        fields_table.add_column("Campo", style="cyan", width=20)
        fields_table.add_column("Tipo", style="yellow", width=15)
        fields_table.add_column("Tamanho", style="green", width=8)
        fields_table.add_column("Chave", style="red", width=8)
        fields_table.add_column("Descrição", style="white")
        
        for field in table.fields:
            key_indicator = "✓" if field.key_field else ""
            fields_table.add_row(
                field.name,
                field.data_type,
                str(field.length),
                key_indicator,
                field.description
            )
        
        console.print(fields_table)
        
        # Relacionamentos
        if include_relationships and table.foreign_keys:
            console.print(f"\n[bold yellow]Relacionamentos encontrados: {len(table.foreign_keys)}[/bold yellow]")
            for fk in table.foreign_keys:
                console.print(f"  • {fk.get('from_table')} → {fk.get('to_table')}")
        
        # Salva em arquivo se especificado
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(table.dict(), f, indent=2, ensure_ascii=False, default=str)
            console.print(f"\n[green]Análise salva em: {output_file}[/green]")
        
        connection.close()
        
    except Exception as e:
        logger.error(f"Erro ao analisar tabela {table_name}: {str(e)}")
        console.print(f"[bold red]Erro ao analisar tabela:[/] {str(e)}")


def generate_sap_aware_alv(
    description: str,
    tables: List[str],
    output_dir: str,
    filename: str,
    sap_environment: str = "DEV"
) -> None:
    """
    Gera ALV com análise automática de tabelas SAP.
    
    Args:
        description: Descrição do ALV.
        tables: Lista de tabelas.
        output_dir: Diretório de saída.
        filename: Nome do arquivo.
        sap_environment: Ambiente SAP.
    """
    try:
        console.print(f"[bold green]Gerando ALV SAP-aware:[/] {description}")
        
        # Conecta ao SAP e analisa tabelas
        with console.status(f"[cyan]Analisando tabelas no SAP {sap_environment}...[/cyan]"):
            connection = SAPConnection(environment=sap_environment)
            analyzer = MetadataAnalyzer(connection)
            
            # Analisa todas as tabelas
            analyzed_tables = analyzer.analyze_multiple_tables(tables)
            
            # Busca tabelas relacionadas
            related_tables = set()
            for table_name in tables:
                related = analyzer.find_related_tables(table_name, max_depth=1)
                related_tables.update(related)
            
            # Detecta padrões de nomenclatura
            custom_objects = analyzer.analyze_custom_objects("Z*")
            patterns = analyzer.detect_naming_patterns(custom_objects)
        
        # Constrói contexto enriquecido
        context = _build_sap_context(analyzed_tables, list(related_tables), patterns)
        
        # Gera código com contexto SAP
        with console.status("[cyan]Gerando código ABAP otimizado...[/cyan]"):
            generator = AbapGenerator(use_enhanced_prompts=True)
            
            # Prompt enriquecido com contexto SAP
            enriched_prompt = f"""
{description}

CONTEXTO SAP ANALISADO:
{context}

TABELAS PRINCIPAIS: {', '.join(tables)}
TABELAS RELACIONADAS: {', '.join(related_tables) if related_tables else 'Nenhuma'}

Gere um relatório ALV otimizado considerando:
1. Estrutura real das tabelas analisadas
2. Relacionamentos identificados
3. Padrões de nomenclatura da empresa
4. Performance otimizada com JOINs adequados
5. Campos mais relevantes para exibição
"""
            
            code = generator.generate_alv(enriched_prompt, tables)
        
        # Salva código gerado
        _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]ALV SAP-aware gerado com sucesso:[/] {os.path.join(output_dir, filename)}")
        console.print(f"[yellow]Tabelas analisadas:[/] {len(analyzed_tables)}")
        console.print(f"[yellow]Tabelas relacionadas encontradas:[/] {len(related_tables)}")
        
        connection.close()
        
    except Exception as e:
        logger.error(f"Erro ao gerar ALV SAP-aware: {str(e)}")
        console.print(f"[bold red]Erro ao gerar ALV SAP-aware:[/] {str(e)}")


def generate_sap_aware_report(
    description: str,
    tables: List[str],
    output_dir: str,
    filename: str,
    sap_environment: str = "DEV"
) -> None:
    """
    Gera relatório com análise automática de tabelas SAP.
    
    Args:
        description: Descrição do relatório.
        tables: Lista de tabelas.
        output_dir: Diretório de saída.
        filename: Nome do arquivo.
        sap_environment: Ambiente SAP.
    """
    try:
        console.print(f"[bold green]Gerando relatório SAP-aware:[/] {description}")
        
        # Conecta ao SAP e analisa tabelas
        with console.status(f"[cyan]Analisando tabelas no SAP {sap_environment}...[/cyan]"):
            connection = SAPConnection(environment=sap_environment)
            analyzer = MetadataAnalyzer(connection)
            
            # Gera análise completa
            analysis_result = analyzer.generate_full_analysis(tables, include_custom_objects=True)
        
        # Constrói contexto enriquecido
        context = _build_comprehensive_sap_context(analysis_result)
        
        # Gera código com contexto SAP
        with console.status("[cyan]Gerando código ABAP otimizado...[/cyan]"):
            generator = AbapGenerator(use_enhanced_prompts=True)
            
            # Prompt enriquecido com análise completa
            enriched_prompt = f"""
{description}

ANÁLISE SAP COMPLETA:
{context}

Gere um relatório ABAP completo considerando:
1. Estrutura detalhada das tabelas
2. Todos os relacionamentos mapeados
3. Padrões de desenvolvimento da empresa
4. Objetos customizados similares existentes
5. Performance e boas práticas SAP
"""
            
            code = generator.generate_report(enriched_prompt, tables)
        
        # Salva código gerado
        _save_code(code, output_dir, filename)
        
        console.print(f"[bold green]Relatório SAP-aware gerado:[/] {os.path.join(output_dir, filename)}")
        _display_analysis_summary(analysis_result)
        
        connection.close()
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatório SAP-aware: {str(e)}")
        console.print(f"[bold red]Erro ao gerar relatório SAP-aware:[/] {str(e)}")


def generate_sap_aware_code(
    code_type: str,
    description: str,
    tables: List[str],
    output_dir: str,
    filename: Optional[str],
    sap_environment: str = "DEV"
) -> None:
    """
    Gera código ABAP com análise SAP automática.
    
    Args:
        code_type: Tipo de código (alv, report, class).
        description: Descrição do código.
        tables: Lista de tabelas.
        output_dir: Diretório de saída.
        filename: Nome do arquivo.
        sap_environment: Ambiente SAP.
    """
    if not filename:
        filename = f"z_{code_type}_{description.lower().replace(' ', '_')[:20]}.abap"
    
    if code_type == "alv":
        generate_sap_aware_alv(description, tables, output_dir, filename, sap_environment)
    elif code_type == "report":
        generate_sap_aware_report(description, tables, output_dir, filename, sap_environment)
    else:
        console.print(f"[red]Tipo de código não suportado para geração SAP-aware: {code_type}[/red]")


def _build_sap_context(analyzed_tables, related_tables, patterns) -> str:
    """Constrói contexto SAP para o prompt."""
    context_parts = []
    
    # Informações das tabelas
    if analyzed_tables:
        context_parts.append("ESTRUTURAS DE TABELAS:")
        for table in analyzed_tables:
            context_parts.append(f"Tabela {table.name}:")
            context_parts.append(f"  - Descrição: {table.description}")
            context_parts.append(f"  - Campos principais: {', '.join([f.name for f in table.fields[:10]])}")
            context_parts.append(f"  - Campos chave: {', '.join([f.name for f in table.fields if f.key_field])}")
        context_parts.append("")
    
    # Tabelas relacionadas
    if related_tables:
        context_parts.append(f"TABELAS RELACIONADAS: {', '.join(related_tables)}")
        context_parts.append("")
    
    # Padrões de nomenclatura
    if patterns.get('prefixes'):
        top_prefixes = sorted(patterns['prefixes'].items(), key=lambda x: x[1], reverse=True)[:3]
        context_parts.append(f"PADRÕES DE NOMENCLATURA: {', '.join([f'{p[0]} ({p[1]}x)' for p in top_prefixes])}")
        context_parts.append("")
    
    return "\n".join(context_parts)


def _build_comprehensive_sap_context(analysis_result: SAPAnalysisResult) -> str:
    """Constrói contexto SAP abrangente."""
    context_parts = []
    
    # Resumo da análise
    context_parts.append("RESUMO DA ANÁLISE:")
    context_parts.append(f"- Tabelas analisadas: {len(analysis_result.tables)}")
    context_parts.append(f"- Relacionamentos: {len(analysis_result.relationships)}")
    context_parts.append(f"- Objetos customizados: {len(analysis_result.custom_objects)}")
    context_parts.append("")
    
    # Detalhes das tabelas
    context_parts.append("DETALHES DAS TABELAS:")
    for table in analysis_result.tables:
        context_parts.append(f"Tabela {table.name} ({table.description}):")
        key_fields = [f.name for f in table.fields if f.key_field]
        important_fields = [f.name for f in table.fields if not f.key_field][:5]
        context_parts.append(f"  - Chaves: {', '.join(key_fields)}")
        context_parts.append(f"  - Campos importantes: {', '.join(important_fields)}")
    context_parts.append("")
    
    # Relacionamentos
    if analysis_result.relationships:
        context_parts.append("RELACIONAMENTOS IDENTIFICADOS:")
        for rel in analysis_result.relationships[:10]:  # Limita a 10 para não sobrecarregar
            context_parts.append(f"- {rel.from_table} → {rel.to_table} ({rel.relationship_type})")
        context_parts.append("")
    
    # Padrões detectados
    if analysis_result.patterns:
        context_parts.append("PADRÕES DA EMPRESA:")
        if 'prefixes' in analysis_result.patterns:
            top_prefixes = sorted(analysis_result.patterns['prefixes'].items(), 
                                key=lambda x: x[1], reverse=True)[:3]
            context_parts.append(f"- Prefixos comuns: {', '.join([f'{p[0]} ({p[1]}x)' for p in top_prefixes])}")
        
        if 'package_patterns' in analysis_result.patterns:
            packages = list(analysis_result.patterns['package_patterns'].keys())[:5]
            context_parts.append(f"- Pacotes utilizados: {', '.join(packages)}")
        context_parts.append("")
    
    return "\n".join(context_parts)


def _save_code(code: str, output_dir: str, filename: str) -> str:
        """Salva código gerado."""
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        
        return file_path


def _display_analysis_summary(analysis_result: SAPAnalysisResult) -> None:
        """Exibe resumo da análise SAP."""
        summary_table = Table(title="Resumo da Análise SAP", show_header=True)
        summary_table.add_column("Métrica", style="cyan")
        summary_table.add_column("Valor", style="white")
        
        summary_table.add_row("Tabelas analisadas", str(len(analysis_result.tables)))
        summary_table.add_row("Relacionamentos", str(len(analysis_result.relationships)))
        summary_table.add_row("Objetos customizados", str(len(analysis_result.custom_objects)))
        summary_table.add_row("Timestamp", analysis_result.analysis_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        
        console.print(summary_table)