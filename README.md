# Public Record

**All public records in one location** - A comprehensive full-stack web application for searching and accessing various public record APIs.

![Public Records Search](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

Public Record is a unified platform that integrates multiple public record APIs into a single, user-friendly interface. Search across court records, property data, business registrations, government datasets, background checks, and vehicle records all in one place.

## Features

### 🔍 **Unified Search Interface**
- Search across multiple record types simultaneously
- Filter by specific record categories
- Clean, intuitive web interface

### 📋 **Integrated Record Types**

1. **Court Records**
   - Federal and state court cases (PACER)
   - CourtListener RECAP Archive
   - Legislation tracking (LegiScan)
   - Case documents and filings

2. **Property Records**
   - Property ownership and tax records
   - Valuations and rent estimates (RentCast)
   - Title information (First American)
   - Comprehensive property analytics (HouseCanary)

3. **Business Registration**
   - Company registrations (OpenCorporates - 200M+ companies)
   - Fresh company data (Coresignal - 70M+ profiles)
   - Company enrichment (The Companies API)
   - Corporate filings and licenses

4. **Government Data**
   - Federal datasets (Data.gov)
   - Census data and demographics
   - Agency-specific information
   - Open government data

5. **Background Checks**
   - Criminal records (Checkr, iDenfy)
   - Employment screening
   - Education verification
   - Continuous monitoring

6. **Vehicle Records**
   - VIN decoding (NHTSA vPIC)
   - Vehicle history (VINData - 1B+ records)
   - DMV verification (IDScan.net)
   - Title information (NMVTIS)

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vinnieboy707/public-record.git
   cd public-record
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   ```
   Open your browser to: http://localhost:5000
   ```

## Configuration

### API Keys

The application supports multiple API providers. Copy `.env.example` to `.env` and configure your API keys:

```env
# Federal Government APIs
DATA_GOV_API_KEY=your_key_here
CENSUS_API_KEY=your_key_here

# Court Records
PACER_USERNAME=your_username
PACER_PASSWORD=your_password
COURTLISTENER_API_KEY=your_key_here
LEGISCAN_API_KEY=your_key_here

# Property Records
BRIDGE_API_KEY=your_key_here
RENTCAST_API_KEY=your_key_here
FIRST_AMERICAN_API_KEY=your_key_here

# Business Records
OPENCORPORATES_API_KEY=your_key_here
CORESIGNAL_API_KEY=your_key_here

# Background Checks
CHECKR_API_KEY=your_key_here
IDENFY_API_KEY=your_key_here

# Vehicle Records
VINDATA_API_KEY=your_key_here
IDSCAN_API_KEY=your_key_here
```

**Note:** The application works in demo mode without API keys, returning mock data. Configure API keys for real data access.

## Usage

### Web Interface

The web interface provides:
- **Unified Search**: Search across all record types with a single query
- **Filtered Search**: Select specific record types to search
- **Quick Access**: Direct links to common search categories
- **API Status**: View which APIs are configured

### API Endpoints

The application provides a RESTful API:

#### Search All Records
```http
POST /api/search
Content-Type: application/json

{
  "query": "search term",
  "record_types": ["all"]
}
```

#### Search Specific Record Type
```http
POST /api/search/court
Content-Type: application/json

{
  "query": "case name",
  "filters": {}
}
```

#### Get Specific Record
```http
GET /api/record/property/12345
```

#### Specialized Endpoints

- `GET /api/vehicle/decode/<vin>` - Decode VIN
- `POST /api/property/address` - Search by address
- `GET /api/business/enrich/<domain>` - Enrich company data
- `GET /api/court/case/<case_id>` - Get court case details

### Python API

Use the client directly in Python:

```python
from src.public_record import PublicRecordClient

# Initialize client
client = PublicRecordClient()

# Search all records
results = client.search_all("John Doe")

# Search specific type
court_results = client.court_records.search("Smith v. Jones")
property_results = client.property_records.get_by_address(
    "123 Main St", "Springfield", "CA"
)

# Decode VIN
vehicle_info = client.vehicle_records.decode_vin("1HGBH41JXMN109186")
```

## Architecture

```
public-record/
├── app.py                      # Flask web application
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment configuration
├── src/
│   └── public_record/         # Core package
│       ├── __init__.py
│       ├── base.py            # Base API client
│       ├── client.py          # Unified client
│       └── apis/              # API implementations
│           ├── court_records.py
│           ├── property_records.py
│           ├── business_registration.py
│           ├── government_data.py
│           ├── background_check.py
│           └── vehicle_records.py
├── templates/
│   └── index.html             # Web interface
└── static/
    ├── css/
    │   └── style.css          # Styles
    └── js/
        └── app.js             # Frontend logic
```

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

#### Environment Variables
```bash
export FLASK_ENV=production
export PORT=5000
```

## API Providers

This application integrates with numerous public record APIs:

- **PACER** - Federal court records
- **CourtListener** - Free PACER data archive
- **LegiScan** - State and federal legislation
- **RentCast** - Property valuations and rentals
- **First American** - Title and property data
- **OpenCorporates** - Global company database
- **Coresignal** - Real-time company data
- **Checkr** - Background checks
- **NHTSA vPIC** - Vehicle information (free)
- **VINData** - Vehicle history
- And many more...

## Legal & Compliance

- **FCRA Compliance**: Required for consumer reports
- **DPPA**: Driver's Privacy Protection Act compliance
- **Data Privacy**: GDPR, CCPA considerations
- **Rate Limiting**: Respect API provider limits
- **Terms of Service**: Review each API provider's terms

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- All public record API providers
- Open data initiatives
- Contributors and maintainers

---

**Disclaimer**: This application is a demonstration of API integration. Always ensure you have proper authorization and comply with all applicable laws and regulations when accessing public records.
