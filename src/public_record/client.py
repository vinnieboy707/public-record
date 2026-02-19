"""Unified Public Record API Client."""

from typing import Dict, Any, Optional, List
import os
from dotenv import load_dotenv

from .apis import (
    CourtRecordsAPI,
    PropertyRecordsAPI,
    BusinessRegistrationAPI,
    GovernmentDataAPI
)


class PublicRecordClient:
    """Unified client for accessing all public record APIs."""
    
    def __init__(
        self,
        court_api_key: Optional[str] = None,
        property_api_key: Optional[str] = None,
        business_api_key: Optional[str] = None,
        government_api_key: Optional[str] = None,
        load_env: bool = True
    ):
        """Initialize the unified public record client.
        
        Args:
            court_api_key: API key for court records
            property_api_key: API key for property records
            business_api_key: API key for business registrations
            government_api_key: API key for government data
            load_env: Whether to load API keys from .env file
        """
        if load_env:
            load_dotenv()
        
        # Initialize API keys from parameters or environment variables
        self.court_api_key = court_api_key or os.getenv('UNICOURT_API_KEY')
        self.property_api_key = property_api_key or os.getenv('PROPMIX_API_KEY')
        self.business_api_key = business_api_key or os.getenv('BUSINESS_API_KEY')
        self.government_api_key = government_api_key or os.getenv('DATA_GOV_API_KEY')
        
        # Initialize API clients
        self.court_records = CourtRecordsAPI(api_key=self.court_api_key)
        self.property_records = PropertyRecordsAPI(api_key=self.property_api_key)
        self.business_registration = BusinessRegistrationAPI(api_key=self.business_api_key)
        self.government_data = GovernmentDataAPI(api_key=self.government_api_key)
    
    def search_all(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search across all public record APIs.
        
        Args:
            query: Search query
            **kwargs: Additional search parameters
            
        Returns:
            Dictionary containing results from all APIs:
            {
                'court_records': {...},
                'property_records': {...},
                'business_registration': {...},
                'government_data': {...}
            }
        """
        results = {}
        
        # Search court records
        try:
            results['court_records'] = self.court_records.search(query, **kwargs)
        except Exception as e:
            results['court_records'] = {'error': str(e)}
        
        # Search property records
        try:
            results['property_records'] = self.property_records.search(query, **kwargs)
        except Exception as e:
            results['property_records'] = {'error': str(e)}
        
        # Search business registrations
        try:
            results['business_registration'] = self.business_registration.search(query, **kwargs)
        except Exception as e:
            results['business_registration'] = {'error': str(e)}
        
        # Search government data
        try:
            results['government_data'] = self.government_data.search(query, **kwargs)
        except Exception as e:
            results['government_data'] = {'error': str(e)}
        
        return results
    
    def search_by_type(self, record_type: str, query: str, **kwargs) -> Dict[str, Any]:
        """Search a specific type of public record.
        
        Args:
            record_type: Type of record ('court', 'property', 'business', 'government')
            query: Search query
            **kwargs: Additional search parameters
            
        Returns:
            Search results for the specified record type
            
        Raises:
            ValueError: If record_type is not valid
        """
        record_type = record_type.lower()
        
        if record_type in ['court', 'court_records']:
            return self.court_records.search(query, **kwargs)
        elif record_type in ['property', 'property_records']:
            return self.property_records.search(query, **kwargs)
        elif record_type in ['business', 'business_registration']:
            return self.business_registration.search(query, **kwargs)
        elif record_type in ['government', 'government_data']:
            return self.government_data.search(query, **kwargs)
        else:
            raise ValueError(
                f"Invalid record type: {record_type}. "
                f"Valid types: court, property, business, government"
            )
    
    def get_record_by_type(self, record_type: str, record_id: str) -> Dict[str, Any]:
        """Get a specific record by type and ID.
        
        Args:
            record_type: Type of record ('court', 'property', 'business', 'government')
            record_id: Record identifier
            
        Returns:
            Record details
            
        Raises:
            ValueError: If record_type is not valid
        """
        record_type = record_type.lower()
        
        if record_type in ['court', 'court_records']:
            return self.court_records.get_record(record_id)
        elif record_type in ['property', 'property_records']:
            return self.property_records.get_record(record_id)
        elif record_type in ['business', 'business_registration']:
            return self.business_registration.get_record(record_id)
        elif record_type in ['government', 'government_data']:
            return self.government_data.get_record(record_id)
        else:
            raise ValueError(
                f"Invalid record type: {record_type}. "
                f"Valid types: court, property, business, government"
            )
    
    def get_available_apis(self) -> List[str]:
        """Get list of available API types.
        
        Returns:
            List of API type names
        """
        return [
            'court_records',
            'property_records',
            'business_registration',
            'government_data'
        ]
    
    def get_api_status(self) -> Dict[str, bool]:
        """Check which APIs have valid API keys configured.
        
        Returns:
            Dictionary mapping API types to configuration status
        """
        return {
            'court_records': bool(self.court_api_key),
            'property_records': bool(self.property_api_key),
            'business_registration': bool(self.business_api_key),
            'government_data': bool(self.government_api_key)
        }
