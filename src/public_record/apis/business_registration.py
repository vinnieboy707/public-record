"""Business Registration API client."""

from typing import Dict, Any, Optional
from ..base import BaseAPIClient


class BusinessRegistrationAPI(BaseAPIClient):
    """API client for business registration records.
    
    Integrates multiple business record sources:
    - OpenCorporates: World's largest open database with 200M+ companies
    - Coresignal: Fresh company data from public web with 70M+ profiles
    - The Companies API: Company enrichment with 300+ data points
    - Moody's: Entity verification from 200+ jurisdictions
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        opencorporates_key: Optional[str] = None,
        coresignal_key: Optional[str] = None,
        companies_api_key: Optional[str] = None
    ):
        """Initialize Business Registration API client.
        
        Args:
            api_key: Default API key
            opencorporates_key: OpenCorporates API key
            coresignal_key: Coresignal API key
            companies_api_key: The Companies API key
        """
        super().__init__(api_key=api_key, base_url="https://api.opencorporates.com")
        self.api_type = "business_registration"
        self.opencorporates_key = opencorporates_key
        self.coresignal_key = coresignal_key
        self.coresignal_base_url = "https://api.coresignal.com"
        self.companies_api_key = companies_api_key
        self.companies_base_url = "https://api.thecompaniesapi.com"
    
    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for business registrations.
        
        Args:
            query: Search query (business name, registration number)
            **kwargs: Additional parameters like:
                - state: State abbreviation
                - business_type: Type of business entity (LLC, Corp, etc.)
                - status: Active, Dissolved, etc.
                - industry: Industry classification
                
        Returns:
            Dictionary containing search results with structure:
            {
                'results': [list of matching businesses],
                'total': total count,
                'page': current page
            }
        """
        return {
            'api_type': self.api_type,
            'query': query,
            'filters': kwargs,
            'results': [],
            'total': 0,
            'message': 'Mock implementation. Configure API key to use real data.'
        }
    
    def get_record(self, business_id: str) -> Dict[str, Any]:
        """Get details for a specific business registration.
        
        Args:
            business_id: Business registration identifier (EIN, state ID, etc.)
            
        Returns:
            Dictionary containing business details including:
            - Legal name
            - DBA names
            - Registration date
            - Business type
            - Registered agent
            - Principal address
            - Officers/Directors
            - Status
        """
        return {
            'api_type': self.api_type,
            'business_id': business_id,
            'details': {},
            'message': 'Mock implementation. Configure API key to use real data.'
        }
    
    def get_by_ein(self, ein: str) -> Dict[str, Any]:
        """Get business information by EIN (Employer Identification Number).
        
        Args:
            ein: Employer Identification Number
            
        Returns:
            Dictionary containing business information
        """
        return {
            'api_type': self.api_type,
            'ein': ein,
            'details': {},
            'message': 'Mock implementation. Configure API key to use real data.'
        }
    
    def get_filings(self, business_id: str) -> Dict[str, Any]:
        """Get corporate filings for a business.
        
        Args:
            business_id: Business identifier
            
        Returns:
            Dictionary containing list of filings (annual reports, amendments, etc.)
        """
        return {
            'api_type': self.api_type,
            'business_id': business_id,
            'filings': [],
            'message': 'Mock implementation. Configure API key to use real data.'
        }
    
    def get_licenses(self, business_id: str) -> Dict[str, Any]:
        """Get professional licenses associated with a business.
        
        Args:
            business_id: Business identifier
            
        Returns:
            Dictionary containing list of licenses
        """
        return {
            'api_type': self.api_type,
            'business_id': business_id,
            'licenses': [],
            'message': 'Mock implementation. Configure API key to use real data.'
        }
    
    def search_opencorporates(self, company_name: str, jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        """Search OpenCorporates database.
        
        OpenCorporates has 200M+ companies from global jurisdictions with open data license.
        
        Args:
            company_name: Company name to search
            jurisdiction: Optional jurisdiction code (e.g., 'us_ca', 'gb')
            
        Returns:
            Dictionary containing company search results
        """
        return {
            'api_type': self.api_type,
            'source': 'opencorporates',
            'company_name': company_name,
            'jurisdiction': jurisdiction,
            'base_url': 'https://api.opencorporates.com/v0.4',
            'data_available': [
                'company_name',
                'company_number',
                'jurisdiction',
                'incorporation_date',
                'company_type',
                'registered_address',
                'officers_directors',
                'filing_history'
            ],
            'license': 'CC BY-SA 3.0 or commercial',
            'message': 'Mock implementation. OpenCorporates provides both free and commercial access.'
        }
    
    def enrich_company(self, domain: str) -> Dict[str, Any]:
        """Enrich company data from domain name using The Companies API.
        
        Provides 300+ data points from a single domain name lookup.
        
        Args:
            domain: Company domain (e.g., 'example.com')
            
        Returns:
            Dictionary containing enriched company data
        """
        if not self.companies_api_key:
            return {
                'api_type': self.api_type,
                'source': 'companies_api',
                'message': 'The Companies API key required. Visit https://www.thecompaniesapi.com'
            }
        
        return {
            'api_type': self.api_type,
            'source': 'companies_api',
            'domain': domain,
            'base_url': self.companies_base_url,
            'data_points': '300+',
            'database_size': '50M+ companies',
            'features': [
                'company_enrichment',
                'natural_language_search',
                'industry_filtering',
                'location_search',
                'employee_count_ranges'
            ],
            'message': 'Mock implementation. Configure API key to use real Companies API.'
        }
    
    def search_coresignal(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search Coresignal company database.
        
        Fresh company data from public web with 70M+ profiles and 300+ fields.
        
        Args:
            query: Search query
            **kwargs: Filters like industry, location, headcount, etc.
            
        Returns:
            Dictionary containing company search results
        """
        if not self.coresignal_key:
            return {
                'api_type': self.api_type,
                'source': 'coresignal',
                'message': 'Coresignal API key required. Visit https://coresignal.com'
            }
        
        return {
            'api_type': self.api_type,
            'source': 'coresignal',
            'query': query,
            'filters': kwargs,
            'base_url': self.coresignal_base_url,
            'database_size': '70M+ companies',
            'data_fields': '300+',
            'avg_response_time': '176ms',
            'features': [
                'real_time_data',
                'multi_source_aggregation',
                'ai_enriched_fields',
                'growth_metrics',
                'employee_change_events'
            ],
            'message': 'Mock implementation. Configure API key to use real Coresignal API.'
        }
