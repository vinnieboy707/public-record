"""Flask web application for Public Records search."""

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from src.public_record import PublicRecordClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

# Initialize Public Record Client
client = PublicRecordClient(load_env=True)


@app.route('/')
def index():
    """Render the main search interface."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """Unified search endpoint across all public record types.
    
    Request body:
    {
        "query": "search term",
        "record_types": ["court", "property", "business", "government", "background", "vehicle"],
        "filters": {optional filters}
    }
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        record_types = data.get('record_types', ['all'])
        filters = data.get('filters', {})
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        results = {}
        
        # Search all record types if 'all' is specified
        if 'all' in record_types:
            results = client.search_all(query, **filters)
        else:
            # Search specific record types
            for record_type in record_types:
                try:
                    results[record_type] = client.search_by_type(
                        record_type, query, **filters
                    )
                except Exception as e:
                    results[record_type] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/search/<record_type>', methods=['POST'])
def search_by_type(record_type):
    """Search a specific record type.
    
    Args:
        record_type: Type of record (court, property, business, etc.)
    
    Request body:
    {
        "query": "search term",
        "filters": {optional filters}
    }
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        filters = data.get('filters', {})
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        result = client.search_by_type(record_type, query, **filters)
        
        return jsonify({
            'success': True,
            'record_type': record_type,
            'query': query,
            'result': result
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/record/<record_type>/<record_id>', methods=['GET'])
def get_record(record_type, record_id):
    """Get a specific record by type and ID.
    
    Args:
        record_type: Type of record
        record_id: Record identifier
    """
    try:
        result = client.get_record_by_type(record_type, record_id)
        
        return jsonify({
            'success': True,
            'record_type': record_type,
            'record_id': record_id,
            'result': result
        })
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/types', methods=['GET'])
def get_record_types():
    """Get available record types."""
    return jsonify({
        'success': True,
        'record_types': client.get_available_apis()
    })


@app.route('/api/status', methods=['GET'])
def get_api_status():
    """Get API configuration status."""
    return jsonify({
        'success': True,
        'status': client.get_api_status()
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'service': 'Public Records API'
    })


# Court Records specific endpoints
@app.route('/api/court/case/<case_id>', methods=['GET'])
def get_court_case(case_id):
    """Get court case details."""
    result = client.court_records.get_record(case_id)
    return jsonify({'success': True, 'result': result})


@app.route('/api/court/documents/<case_id>', methods=['GET'])
def get_case_documents(case_id):
    """Get documents for a court case."""
    result = client.court_records.get_case_documents(case_id)
    return jsonify({'success': True, 'result': result})


# Property Records specific endpoints
@app.route('/api/property/address', methods=['POST'])
def search_property_by_address():
    """Search property by address."""
    data = request.get_json()
    address = data.get('address', '')
    city = data.get('city', '')
    state = data.get('state', '')
    
    result = client.property_records.get_by_address(address, city, state)
    return jsonify({'success': True, 'result': result})


@app.route('/api/property/valuation', methods=['POST'])
def get_property_valuation():
    """Get property valuation."""
    data = request.get_json()
    address = data.get('address', '')
    
    result = client.property_records.get_rentcast_valuation(address, **data)
    return jsonify({'success': True, 'result': result})


# Business Records specific endpoints
@app.route('/api/business/enrich/<domain>', methods=['GET'])
def enrich_company(domain):
    """Enrich company data from domain."""
    result = client.business_registration.enrich_company(domain)
    return jsonify({'success': True, 'result': result})


# Vehicle Records specific endpoints
@app.route('/api/vehicle/decode/<vin>', methods=['GET'])
def decode_vin(vin):
    """Decode VIN."""
    result = client.vehicle_records.decode_vin(vin)
    return jsonify({'success': True, 'result': result})


@app.route('/api/vehicle/history/<vin>', methods=['GET'])
def get_vehicle_history(vin):
    """Get vehicle history."""
    result = client.vehicle_records.get_vehicle_history(vin)
    return jsonify({'success': True, 'result': result})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
