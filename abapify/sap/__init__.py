#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de integração SAP para ABAPify.
Fornece conectividade e análise de metadados SAP.
"""

try:
    from .connection import SAPConnection
    from .metadata_analyzer import MetadataAnalyzer
    from .auth import SAPAuthenticator
    from .exceptions import (
        SAPConnectionError,
        SAPAuthenticationError,
        SAPMetadataError,
        SAPRFCError,
        SAPHTTPError,
    )
    
    __all__ = [
        "SAPConnection",
        "MetadataAnalyzer", 
        "SAPAuthenticator",
        "SAPConnectionError",
        "SAPAuthenticationError",
        "SAPMetadataError",
        "SAPRFCError",
        "SAPHTTPError",
    ]
    
except ImportError as e:
    # Se algum módulo não existe, define versões básicas
    import warnings
    warnings.warn(f"Alguns módulos SAP não puderam ser carregados: {e}")
    
    # Define classes básicas para evitar erros de import
    class SAPConnection:
        def __init__(self, *args, **kwargs):
            raise ImportError("Módulo SAP não configurado corretamente")
    
    class MetadataAnalyzer:
        def __init__(self, *args, **kwargs):
            raise ImportError("Módulo SAP não configurado corretamente")
    
    class SAPAuthenticator:
        def __init__(self, *args, **kwargs):
            raise ImportError("Módulo SAP não configurado corretamente")
    
    # Exceções básicas
    class SAPError(Exception):
        pass
    
    SAPConnectionError = SAPError
    SAPAuthenticationError = SAPError
    SAPMetadataError = SAPError
    SAPRFCError = SAPError
    SAPHTTPError = SAPError
    
    __all__ = [
        "SAPConnection",
        "MetadataAnalyzer", 
        "SAPAuthenticator",
        "SAPConnectionError",
        "SAPAuthenticationError",
        "SAPMetadataError",
        "SAPRFCError",
        "SAPHTTPError",
    ]

__version__ = "1.0.0"