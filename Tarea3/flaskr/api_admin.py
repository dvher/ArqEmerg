from flask import (
    Blueprint, request, jsonify, make_response
)

from flaskr.db import get_db

from flaskr.auth_middleware import token_required

from werkzeug.security import check_password_hash

import jwt

import os

v1_adm = Blueprint('api_adminv1', __name__, url_prefix='/api/v1/admin')

@v1_adm.route('login', methods=('POST',))
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return jsonify({'error': 'username and password are required'}), 400
    
    db = get_db()

    user = db.execute(
        'SELECT * FROM Admin WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        return jsonify({'error': 'username is invalid'}), 400
    
    if not check_password_hash(user['password'], password):
        return jsonify({'error': 'password is invalid'}), 400

    
    token = jwt.encode({
        'username': user['username'],
        'id': db.cursor().lastrowid
    },
    os.environ.get('SECRET_KEY', default='dev'),
    algorithm='HS256')
    
    resp = make_response(jsonify({'message': 'Login successful'}), 200)

    resp.headers['Authorization'] = 'Bearer ' + token

    return resp

@v1_adm.route('company', methods=('GET', 'POST', 'PUT', 'DELETE'))
@token_required
def company():
    if request.method == 'GET':
        company_id = request.args.get('id')

        if company_id is not None:
            db = get_db()

            company = db.execute(
                'SELECT * FROM Company WHERE id = ?', (company_id,)
            ).fetchone()

            if company is None:
                return jsonify({'error': 'company id is invalid'}), 400

            company = dict(company)

            return jsonify(company), 200
        
        db = get_db()

        companies = db.execute(
            'SELECT * FROM Company'
        ).fetchall()

        companies = [dict(company) for company in companies]

        return jsonify(companies), 200
    
    elif request.method == 'POST':
        data = request.get_json()

        if data is None:
            return jsonify({'error': 'JSON data is required'}), 400
        
        name = data.get('name')

        if name is None:
            return jsonify({'error': 'name is required'}), 400
        
        api_key = jwt.encode({
            'name': name
        },
        os.environ.get('SECRET_KEY', default='dev'),
        algorithm='HS256')

        db = get_db()

        db.execute(
            'INSERT INTO Company (name, api_key) VALUES (?, ?)',
            (name, api_key)
        )

        db.commit()

        return jsonify({'message': 'Company created successfully', 'api_key': api_key}), 201
    
    elif request.method == 'PUT':
        data = request.get_json()

        if data is None:
            return jsonify({'error': 'JSON data is required'}), 400
        
        name = data.get('name')

        if name is None:
            return jsonify({'error': 'name is required'}), 400
        
        company_id = data.get('id')

        if company_id is None:
            return jsonify({'error': 'company id is required'}), 400
        
        db = get_db()

        company = db.execute(
            'SELECT * FROM Company WHERE id = ?', (company_id,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company id is invalid'}), 400
        
        api_key = jwt.encode({
            'name': name
        },
        os.environ.get('SECRET_KEY', default='dev'),
        algorithm='HS256')
        
        db.execute(
            'UPDATE Company SET name = ?, api_key = ? WHERE id = ?',
            (name, api_key, company_id)
        )

        db.commit()

        return jsonify({'message': 'Company updated successfully', 'api-key': api_key}), 200
    
    elif request.method == 'DELETE':
        
        company_id = request.args.get('id')

        if company_id is None:
            return jsonify({'error': 'company id is required'}), 400
        
        db = get_db()

        company = db.execute(
            'SELECT * FROM Company WHERE id = ?', (company_id,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company id is invalid'}), 400
        
        db.execute(
            'DELETE FROM Company WHERE id = ?',
            (company_id,)
        )

        db.commit()

        return jsonify({'message': 'Company deleted successfully'}), 200

@v1_adm.route('location', methods=('GET', 'POST', 'PUT', 'DELETE'))
@token_required
def location():
    if request.method == 'GET':
        company_id = request.args.get('company_id')

        if company_id is None:
            return jsonify({'error': 'company id is required'}), 400
        
        db = get_db()

        company = db.execute(
            'SELECT * FROM Company WHERE id = ?', (company_id,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company id is invalid'}), 400
        
        loc_id = request.args.get('location_id')

        if loc_id is not None:
            location = db.execute(
                'SELECT * FROM Location WHERE id = ?', (loc_id,)
            ).fetchone()

            if location is None:
                return jsonify({'error': 'location id is invalid'}), 400
            
            location = dict(location)

            return jsonify(location), 200

        locations = db.execute(
            'SELECT * FROM Location WHERE company_id = ?', (company_id,)
        ).fetchall()

        locations = [dict(location) for location in locations]

        return jsonify(locations), 200
    
    elif request.method == 'POST':

        data = request.get_json()

        if data is None:
            return jsonify({'error': 'JSON data is required'}), 400

        company_id = data.get('company_id')

        if company_id is None:
            return jsonify({'error': 'company id is required'}), 400
        
        db = get_db()

        company = db.execute(
            'SELECT * FROM Company WHERE id = ?', (company_id,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company id is invalid'}), 400
        
        name = data.get('name')
        country = data.get('country')
        city = data.get('city')
        meta = data.get('meta')

        if name is None or country is None or city is None:
            return jsonify({'error': 'name, country and city are required'}), 400
        
        db.execute(
            'INSERT INTO Location (name, country, city, meta, company_id) VALUES (?, ?, ?, ?, ?)',
            (name, country, city, meta, company_id)
        )

        db.commit()

        return jsonify({'message': 'Location created successfully'}), 201
    
    elif request.method == 'PUT':
        data = request.get_json()

        if data is None:
            return jsonify({'error': 'JSON data is required'}), 400
        
        name = data.get('name')
        country = data.get('country')
        city = data.get('city')
        meta = data.get('meta')

        if name is None or country is None or city is None:
            return jsonify({'error': 'name, country and city are required'}), 400
        
        loc_id = data.get('id')

        if loc_id is None:
            return jsonify({'error': 'location id is required'}), 400
        
        db = get_db()

        location = db.execute(
            'SELECT * FROM Location WHERE id = ?', (loc_id,)
        ).fetchone()

        if location is None:
            return jsonify({'error': 'location id is invalid'}), 400
        
        db.execute(
            'UPDATE Location SET name = ?, country = ?, city = ?, meta = ? WHERE id = ?',
            (name, country, city, meta, loc_id)
        )

        db.commit()

        return jsonify({'message': 'Location updated successfully'}), 200
    
    elif request.method == 'DELETE':
        
        loc_id = request.args.get('id')

        if loc_id is None:
            return jsonify({'error': 'location id is required'}), 400
        
        db = get_db()

        location = db.execute(
            'SELECT * FROM Location WHERE id = ?', (loc_id,)
        ).fetchone()

        if location is None:
            return jsonify({'error': 'location id is invalid'}), 400
        
        db.execute(
            'DELETE FROM Location WHERE id = ?',
            (loc_id,)
        )

        db.commit()

        return jsonify({'message': 'Location deleted successfully'}), 200

@v1_adm.route('sensor', methods=('GET', 'POST', 'PUT', 'DELETE'))
@token_required
def sensor():
    if request.method == 'GET':
        company_id = request.args.get('company_id')
        loc_id = request.args.get('location_id')

        if company_id is None or loc_id is None:
            return jsonify({'error': 'company id and location id are required'}), 400
        
        db = get_db()

        company = db.execute(
            'SELECT * FROM Company WHERE id = ?', (company_id,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company id is invalid'}), 400
        
        location = db.execute(
            'SELECT * FROM Location WHERE id = ?', (loc_id,)
        ).fetchone()

        if location is None:
            return jsonify({'error': 'location id is invalid'}), 400
        
        sensor_id = request.args.get('sensor_id')

        if sensor_id is not None:
            sensor = db.execute(
                'SELECT * FROM Sensor WHERE id = ?', (sensor_id,)
            ).fetchone()

            if sensor is None:
                return jsonify({'error': 'sensor id is invalid'}), 400
            
            sensor = dict(sensor)

            return jsonify(sensor), 200

        sensors = db.execute(
            'SELECT * FROM Sensor WHERE location_id = ?', (loc_id,)
        ).fetchall()

        sensors = [dict(sensor) for sensor in sensors]

        return jsonify(sensors), 200
    
    elif request.method == 'POST':

        data = request.get_json()

        if data is None:
            return jsonify({'error': 'JSON data is required'}), 400
        
        db = get_db()
        
        loc_id = data.get('location_id')

        if loc_id is None:
            return jsonify({'error': 'location id is required'}), 400
        
        location = db.execute(
            'SELECT * FROM Location WHERE id = ?', (loc_id,)
        ).fetchone()

        if location is None:
            return jsonify({'error': 'location id is invalid'}), 400
        
        name = data.get('name')
        category = data.get('category')
        meta = data.get('meta')

        if name is None or category is None or meta is None:
            return jsonify({'error': 'name, category and meta are required'}), 400
        
        api_key = jwt.encode({
            'name': name,
            'category': category,
            'meta': meta,
            'id': db.cursor().lastrowid
        },
        os.environ.get('SECRET_KEY', default='dev'),
        algorithm='HS256')

        db.execute(
            'INSERT INTO Sensor (name, category, meta, api_key, location_id) VALUES (?, ?, ?, ?, ?)',
            (name, category, meta, api_key, loc_id)
        )

        db.commit()

        return jsonify({'message': 'Sensor created successfully', 'api_key': api_key}), 201
    
    elif request.method == 'PUT':
        data = request.get_json()

        if data is None:
            return jsonify({'error': 'JSON data is required'}), 400
        
        name = data.get('name')
        category = data.get('category')
        meta = data.get('meta')

        if name is None or category is None or meta is None:
            return jsonify({'error': 'name, category and meta are required'}), 400
        
        sensor_id = data.get('id')

        if sensor_id is None:
            return jsonify({'error': 'sensor id is required'}), 400
        
        db = get_db()

        sensor = db.execute(
            'SELECT * FROM Sensor WHERE id = ?', (sensor_id,)
        ).fetchone()

        if sensor is None:
            return jsonify({'error': 'sensor id is invalid'}), 400
        
        api_key = jwt.encode({
            'name': name,
            'category': category,
            'meta': meta
        },
        os.environ.get('SECRET_KEY', default='dev'),
        algorithm='HS256')
        
        db.execute(
            'UPDATE Sensor SET name = ?, category = ?, meta = ? WHERE id = ?',
            (name, category, meta, sensor_id)
        )

        db.commit()

        return jsonify({'message': 'Sensor updated successfully', 'api-key': api_key}), 200
    
    elif request.method == 'DELETE':
        
        sensor_id = request.args.get('id')

        if sensor_id is None:
            return jsonify({'error': 'sensor id is required'}), 400
        
        db = get_db()

        sensor = db.execute(
            'SELECT * FROM Sensor WHERE id = ?', (sensor_id,)
        ).fetchone()

        if sensor is None:
            return jsonify({'error': 'sensor id is invalid'}), 400
        
        db.execute(
            'DELETE FROM Sensor WHERE id = ?',
            (sensor_id,)
        )

        db.commit()

        return jsonify({'message': 'Sensor deleted successfully'}), 200
