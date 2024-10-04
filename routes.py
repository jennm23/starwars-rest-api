from flask import Flask, jsonify, request
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get_or_404(people_id)
    return jsonify({
        'id': person.id,
        'name': person.name,
        'birth_year': person.birth_year,
        'eye_color': person.eye_color,
        'gender': person.gender,
        'hair_color': person.hair_color,
        'height': person.height,
        'mass': person.mass,
        'skin_color': person.skin_color
    })

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify({
        'id': planet.id,
        'name': planet.name,
        'climate': planet.climate,
        'gravity': planet.gravity,
        'rotation_period': planet.rotation_period,
        'population': planet.population,
        'terrain': planet.terrain
    })

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'planet_id': f.planet_id,
        'people_id': f.people_id
    } for f in favorites])

@app.route('/favorite/<string:item_type>/<int:item_id>', methods=['POST'])
def add_favorite(item_type, item_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id es requerido'}), 400

    new_favorite = Favorite(user_id=user_id)
    if item_type == 'planet':
        new_favorite.planet_id = item_id
    elif item_type == 'people':
        new_favorite.people_id = item_id
    else:
        return jsonify({'message': 'Tipo de favorito no válido'}), 400

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'message': 'Favorito agregado'}), 201

@app.route('/favorite/<string:item_type>/<int:item_id>', methods=['DELETE'])
def remove_favorite(item_type, item_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id es requerido'}), 400

    favorite = Favorite.query.filter_by(user_id=user_id).filter(
        (Favorite.planet_id == item_id) if item_type == 'planet' else (Favorite.people_id == item_id)
    ).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorito eliminado'}), 204

    return jsonify({'message': 'Favorito no encontrado'}), 404

if __name__ == '__main__':
    app.run()

