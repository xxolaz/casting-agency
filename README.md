# Casting Agency API

## Project Motivation
This project is a backend API for a Casting Agency. It allows authorized users to manage a database of actors and movies. The API provides endpoints for creating, retrieving, updating, and deleting actors and movies, with Role-Based Access Control (RBAC) to ensure that users can only perform actions appropriate for their assigned roles (Casting Assistant, Casting Director, or Executive Producer).

---

## API URL
> `https://casting-agency-api-gg07.onrender.com/`

---

## Dependencies
The project is built with Python and Flask and relies on the following main packages:
- `Flask`: A lightweight web framework for Python.
- `Flask-SQLAlchemy`: An extension that adds SQLAlchemy support to Flask.
- `Flask-Migrate`: An extension that handles SQLAlchemy database migrations for Flask applications.
- `psycopg2-binary`: A PostgreSQL adapter for Python.
- `python-dotenv`: For managing environment variables in a local development environment.
- `gunicorn`: A Python WSGI HTTP Server for UNIX, used for production deployment.
- `Flask-Cors`: An extension for handling Cross-Origin Resource Sharing (CORS).
- `python-jose`: A library for handling JSON Object Signing and Encryption (JOSE) and JWTs.

---

## Local Development
To run this project on your local machine, follow these steps:

#### 1. Set Up Virtual Environment
Create and activate a Python virtual environment to keep dependencies isolated.
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

2. Install Dependencies
Install all required packages from the requirements.txt file.

pip install -r requirements.txt

3. Set Up the Database
Ensure you have PostgreSQL installed and running. Then, create the database for the project.

# Open the psql command-line tool
psql

# Inside psql, run the following SQL command
CREATE DATABASE casting_agency;

4. Set Up Environment Variables
Create a setup.sh file in the root directory with your Auth0 and database credentials.

# In setup.sh
export AUTH0_DOMAIN='YOUR_AUTH0_DOMAIN'
export ALGORITHMS=['RS256']
export API_AUDIENCE='YOUR_API_AUDIENCE'
export DATABASE_URL='postgresql://localhost:5432/casting_agency'

Run the script to load the variables.

source setup.sh

5. Run Database Migrations
Initialize the database with the required tables.

# Set the Flask app environment variable
export FLASK_APP=app.py

# Run the migrations
flask db upgrade

6. Run the Application
Start the Flask development server.

python app.py

The application will be running at http://127.0.0.1:8080/.

API Documentation
Authentication and Testing
To test the API endpoints, you must include a JSON Web Token (JWT) in the Authorization header of your requests. The API has three roles, each with different permissions:

Casting Assistant: Can view actors and movies.

Casting Director: Has all permissions of the Assistant, plus can add, delete, and modify actors and modify movies.

Executive Producer: Has all permissions of the Director, plus can add and delete movies.

Please fill in your sample JWTs for each role below:

Casting Assistant Token:

Bearer YOUR_CASTING_ASSISTANT_TOKEN

Casting Director Token:

Bearer YOUR_CASTING_DIRECTOR_TOKEN

Executive Producer Token:

Bearer YOUR_EXECUTIVE_PRODUCER_TOKEN

Endpoints
GET /actors
Retrieves a list of all actors.

Permission Required: get:actors

Sample cURL Request:

curl -H "Authorization: Bearer <TOKEN>" https://YOUR_RENDER_API_[URL.onrender.com/actors](https://URL.onrender.com/actors)

Sample JSON Response:

{
    "actors": [
        {
            "age": 35,
            "gender": "Male",
            "id": 1,
            "name": "John Doe"
        }
    ],
    "success": true
}

POST /actors
Creates a new actor.

Permission Required: post:actors

Sample cURL Request:

curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"name": "Jane Smith", "age": 28, "gender": "Female"}' https://YOUR_RENDER_API_[URL.onrender.com/actors](https://URL.onrender.com/actors)

Sample JSON Response:

{
    "created": 2,
    "success": true
}

PATCH /actors/<id>
Updates an existing actor's information.

Permission Required: patch:actors

Sample cURL Request:

curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"age": 29}' https://YOUR_RENDER_API_[URL.onrender.com/actors/2](https://URL.onrender.com/actors/2)

Sample JSON Response:

{
    "actor": {
        "age": 29,
        "gender": "Female",
        "id": 2,
        "name": "Jane Smith"
    },
    "success": true
}

DELETE /actors/<id>
Deletes an existing actor.

Permission Required: delete:actors

Sample cURL Request:

curl -X DELETE -H "Authorization: Bearer <TOKEN>" https://YOUR_RENDER_API_[URL.onrender.com/actors/2](https://URL.onrender.com/actors/2)

Sample JSON Response:

{
    "deleted": 2,
    "success": true
}

GET /movies
Retrieves a list of all movies.

Permission Required: get:movies

Sample cURL Request:

curl -H "Authorization: Bearer <TOKEN>" https://YOUR_RENDER_API_[URL.onrender.com/movies](https://URL.onrender.com/movies)

Sample JSON Response:

{
    "movies": [
        {
            "id": 1,
            "release_date": "2024-01-01",
            "title": "The First Movie"
        }
    ],
    "success": true
}

POST /movies
Creates a new movie.

Permission Required: post:movies

Sample cURL Request:

curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"title": "The Sequel", "release_date": "2025-05-10"}' https://YOUR_RENDER_API_[URL.onrender.com/movies](https://URL.onrender.com/movies)

Sample JSON Response:

{
    "created": 2,
    "success": true
}

PATCH /movies/<id>
Updates an existing movie's information.

Permission Required: patch:movies

Sample cURL Request:

curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"title": "The Sequel: Remastered"}' https://YOUR_RENDER_API_[URL.onrender.com/movies/2](https://URL.onrender.com/movies/2)

Sample JSON Response:

{
    "movie": {
        "id": 2,
        "release_date": "2025-05-10",
        "title": "The Sequel: Remastered"
    },
    "success": true
}

DELETE /movies/<id>
Deletes an existing movie.

Permission Required: delete:movies

Sample cURL Request:

curl -X DELETE -H "Authorization: Bearer <TOKEN>" https://YOUR_RENDER_API_[URL.onrender.com/movies/2](https://URL.onrender.com/movies/2)

Sample JSON Response:

{
    "deleted": 2,
    "success": true
}
