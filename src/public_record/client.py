"""Unified Public Record API Client."""

from typing import Dict, Any, Optional, List
import os
from dotenv import load_dotenv

from .apis import (
    CourtRecordsAPI,
    PropertyRecordsAPI,
    BusinessRegistrationAPI,
    GovernmentDataAPI,
    BackgroundCheckAPI,
    VehicleRecordsAPI
)


class PublicRecordClient:
    """Unified client for accessing all public record APIs."""
    
    def __init__(self, load_env: bool = True):
        """Initialize the unified public record client.
        
        Args:
            load_env: Whether to load API keys from .env file
        """
        if load_env:
            load_dotenv()
        
        # Initialize Court Records API
        self.court_records = CourtRecordsAPI(
            api_key=os.getenv('UNICOURT_API_KEY'),
            pacer_username=os.getenv('PACER_USERNAME'),
            pacer_password=os.getenv('PACER_PASSWORD'),
            courtlistener_token=os.getenv('COURTLISTENER_API_KEY'),
            legiscan_key=os.getenv('LEGISCAN_API_KEY')
        )
        
        # Initialize Property Records API
        self.property_records = PropertyRecordsAPI(
            api_key=os.getenv('BRIDGE_API_KEY'),
            bridge_key=os.getenv('BRIDGE_API_KEY'),
            first_american_key=os.getenv('FIRST_AMERICAN_API_KEY'),
            rentcast_key=os.getenv('RENTCAST_API_KEY'),
            housecanary_key=os.getenv('HOUSECANARY_API_KEY')
        )
        
        # Initialize Business Registration API
        self.business_registration = BusinessRegistrationAPI(
            api_key=os.getenv('OPENCORPORATES_API_KEY'),
            opencorporates_key=os.getenv('OPENCORPORATES_API_KEY'),
            coresignal_key=os.getenv('CORESIGNAL_API_KEY'),
            companies_api_key=os.getenv('COMPANIES_API_KEY')
        )
        
        # Initialize Government Data API
        self.government_data = GovernmentDataAPI(
            api_key=os.getenv('DATA_GOV_API_KEY')
        )
        
        # Initialize Background Check API
        self.background_check = BackgroundCheckAPI(
            api_key=os.getenv('CHECKR_API_KEY'),
            checkr_key=os.getenv('CHECKR_API_KEY'),
            gridlines_key=os.getenv('GRIDLINES_API_KEY'),
            idenfy_key=os.getenv('IDENFY_API_KEY')
        )
        
        # Initialize Vehicle Records API
        self.vehicle_records = VehicleRecordsAPI(
            api_key=os.getenv('NHTSA_API_KEY'),
            vindata_key=os.getenv('VINDATA_API_KEY'),
            idscan_key=os.getenv('IDSCAN_API_KEY')
        )
    
    def search_all(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search across all public record APIs.
        
        Args:
            query: Search query
            **kwargs: Additional search parameters
            
        Returns:
            Dictionary containing results from all APIs
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
        
        # Search background checks
        try:
            results['background_check'] = self.background_check.search(query, **kwargs)
        except Exception as e:
            results['background_check'] = {'error': str(e)}
        
        # Search vehicle records
        try:
            results['vehicle_records'] = self.vehicle_records.search(query, **kwargs)
        except Exception as e:
            results['vehicle_records'] = {'error': str(e)}
        
        return results
    
    def search_by_type(self, record_type: str, query: str, **kwargs) -> Dict[str, Any]:
        """Search a specific type of public record.
        
        Args:
            record_type: Type of record
            query: Search query
            **kwargs: Additional search parameters
            
        Returns:
            Search results for the specified record type
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
        elif record_type in ['background', 'background_check']:
            return self.background_check.search(query, **kwargs)
        elif record_type in ['vehicle', 'vehicle_records']:
            return self.vehicle_records.search(query, **kwargs)
        else:
            raise ValueError(
                f"Invalid record type: {record_type}. "
                f"Valid types: court, property, business, government, background, vehicle"
            )
    
    def get_record_by_type(self, record_type: str, record_id: str) -> Dict[str, Any]:
        """Get a specific record by type and ID.
        
        Args:
            record_type: Type of record
            record_id: Record identifier
            
        Returns:
            Record details
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
        elif record_type in ['background', 'background_check']:
            return self.background_check.get_record(record_id)
        elif record_type in ['vehicle', 'vehicle_records']:
            return self.vehicle_records.get_record(record_id)
        else:
            raise ValueError(
                f"Invalid record type: {record_type}. "
                f"Valid types: court, property, business, government, background, vehicle"
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
            'government_data',
            'background_check',
            'vehicle_records'
        ]
    
    def get_api_status(self) -> Dict[str, bool]:
        """Check which APIs have valid API keys configured.
        
        Returns:
            Dictionary mapping API types to configuration status
        """
        return {
            'court_records': bool(os.getenv('UNICOURT_API_KEY') or os.getenv('PACER_USERNAME')),
            'property_records': bool(os.getenv('BRIDGE_API_KEY') or os.getenv('RENTCAST_API_KEY')),
            'business_registration': bool(os.getenv('OPENCORPORATES_API_KEY') or os.getenv('CORESIGNAL_API_KEY')),
            'government_data': bool(os.getenv('DATA_GOV_API_KEY')),
            'background_check': bool(os.getenv('CHECKR_API_KEY') or os.getenv('IDENFY_API_KEY')),
            'vehicle_records': bool(os.getenv('VINDATA_API_KEY') or os.getenv('IDSCAN_API_KEY'))
        }
