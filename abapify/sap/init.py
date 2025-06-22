#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de integração SAP para ABAPify.
Fornece conectividade e análise de metadados SAP.
"""

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

__version__ = "1.0.0"