# GeoDjango Property Management System

A modern vacation rental property management system with geospatial search and AI-powered semantic search.


## Overview
This is a 3-day Django project that implements a vacation rental property management system with:
- Geospatial search (find properties near a location)
- Semantic search (AI-powered search using sentence embeddings)
- Responsive frontend with Bootstrap 5
- Property listing and detail pages
- Admin panel for managing properties and locations

## Tech Stack
- **Backend**: Python 3.12, Django 6.0, Django REST Framework
- **Database**: PostgreSQL 16 with PostGIS (geospatial) and pgvector (vector search)
- **AI**: Sentence Transformers (all-MiniLM-L6-v2)
- **Frontend**: Bootstrap 5
- **Other**: Pandas (CSV import), Pillow (image handling)

## Project Structure
```
md-sourav-geodjango-property-system/
├── core/                          # Django project root
│   ├── __init__.py
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Project URLs
│   └── wsgi.py
├── property_app/                  # Main application
│   ├── __init__.py
│   ├── admin.py                   # Admin configuration
│   ├── api.py                     # API views (autocomplete)
│   ├── embeddings.py              # AI embedding utilities
│   ├── management/
│   │   └── commands/
│   │       ├── import_properties.py    # CSV import command
│   │       ├── generate_location_embeddings.py
│   │       └── generate_property_embeddings.py
│   ├── models.py                  # Database models
│   ├── static/
│   │   └── css/
│   │       └── style.css          # Custom styles
│   ├── templates/
│   │   └── property_app/
│   │       ├── base.html
│   │       ├── homepage.html
│   │       ├── property_list.html
│   │       └── property_detail.html
│   ├── urls.py                    # App URLs
│   └── views.py                   # Django views
├── data/
│   └── sample_properties.csv      # Sample property data
├── media/                         # Uploaded media files (gitignored)
├── Dockerfile.db                  # Database Dockerfile
├── Dockerfile.django              # Django Dockerfile
├── docker-compose.yml             # Docker compose configuration
├── init.sql                       # Database initialization script
├── requirements.txt               # Python dependencies
└── .env.example                   # Environment variables example
```

## Quick Start

### Prerequisites
- Docker Desktop (for Windows/macOS) or Docker Engine (for Linux)
- Git (optional)

### 1. Clone or download the project
```bash
git clone https://github.com/sourav-islam/md-sourav-geodjango-property-system.git
cd md-sourav-geodjango-property-system
```

### 2. Set up environment variables
Copy `.env.example` to `.env` and update values if needed:
```bash
cp .env.example .env
```

### 3. Start Docker containers
```bash
docker-compose up -d --build
```
Wait for the containers to start (this may take a few minutes the first time).

### 4. Run database migrations
```bash
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate
```

### 5. Create a superuser
```bash
docker-compose exec django python manage.py createsuperuser
```

### 6. Import sample properties
```bash
docker-compose exec django python manage.py import_properties data/sample_properties.csv
```

### 7. Generate AI embeddings (for semantic search)
```bash
docker-compose exec django python manage.py generate_location_embeddings
docker-compose exec django python manage.py generate_property_embeddings
```

### 8. Access the application
- **Homepage**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
- **autocomplete API test**: http://localhost:8000/api/locations/autocomplete/


## Day 1: Setup & Data Foundation

### Features Implemented
- Dockerized PostgreSQL database with PostGIS and pgvector
- Django project with property_app
- Database models:
  - Location (name, slug, coordinates, boundary, embedding)
  - Property (location, title, price, bedrooms, amenities, point, etc.)
  - PropertyImage (images linked to properties)
- Django Admin with image previews
- CSV import management command
- Sample property data (21 properties in Bangladesh)

## Day 2: Search & Frontend

### Features Implemented
- Responsive homepage with search form and featured properties
- Property listing page with filters and pagination
- Property detail page with gallery and amenities
- Geospatial search (find properties near a location with radius)
- Filters for property type, price range, bedrooms
- Bootstrap 5 frontend with custom styling

## Day 3: Semantic Search with AI

### Features Implemented
- Sentence Transformers integration (all-MiniLM-L6-v2, 384-dimensional vectors)
- Management commands to generate embeddings for locations and properties
- Location autocomplete API with semantic search
- Enhanced property search with semantic fallback
- Interactive autocomplete with keyboard navigation


## Troubleshooting

### Database connection errors
- Make sure the database container is running: `docker-compose ps`
- Check logs: `docker-compose logs db`
- Restart containers: `docker-compose restart`

### Static files not loading
- Restart Django container: `docker-compose restart django`

### Embedding generation errors
- Make sure the Sentence Transformers model is downloaded (this happens automatically the first time)

### Clean up and reset
```bash
docker-compose down -v  # Deletes all data and volumes
docker-compose up -d --build  # Rebuild and restart
```