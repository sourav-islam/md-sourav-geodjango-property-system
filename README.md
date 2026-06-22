# GeoDjango Property Management System

A vacation rental property management system with geospatial search and AI-powered semantic search.

## Day 1: Setup & Data Foundation

### Docker Setup
The project uses Docker to run PostgreSQL with PostGIS and pgvector.

#### Running the containers:
```bash
docker-compose up -d --build
```

This will start two services:
1. `db`: PostgreSQL database with PostGIS and pgvector extensions
2. `django`: Django backend server

### Django Setup
Once the containers are running, execute the following commands in the Django container:

1. Make migrations:
```bash
docker-compose exec django python manage.py makemigrations
```

2. Apply migrations:
```bash
docker-compose exec django python manage.py migrate
```

3. Create a superuser:
```bash
docker-compose exec django python manage.py createsuperuser
```

4. Import sample properties from CSV:
```bash
docker-compose exec django python manage.py import_properties data/sample_properties.csv
```

### Access the Application
- Django Admin: http://localhost:8000/admin/
- Django Server: http://localhost:8000/

## Tech Stack
- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL + PostGIS + pgvector
- Sentence Transformers
- Pandas
- Pillow
