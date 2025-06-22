#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Clientes de conectividade SAP.
"""

try:
    from .rfc_client import RFCClient
    from .http_client import HTTPClient
    
    __all__ = ["RFCClient", "HTTPClient"]
    
except ImportError as e:
    import warnings
    warnings.warn(f"Clientes SAP não puderam ser carregados: {e}")
    
    # Classes básicas para evitar erros
    class RFCClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("Cliente RFC não disponível")
    
    class HTTPClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("Cliente HTTP não disponível")
    
    __all__ = ["RFCClient", "HTTPClient"]