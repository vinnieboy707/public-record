"""Public Record API Integration Package

This package provides a unified interface to access various public record APIs
including court records, property records, business registrations, government data,
background checks, and vehicle records.
"""

__version__ = "1.0.0"

from .client import PublicRecordClient
from .apis import (
    CourtRecordsAPI,
    PropertyRecordsAPI,
    BusinessRegistrationAPI,
    GovernmentDataAPI,
    BackgroundCheckAPI,
    VehicleRecordsAPI
)

__all__ = [
    'PublicRecordClient',
    'CourtRecordsAPI',
    'PropertyRecordsAPI',
    'BusinessRegistrationAPI',
    'GovernmentDataAPI',
    'BackgroundCheckAPI',
    'VehicleRecordsAPI'
]
