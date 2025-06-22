#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelos de dados para integração SAP.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class SAPConnectionConfig(BaseModel):
    """Configuração de conexão SAP."""
    
    # RFC Connection
    ashost: Optional[str] = Field(None, description="Application server host")
    sysnr: Optional[str] = Field(None, description="System number")
    client: Optional[str] = Field(None, description="Client")
    user: Optional[str] = Field(None, description="Username")
    passwd: Optional[str] = Field(None, description="Password")
    saprouter: Optional[str] = Field(None, description="SAP Router")
    mshost: Optional[str] = Field(None, description="Message server host")
    msserv: Optional[str] = Field(None, description="Message server service")
    group: Optional[str] = Field(None, description="Logon group")
    
    # HTTP/REST Connection
    base_url: Optional[str] = Field(None, description="Base URL para APIs SAP")
    use_ssl: bool = Field(True, description="Usar SSL/HTTPS")
    verify_ssl: bool = Field(True, description="Verificar certificado SSL")
    timeout: int = Field(30, description="Timeout em segundos")
    
    # Common
    language: str = Field("EN", description="Language")
    connection_type: str = Field("RFC", description="Tipo de conexão: RFC ou HTTP")


class SAPTableField(BaseModel):
    """Campo de tabela SAP."""
    
    name: str = Field(..., description="Nome do campo")
    data_type: str = Field(..., description="Tipo de dados ABAP")
    length: int = Field(..., description="Comprimento do campo")
    decimals: int = Field(0, description="Casas decimais")
    description: str = Field("", description="Descrição do campo")
    key_field: bool = Field(False, description="Se é campo chave")
    not_null: bool = Field(False, description="Se não permite nulo")
    domain: Optional[str] = Field(None, description="Domínio SAP")
    data_element: Optional[str] = Field(None, description="Elemento de dados")


class SAPTable(BaseModel):
    """Estrutura de tabela SAP."""
    
    name: str = Field(..., description="Nome da tabela")
    description: str = Field("", description="Descrição da tabela")
    table_type: str = Field("TRANSP", description="Tipo da tabela")
    delivery_class: str = Field("A", description="Classe de entrega")
    fields: List[SAPTableField] = Field(default_factory=list, description="Campos da tabela")
    foreign_keys: List[Dict[str, Any]] = Field(default_factory=list, description="Chaves estrangeiras")
    indexes: List[Dict[str, Any]] = Field(default_factory=list, description="Índices")
    created_on: Optional[datetime] = Field(None, description="Data de criação")
    changed_on: Optional[datetime] = Field(None, description="Data de alteração")


class SAPObject(BaseModel):
    """Objeto SAP genérico."""
    
    name: str = Field(..., description="Nome do objeto")
    object_type: str = Field(..., description="Tipo do objeto (PROG, CLAS, FUGR, etc.)")
    description: str = Field("", description="Descrição do objeto")
    package: Optional[str] = Field(None, description="Pacote")
    author: Optional[str] = Field(None, description="Autor")
    created_on: Optional[datetime] = Field(None, description="Data de criação")
    changed_on: Optional[datetime] = Field(None, description="Data de alteração")
    status: Optional[str] = Field(None, description="Status do objeto")
    
    
class SAPRelationship(BaseModel):
    """Relacionamento entre tabelas SAP."""
    
    from_table: str = Field(..., description="Tabela origem")
    to_table: str = Field(..., description="Tabela destino")
    from_fields: List[str] = Field(..., description="Campos origem")
    to_fields: List[str] = Field(..., description="Campos destino")
    relationship_type: str = Field(..., description="Tipo de relacionamento")
    cardinality: str = Field("1:N", description="Cardinalidade")


class SAPAnalysisResult(BaseModel):
    """Resultado de análise SAP."""
    
    tables: List[SAPTable] = Field(default_factory=list, description="Tabelas analisadas")
    relationships: List[SAPRelationship] = Field(default_factory=list, description="Relacionamentos")
    custom_objects: List[SAPObject] = Field(default_factory=list, description="Objetos customizados")
    patterns: Dict[str, Any] = Field(default_factory=dict, description="Padrões identificados")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da análise")