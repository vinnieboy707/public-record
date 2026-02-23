#!/usr/bin/env python
"""
Example usage script for the Public Records API.

This script demonstrates how to use the Public Record client
to search across different types of public records.
"""

from src.public_record import PublicRecordClient


def main():
    """Main example function."""
    
    print("=" * 60)
    print("Public Records API - Example Usage")
    print("=" * 60)
    print()
    
    # Initialize the client
    print("Initializing client...")
    client = PublicRecordClient(load_env=False)
    print("✓ Client initialized\n")
    
    # Example 1: Search all record types
    print("Example 1: Search All Record Types")
    print("-" * 60)
    query = "John Doe"
    print(f"Searching for: '{query}' across all record types")
    results = client.search_all(query)
    print(f"✓ Found results from {len(results)} record types")
    for record_type, result in results.items():
        print(f"  - {record_type}: {result.get('message', 'OK')[:50]}...")
    print()
    
    # Example 2: Search court records
    print("Example 2: Search Court Records")
    print("-" * 60)
    case_query = "Smith v. Jones"
    print(f"Searching court records for: '{case_query}'")
    court_results = client.court_records.search(case_query)
    print(f"✓ API Type: {court_results.get('api_type')}")
    print(f"✓ Total Results: {court_results.get('total', 0)}")
    print()
    
    # Example 3: Search property by address
    print("Example 3: Search Property Records")
    print("-" * 60)
    address = "123 Main St"
    city = "Springfield"
    state = "CA"
    print(f"Searching property: {address}, {city}, {state}")
    property_results = client.property_records.get_by_address(
        address, city, state
    )
    print(f"✓ API Type: {property_results.get('api_type')}")
    print()
    
    # Example 4: Decode VIN
    print("Example 4: Decode Vehicle VIN")
    print("-" * 60)
    vin = "1HGBH41JXMN109186"
    print(f"Decoding VIN: {vin}")
    vin_results = client.vehicle_records.decode_vin(vin)
    print(f"✓ Source: {vin_results.get('source')}")
    print(f"✓ Data Available: {len(vin_results.get('data_available', []))} fields")
    print()
    
    # Example 5: Search business records
    print("Example 5: Search Business Records")
    print("-" * 60)
    company = "Acme Corporation"
    print(f"Searching for: '{company}'")
    business_results = client.business_registration.search(company)
    print(f"✓ API Type: {business_results.get('api_type')}")
    print()
    
    # Example 6: Get property valuation
    print("Example 6: Get Property Valuation (RentCast)")
    print("-" * 60)
    address = "456 Oak Avenue"
    print(f"Getting valuation for: {address}")
    valuation = client.property_records.get_rentcast_valuation(address)
    print(f"✓ Source: {valuation.get('source')}")
    if 'data_available' in valuation:
        print(f"✓ Available Data: {', '.join(valuation['data_available'][:3])}...")
    print()
    
    # Example 7: Search legislation
    print("Example 7: Search Legislation (LegiScan)")
    print("-" * 60)
    bill_text = "healthcare reform"
    state = "CA"
    print(f"Searching legislation: '{bill_text}' in {state}")
    legislation = client.court_records.search_legislation(bill_text, state)
    print(f"✓ Source: {legislation.get('source')}")
    print()
    
    # Example 8: Check API status
    print("Example 8: Check API Configuration Status")
    print("-" * 60)
    status = client.get_api_status()
    print("API Configuration Status:")
    for api_name, is_configured in status.items():
        status_icon = "✓" if is_configured else "✗"
        status_text = "Configured" if is_configured else "Not Configured"
        print(f"  {status_icon} {api_name}: {status_text}")
    print()
    
    # Example 9: Get available APIs
    print("Example 9: List Available APIs")
    print("-" * 60)
    available_apis = client.get_available_apis()
    print(f"Available record types ({len(available_apis)}):")
    for api in available_apis:
        print(f"  - {api}")
    print()
    
    print("=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)
    print()
    print("Note: These examples use mock data in demo mode.")
    print("Configure API keys in .env file to access real data.")
    print()
    print("For more information, see README.md")


if __name__ == "__main__":
    main()
