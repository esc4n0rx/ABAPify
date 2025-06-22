#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Templates de prompts específicos para geração de código ABAP.
"""

ALV_PROMPT_TEMPLATE = """
Crie um relatório ABAP com ALV usando Cl_Salv_Table que:

- Descrição: {description}
- Tabelas envolvidas: {tables}

Inclua:
1. Tela de seleção apropriada
2. Lógica de processamento adequada
3. Estrutura de dados para exibição no ALV
4. Configuração completa do ALV (título, cabeçalhos, otimização, etc.)
5. Tratamento de erros

Utilize ABAP moderno e boas práticas de programação SAP.
"""

REPORT_PROMPT_TEMPLATE = """
Crie um programa de relatório ABAP que:

- Descrição: {description}
- Tabelas envolvidas: {tables}

Inclua:
1. Tela de seleção apropriada
2. Lógica de processamento
3. Estrutura do relatório
4. Exibição formatada dos dados
5. Tratamento de erros

Utilize ABAP moderno e boas práticas de programação SAP.
"""

CLASS_PROMPT_TEMPLATE = """
Crie uma classe ABAP que:

- Descrição/Propósito: {description}
- Métodos a implementar: {methods}

Inclua:
1. Declaração completa da classe
2. Atributos necessários
3. Métodos públicos e privados
4. Implementação dos métodos
5. Documentação em formato ABAP Doc
6. Tratamento de exceções

Utilize ABAP moderno e boas práticas de programação SAP, incluindo princípios SOLID.
"""

FUNCTION_MODULE_PROMPT_TEMPLATE = """
Crie um módulo de função ABAP que:

- Descrição/Propósito: {description}
- Parâmetros: {params}

Inclua:
1. Declaração completa do módulo de função
2. Documentação dos parâmetros
3. Implementação da lógica
4. Tratamento de exceções
5. Verificação de parâmetros de entrada

Utilize ABAP moderno e boas práticas de programação SAP.
"""

STRUCTURE_PROMPT_TEMPLATE = """
Crie uma estrutura de dados ABAP que:

- Descrição/Propósito: {description}
- Campos: {fields}

Inclua:
1. Definição da estrutura
2. Tipos de dados apropriados
3. Comentários explicativos
4. Definições relacionadas (constantes, tipos, etc.)

Utilize ABAP moderno e boas práticas de programação SAP.
"""

TEST_PROMPT_TEMPLATE = """
Crie uma classe de teste unitário ABAP para:

- Classe/Módulo de Função a ser testado: {target}

Inclua:
1. Estrutura completa da classe de teste usando ABAP Unit
2. Métodos de configuração (SETUP)
3. Métodos de teste para os principais casos
4. Verificações (asserts) adequadas
5. Limpeza (TEARDOWN)

Utilize ABAP moderno e boas práticas de teste unitário.
"""

CUSTOM_PROGRAM_PROMPT_TEMPLATE = """
Crie um programa ABAP completo baseado no seguinte resumo/especificação:

ESPECIFICAÇÃO DO PROGRAMA:
{specification}

REQUISITOS TÉCNICOS:
- Tipo de programa: {program_type}
- Funcionalidades principais: {main_features}
- Tabelas/Entidades envolvidas: {entities}
- Integrações necessárias: {integrations}
- Regras de negócio específicas: {business_rules}

REQUISITOS NÃO FUNCIONAIS:
- Performance: {performance_requirements}
- Segurança: {security_requirements}
- Usabilidade: {usability_requirements}

Implemente um programa ABAP completo e funcional que atenda a todos os requisitos especificados.
Inclua tela de seleção adequada, lógica de processamento robusta, tratamento de erros, 
logging e documentação apropriada.

O programa deve ser de qualidade produtiva e seguir todas as melhores práticas ABAP.
"""

ENHANCEMENT_PROMPT_TEMPLATE = """
Crie uma melhoria/enhancement ABAP que:

- Objeto base: {base_object}
- Tipo de enhancement: {enhancement_type}
- Funcionalidade a adicionar: {functionality}
- Pontos de enhancement: {enhancement_points}

Inclua:
1. Implementação do enhancement
2. Validações necessárias
3. Tratamento de erros
4. Documentação das alterações
5. Testes de regressão considerados

Utilize técnicas modernas de enhancement (BADIs, Enhancement Points, etc.).
"""