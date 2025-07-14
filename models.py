from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, Movie, Actor, db # Import the db instance
from auth import AuthError, requires_auth
from flask_migrate import Migrate # Import Migrate

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    @app.route('/')
    def health_check():
        return jsonify({"success": True, "message": "Healthy"})

    # -- Actor Endpoints --
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        if len(actors) == 0:
            # Return an empty list for GET requests, not a 404
            return jsonify({
                'success': True,
                'actors': []
            })

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if not body or 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400) # Bad Request

        new_actor = Actor(
            name=body.get('name'),
            age=body.get('age'),
            gender=body.get('gender')
        )
        new_actor.insert()

        return jsonify({
            'success': True,
            'created': new_actor.id
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)
            
        if 'name' in body:
            actor.name = body.get('name')
        if 'age' in body:
            actor.age = body.get('age')

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    # -- Movie Endpoints --
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()
        if len(movies) == 0:
            # Return an empty list for GET requests, not a 404
            return jsonify({
                'success': True,
                'movies': []
            })

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if not body or 'title' not in body or 'release_date' not in body:
            abort(400) # Bad Request

        new_movie = Movie(
            title=body.get('title'),
            release_date=body.get('release_date')
        )
        new_movie.insert()

        return jsonify({
            'success': True,
            'created': new_movie.id
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        if 'title' in body:
            movie.title = body.get('title')
        if 'release_date' in body:
            movie.release_date = body.get('release_date')

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    # -- Error Handlers --
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
