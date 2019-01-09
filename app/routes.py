#!flask/bin/python
from app import application
from app.backend import DefineQuery as b
from flask import Flask, jsonify, abort, make_response, request, url_for, render_template
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "kuba": "test",
    "test": "test1"
}

def make_public_app(id):
    result = b.get_app_by_id(id)
    del result['id']
    result['uri'] = url_for('get_app', app_id=id, _external=True)
    return result

@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None

@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access - go back'}), 401)    


@application.route('/app')
def hello_name():
   t = [make_public_app(app) for app in b.get_apps_id()]
   return render_template('hello.html', table = t)

# return all app with all infos 
@application.route('/api/apps', methods=['GET'])
@auth.login_required
def get_apps():
    return jsonify({'apps': [make_public_app(app) for app in b.get_apps_id()]})

# return all info about one app
@application.route('/api/app/<int:app_id>', methods=['GET'])
def get_app(app_id):
    app = [app for app in b.get_apps_id() if app_id == app]
    if len(app) == 0:
        abort(404)
    return jsonify({'apps': b.get_app_by_id(app[0])})

@application.route('/api/app/new', methods=['POST'])
@auth.login_required
def create_app():
    if not request.json or not 'app_name' in request.json:
        abort(400)
    b.add_new_app(request.json['app_name'],  request.json.get('version', "1.0"), request.json.get('updated_by', 'jenkins'))
    return jsonify({'task': b.get_last_app()}), 201

# Update version
@application.route('/api/app/<int:app_id>', methods=['PUT'])
@auth.login_required
def update_app(app_id):
    app = [app for app in b.get_apps_id() if app_id == app]
    if len(app) == 0 or not request.json:
        abort(404)
    if 'app_name' in request.json and type(request.json['app_name']) != str:
        abort(400)
    if 'version' in request.json and type(request.json['version']) != str:
        abort(400)
    if 'updated_by' in request.json and type(request.json['updated_by']) != str:
        abort(400)

    new_app_name =  request.json.get('app_name', '')
    new_version = request.json.get('version', '')
    new_updated_by = request.json.get('updated_by', '')

    if len(new_app_name) != 0:
        b.update_column('app_name', new_app_name, app[0])

    if len(new_version) != 0:
        b.update_column('version', new_version, app[0])

    if len(new_updated_by) != 0:
        b.update_column('updated_by', new_updated_by, app[0])

    return jsonify({'task': b.get_app_by_id(app[0])})

#Delete app
@application.route('/api/app/<int:app_id>', methods=['DELETE'])
@auth.login_required
def delete_app(app_id):
    app = [app for app in b.get_apps_id() if app_id == app]
    if len(app) == 0:
        abort(404)
    return jsonify({'App': b.delete_app_by_id(app[0])})
    
