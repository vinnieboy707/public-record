"""Base API client for public record APIs."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseAPIClient(ABC):
    """Base class for all public record API clients."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the API client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API endpoint
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests.
        
        Returns:
            Dictionary of headers
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        return headers
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an API request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            Response data as dictionary
            
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = f"{self.base_url}/{endpoint}" if self.base_url else endpoint
        
        response = self.session.request(
            method=method,
            url=url,
            headers=self._get_headers(),
            params=params,
            json=data
        )
        
        response.raise_for_status()
        return response.json()
    
    @abstractmethod
    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search for records.
        
        Args:
            query: Search query
            **kwargs: Additional search parameters
            
        Returns:
            Search results
        """
        pass
    
    @abstractmethod
    def get_record(self, record_id: str) -> Dict[str, Any]:
        """Get a specific record by ID.
        
        Args:
            record_id: Record identifier
            
        Returns:
            Record data
        """
        pass
