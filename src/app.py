"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Ship, FavoriteCharacter
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialize_characters = [character.serialize() for character in characters]

    response_body = {
        "msg": "This is the list of characters",
        "results": serialize_characters
    }

    return jsonify(response_body), 200


@app.route('/characters/<int:id>', methods=['GET'])
def get_one_character(id):
    characters = Character.query.get(id)

    response_body = {
        "msg": "This is one character",
        "result": characters.serialize()
    }
    return jsonify(response_body), 200

@app.route('favorite/characters/<int:character_id>', methods=['POST'])
def create_favorite_character(character_id):
    new_favorite_chatacer = FavoriteCharacter(user_id=1, character_id=character_id)
    db.session.add(new_favorite_chatacer)
    db.session.commit()

    response_body = {
        "msg": "This is your post /favorite/characters/<int:character_id> response",
        "result": new_favorite_chatacer.serialize()
    }
    return jsonify(response_body), 200


@app.route('favorite/characters/<int: id>', methods=['DELETE'])
def create_favorite_character(id):
    favorite_chatacer = FavoriteCharacter.query.get(id)
    db.session.delete(favorite_chatacer)
    db.session.commit()

    response_body = {
        "msg": "This is your delete /favorite/characters/<int:id> response",
        "result": "eliminado"
    }
    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialize_planets = [planet.serialize() for planet in planets]

    response_body = {
        "msg": "This is the list of planets",
        "results": serialize_planets
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    planets = Planet.query.get(id)

    response_body = {
        "msg": "This is one planet",
        "result": planets.serialize()
    }
    return jsonify(response_body), 200



@app.route('/ships', methods=['GET'])
def get_ships():
    ships = Ship.query.all()
    serialize_ships = [ship.serialize() for ship in ships]

    response_body = {
        "msg": "This is the list of ships",
        "results": serialize_ships
    }

    return jsonify(response_body), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  
    fav_characters = db.session.query(Character).join(FavoriteCharacter).filter(FavoriteCharacter.user_id == user_id).all()
    fav_characters = [character.serialize() for character in fav_characters]
    fav_planets = []
    favorites = fav_characters + fav_planets

    response_body = {
        "msg": "This is the list of favorites for the user",
        "results": favorites
    }

    return jsonify(response_body), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


