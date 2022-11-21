from flask import Blueprint, request, jsonify
from marvel_collection.helpers import token_required
from marvel_collection.models import db, MarvelCharacter, marvel_char_schema, marvel_chars_schemas

api = Blueprint('api', __name__, url_prefix='/api')

# @api.route('/getdata')
# @token_required
# def getdata():
#     return {'some':'value'}

@api.route('/marvelchars', methods=['POST'])
@token_required
def add_char(owner):
    superhero_name = request.json['superhero_name']
    name = request.json['name']
    description = request.json['description']
    num_of_comics = request.json['num_of_comics']
    superpower = request.json['superpower']
    user_token = owner.token

    marvel_char = MarvelCharacter(superhero_name, name, description, num_of_comics, superpower, user_token=user_token)
    db.session.add(marvel_char)
    db.session.commit()

    response = marvel_char_schema.dump(marvel_char)
    return jsonify(response)

@api.route('/marvelchars', methods=['GET'])
@token_required
def get_all_chars(owner):
    owner_token = owner.token
    marvel_chars = MarvelCharacter.query.filter_by(user_token=owner_token).all()
    response = marvel_chars_schemas.dump(marvel_chars)
    return jsonify(response)

@api.route('/marvelchars/<id>', methods=['GET'])
@token_required
def get_char(owner, id):
    owner_token = owner.token
    if owner_token == owner.token:
        marvel_char = MarvelCharacter.query.get(id)
        response = marvel_char_schema.dump(marvel_char)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid dToken Required'}), 401

@api.route('/marvelchars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_char(owner, id):
    marvel_char = MarvelCharacter.query.get(id)
    marvel_char.superhero_name = request.json['superhero_name']
    marvel_char.name = request.json['name']
    marvel_char.description = request.json['description']
    marvel_char.num_of_comics = request.json['num_of_comics']
    marvel_char.superpower = request.json['superpower']
    marvel_char.user_token = owner.token

    db.session.commit()
    response = marvel_char_schema.dump(marvel_char)
    return jsonify(response)

@api.route('/marvelchars/<id>', methods = ['DELETE'])
@token_required
def delete_char(owner, id):
    marvel_char = MarvelCharacter.query.get(id)
    db.session.delete(marvel_char)
    db.session.commit()
    response = marvel_char_schema.dump(marvel_char)
    return jsonify(response)