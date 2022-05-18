#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request
from flask import make_response
from flask import url_for
from flask_httpauth import HTTPBasicAuth



auth = HTTPBasicAuth()

app = Flask(__name__)


@app.route('/photos/api/', methods=['GET'])
def get_api():
    return "Dokumentacija\nPopis URL-ova:\n\\api - početna stranica s dokumentacijom\n\\GET /photos/api/users - ispis svih korisnika\
    \n\\ POST /photos/api/users - kreiranje novog korisnika\n\\GET /photos/api/users/<int:user_id> - informacije o jednom korisniku\
    \n\\PUT /photos/api/users/<int:user_id> - uređivanje podataka jednog korisnika\n\\DELETE /photos/api/users/<int:user_id> - brisanje korisnika\
    \n\\GET /photos/api/pics - ispis informacija o svim slikama\n\\GET /photos/api/pics/<int:pic_id> - ispis informacije o pojedinoj slici\
    \n\\POST /photos/api/pics - dodavanje nove slike\n\\PUT /photos/api/pics/<int:pic_id> - uređivanje informacije o jenoj slici\
    \n\\DELETE /photos/pics/<int:pic_id> - brisanje slike, \n\\GET /photos/api/users/<int:pic_id>/pics - dohvat slika jednog korisnika (potrebna autentifikacija)"

users = [
    {
    	'id': 1,
        'name': u'Ivan',
        'password': u'python1'
    },
    {
    	'id': 2,
        'name': u'Marko',
        'password': u'abcdef'
    }
]


@app.route('/photos/api/users', methods=['GET'])
def get_users():
    return jsonify({'users': [make_public_user(user) for user in users]})


@app.route('/photos/api/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name'],
        'password': request.json.get('password', ""),
    }
    users.append(user)
    return jsonify({'user': user}), 201

def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_users', user_id=user['id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user


@app.route('/photos/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


@app.route('/photos/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'password' in request.json and type(request.json['password']) is not unicode:
    	abort(400)

    task[0]['name'] = request.json.get('name', task[0]['name'])
    task[0]['password'] = request.json.get('password', task[0]['password'])
    return jsonify({'user': user[0]})


@app.route('/photos/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    tasks.remove(user[0])
    return jsonify({'result': True})

pics = [
    {
        'id': 1,
        'title': u'Nature',
        'description': u'Beautiful nature'
    },
    {
        'id': 2,
        'title': u'Books',
        'description': u'A lot of books' 
    }
]


@app.route('/photos/api/pics', methods=['GET'])
#@auth.login_required
def get_pics():
    return jsonify({'pics': [make_public_pic(pic) for pic in pics]})


@app.route('/photos/api/pics/<int:pic_id>', methods=['GET'])
def get_pic(pic_id):
    pic = [pic for pic in pics if pic['id'] == pic_id]
    if len(pic) == 0:
        abort(404)
    return jsonify({'pic': pic[0]})


def make_public_pic(pic):
    new_pic = {}
    for field in pic:
        if field == 'id':
            new_pic['uri'] = url_for('get_pics', pic_id=pic['id'], _external=True)
        else:
            new_pic[field] = pic[field]
    return new_pic



@app.route('/photos/api/pics', methods=['POST'])
#@auth.login_required
def create_pic():
    if not request.json or not 'title' in request.json:
        abort(400)
    pic = {
        'id': pics[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
    }
    pics.append(pic)
    return jsonify({'pic': pic}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/photos/api/pics/<int:pic_id>', methods=['PUT'])
def update_pic(pic_id):
    pic = [pic for pic in pics if pic['id'] == pic_id]
    if len(pic) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    task[0]['title'] = request.json.get('title', pic[0]['title'])
    task[0]['description'] = request.json.get('description', pic[0]['description'])
    return jsonify({'pic': pic[0]})


@app.route('/photos/pics/<int:pic_id>', methods=['DELETE'])
#@auth.login_required
def delete_pic(pic_id):
    pic = [pic for pic in pics if pic['id'] == pic_id]
    if len(pic) == 0:
        abort(404)
    tasks.remove(pic[0])
    return jsonify({'result': True})


@auth.get_password
def get_password(username):
    if username == 'Ivan':
        return 'python1'
    if username == 'Marko':
    	return 'abcdef'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.route('/photos/api/users/<int:pic_id>/pics', methods=['GET'])
@auth.login_required
def find_pic(pic_id):
    pic = [pic for pic in pics if pic['id'] == pic_id]
    if len(pic) == 0:
        abort(404)
    return jsonify({'pic': pic[0]})

if __name__ == '__main__':
    app.run(debug=True)

