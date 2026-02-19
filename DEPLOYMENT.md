# Deployment Guide

This guide provides instructions for deploying the Public Records application in different environments.

## Table of Contents

- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Configuration](#configuration)
- [Monitoring](#monitoring)

## Local Development

### Quick Start

```bash
# Clone the repository
git clone https://github.com/vinnieboy707/public-record.git
cd public-record

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

### Development Mode

Enable debug mode for development:

```bash
export FLASK_DEBUG=True
python app.py
```

## Production Deployment

### Using Gunicorn

Install Gunicorn:
```bash
pip install gunicorn
```

Run with multiple workers:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

For production with logging:
```bash
gunicorn -w 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/public-records/access.log \
  --error-logfile /var/log/public-records/error.log \
  --log-level info \
  app:app
```

### Using systemd (Linux)

Create `/etc/systemd/system/public-records.service`:

```ini
[Unit]
Description=Public Records Web Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/public-record
Environment="PATH=/var/www/public-record/venv/bin"
EnvironmentFile=/var/www/public-record/.env
ExecStart=/var/www/public-record/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable public-records
sudo systemctl start public-records
```

## Docker Deployment

### Build Docker Image

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
# Build image
docker build -t public-records:latest .

# Run container
docker run -d \
  --name public-records \
  -p 5000:5000 \
  --env-file .env \
  public-records:latest
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/var/log/public-records
```

Run with Docker Compose:
```bash
docker-compose up -d
```

## Cloud Deployment

### Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Create `runtime.txt`:
```
python-3.9.18
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku config:set DATA_GOV_API_KEY=your_key_here
heroku open
```

### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init -p python-3.9 public-records
```

3. Create environment:
```bash
eb create public-records-env
```

4. Set environment variables:
```bash
eb setenv DATA_GOV_API_KEY=your_key_here
```

5. Deploy:
```bash
eb deploy
```

### Google Cloud Platform (Cloud Run)

1. Create `Dockerfile` (see Docker section)

2. Build and push:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/public-records
```

3. Deploy:
```bash
gcloud run deploy public-records \
  --image gcr.io/PROJECT_ID/public-records \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

1. Create App Service:
```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name public-records \
  --runtime "PYTHON|3.9"
```

2. Deploy:
```bash
az webapp up --name public-records
```

## Configuration

### Environment Variables

Required environment variables:

```bash
# Application
FLASK_ENV=production
PORT=5000

# API Keys (at least one per category recommended)
DATA_GOV_API_KEY=your_key
CENSUS_API_KEY=your_key
PACER_USERNAME=your_username
PACER_PASSWORD=your_password
COURTLISTENER_API_KEY=your_key
RENTCAST_API_KEY=your_key
OPENCORPORATES_API_KEY=your_key
CHECKR_API_KEY=your_key
VINDATA_API_KEY=your_key
```

### Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/public-record/static;
        expires 30d;
    }
}
```

### HTTPS with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Monitoring

### Health Check

The application provides a health check endpoint:

```bash
curl http://localhost:5000/api/health
```

### Logging

Configure logging in production:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/public-records.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Monitoring Tools

Recommended monitoring solutions:
- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: New Relic, Datadog
- **Error tracking**: Sentry, Rollbar
- **Log management**: Papertrail, Loggly

## Performance Optimization

### Caching

Consider implementing Redis caching for API responses:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@cache.memoize(timeout=300)
def cached_api_call():
    # Your API call here
    pass
```

### Rate Limiting

Implement rate limiting to protect your API:

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["200 per day", "50 per hour"]
)
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **HTTPS**: Always use HTTPS in production
3. **Input Validation**: Validate all user inputs
4. **CORS**: Configure CORS appropriately for your use case
5. **Rate Limiting**: Implement rate limiting to prevent abuse
6. **Security Headers**: Add security headers (CSP, X-Frame-Options, etc.)

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find and kill the process
lsof -i :5000
kill -9 <PID>
```

**Module not found:**
```bash
# Ensure you're in the right directory and virtual environment
pip install -r requirements.txt
```

**API connection errors:**
- Check your internet connection
- Verify API keys are correct
- Check API provider status pages

## Support

For deployment issues or questions:
- Open an issue on GitHub
- Check the README.md for documentation
- Review API provider documentation

## License

MIT License - See LICENSE file for details
