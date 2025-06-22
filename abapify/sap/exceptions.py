#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exceções específicas para integração SAP.
"""

from abapify.utils.exceptions import AbapifyError


class SAPError(AbapifyError):
    """Exceção base para erros relacionados ao SAP."""
    pass


class SAPConnectionError(SAPError):
    """Erro de conectividade com SAP."""
    pass


class SAPAuthenticationError(SAPError):
    """Erro de autenticação SAP."""
    pass


class SAPMetadataError(SAPError):
    """Erro ao obter metadados SAP."""
    pass


class SAPRFCError(SAPError):
    """Erro específico de RFC."""
    
    def __init__(self, message: str, rfc_name: str = None, group: str = None):
        super().__init__(message)
        self.rfc_name = rfc_name
        self.group = group


class SAPHTTPError(SAPError):
    """Erro específico de HTTP/REST."""
    
    def __init__(self, message: str, status_code: int = None, endpoint: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.endpoint = endpoint


class SAPTableNotFoundError(SAPMetadataError):
    """Tabela não encontrada no SAP."""
    
    def __init__(self, table_name: str):
        super().__init__(f"Tabela '{table_name}' não encontrada no SAP")
        self.table_name = table_name


class SAPObjectNotFoundError(SAPMetadataError):
    """Objeto SAP não encontrado."""
    
    def __init__(self, object_name: str, object_type: str = None):
        message = f"Objeto '{object_name}'"
        if object_type:
            message += f" do tipo '{object_type}'"
        message += " não encontrado no SAP"
        super().__init__(message)
        self.object_name = object_name
        self.object_type = object_type