"""Public Record API Integration Package

This package provides a unified interface to access various public record APIs
including court records, property records, business registrations, and government data.
"""

__version__ = "1.0.0"

from .client import PublicRecordClient
from .apis import (
    CourtRecordsAPI,
    PropertyRecordsAPI,
    BusinessRegistrationAPI,
    GovernmentDataAPI
)

__all__ = [
    'PublicRecordClient',
    'CourtRecordsAPI',
    'PropertyRecordsAPI',
    'BusinessRegistrationAPI',
    'GovernmentDataAPI'
]
