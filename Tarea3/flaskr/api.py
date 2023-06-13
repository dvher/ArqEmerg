from flask import (
    Blueprint, request, jsonify
)

from flaskr.db import get_db

v1 = Blueprint('apiv1', __name__, url_prefix='/api/v1')

@v1.route('location', methods=('GET', 'PUT', 'DELETE'))
def location():
    if request.method == 'GET':
        company_api_key = request.args.get('company_api_key')

        if company_api_key is None:
            return jsonify({'error': 'company_api_key is required'}), 400
        
        db = get_db()
    
        company = db.execute(
            'SELECT id FROM Company WHERE api_key = ?', (company_api_key,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company_api_key is invalid'}), 400
        
        loc_id = request.args.get('id')

        if loc_id is not None:
            location = db.execute(
                'SELECT * FROM Location WHERE id = ?', (loc_id,)
            ).fetchone()

            if location is None:
                return jsonify({'error': 'location id is invalid'}), 400

            location = dict(location)

            return jsonify(location), 200

        locations = db.execute(
            'SELECT * FROM Location WHERE company_id = ?', (company['id'],)
        ).fetchall()

        locations = [dict(loc) for loc in locations]

        return jsonify(locations), 200
    
    elif request.method == 'PUT':

        data = request.get_json()

        if data is None:
            return jsonify({'error': 'data is required'}), 400
        
        company_api_key = data.get('company_api_key')

        if company_api_key is None:
            return jsonify({'error': 'company_api_key is required'}), 400
        
        db = get_db()

        loc_id = data.get('id')
        name = data.get('name')
        country = data.get('country')
        city = data.get('city')
        meta = data.get('meta')

        if name is None or country is None or city is None:
            return jsonify({'error': 'name, country and city are required'}), 400
        
        company = db.execute(
            'SELECT id FROM Company WHERE api_key = ?', (company_api_key,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company_api_key is invalid'}), 400
        
        db.execute(
            'INSERT OR REPLACE INTO Location (id, company_id, name, country, city, meta) VALUES (?, ?, ?, ?, ?, ?)',
            (loc_id, company['id'], name, country, city, meta)
        )

        db.commit()

        return jsonify({'success': True}), 200
    
    elif request.method == 'DELETE':
        company_api_key = request.args.get('company_api_key')

        if company_api_key is None:
            return jsonify({'error': 'company_api_key is required'}), 400
        
        db = get_db()

        loc_id = request.args.get('id')

        if loc_id is None:
            return jsonify({'error': 'location id is required'}), 400
        
        company = db.execute(
            'SELECT id FROM Company WHERE api_key = ?', (company_api_key,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company_api_key is invalid'}), 400
        
        db.execute(
            'DELETE FROM Location WHERE id = ?', (loc_id,)
        )

        db.commit()

        return jsonify({'success': True}), 200
    
@v1.route('sensor', methods=('GET', 'PUT', 'DELETE'))
def sensor():
    if request.method == 'GET':
        company_api_key = request.args.get('company_api_key')

        if company_api_key is None:
            return jsonify({'error': 'company_api_key is required'}), 400
        
        db = get_db()
    
        company = db.execute(
            'SELECT id FROM Company WHERE api_key = ?', (company_api_key,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company_api_key is invalid'}), 400
        
        sensor_id = request.args.get('id')

        if sensor_id is not None:
            sensor = db.execute(
                'SELECT * FROM Sensor WHERE id = ?', (sensor_id,)
            ).fetchone()

            if sensor is None:
                return jsonify({'error': 'sensor id is invalid'}), 400
            
            sensor = dict(sensor)

            return jsonify(sensor), 200
        
        locations = db.execute(
            'SELECT * FROM Location WHERE company_id = ?', (company['id'],)
        ).fetchall()

        locations = [dict(loc)['id'] for loc in locations]

        sensors = db.execute(
            'SELECT * FROM Sensor WHERE location_id IN ({})'.format(','.join('?'*len(locations))), locations
        ).fetchall()

        sensors = [dict(sensor) for sensor in sensors]

        return jsonify(sensors), 200
    
    elif request.method == 'PUT':
        data = request.get_json()

        if data is None:
            return jsonify({'error': 'data is required'}), 400
        
        company_api_key = data.get('company_api_key')

        if company_api_key is None:
            return jsonify({'error': 'company_api_key is required'}), 400
        
        db = get_db()

        sensor_id = data.get('id')
        location_id = data.get('location_id')
        name = data.get('name')
        category = data.get('category')
        meta = data.get('meta')

        if location_id is None or name is None or category is None:
            return jsonify({'error': 'location_id, name and category are required'}), 400
        
        company = db.execute(
            'SELECT * FROM Company WHERE api_key = ?', (company_api_key,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company_api_key is invalid'}), 400
        
        location_exists = db.execute(
            'SELECT * FROM Location WHERE id = ?', (location_id,)
        ).fetchone()

        if location_exists is None:
            return jsonify({'error': 'location_id is invalid'}), 400
        
        sensor_api_key = db.execute(
            'SELECT * FROM Sensor WHERE id = ?', (sensor_id,)
        ).fetchone()

        if sensor_api_key is None:
            return jsonify({'error': 'sensor id is invalid'}), 400
        
        db.execute(
            'INSERT OR REPLACE INTO Sensor (id, location_id, name, category, meta, api_key) VALUES (?, ?, ?, ?, ?, ?)',
            (sensor_id, location_id, name, category, meta, sensor_api_key['api_key'])
        )

        db.commit()

        return jsonify({'success': True}), 200
    
    elif request.method == 'DELETE':
        company_api_key = request.args.get('company_api_key')

        if company_api_key is None:
            return jsonify({'error': 'company_api_key is required'}), 400
        
        db = get_db()

        sensor_id = request.args.get('id')

        if sensor_id is None:
            return jsonify({'error': 'sensor id is required'}), 400
        
        company = db.execute(
            'SELECT id FROM Company WHERE api_key = ?', (company_api_key,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company_api_key is invalid'}), 400
        
        db.execute(
            'DELETE FROM Sensor WHERE id = ?', (sensor_id,)
        )

        db.commit()

        return jsonify({'success': True}), 200

@v1.route('sensor_data', methods=('GET', 'POST'))
def sensor_data():
    if request.method == 'GET':
        company_api_key = request.args.get('company_api_key')

        if company_api_key is None:
            return jsonify({'error': 'company_api_key is required'}), 400
        
        from_date = request.args.get('from')
        to_date = request.args.get('to')
        sensor_id = request.args.get('sensor_id')

        if from_date is None or to_date is None or sensor_id is None:
            return jsonify({'error': 'from, to and sensor_id are required'}), 400
        
        if not sensor_id.startswith('[') or not sensor_id.endswith(']'):
            return jsonify({'error': 'sensor_id must be a list'}), 400
        
        sensor_id = sensor_id[1:-1]
        sensor_id = list(map(int, sensor_id.split(',')))

        db = get_db()

        company = db.execute(
            'SELECT id FROM Company WHERE api_key = ?', (company_api_key,)
        ).fetchone()

        if company is None:
            return jsonify({'error': 'company_api_key is invalid'}), 400
        
        data = db.execute(
            'SELECT * FROM SensorData WHERE sensor_id IN ({}) AND fecha BETWEEN ? AND ?'.format(','.join('?'*len(sensor_id))), (*sensor_id, from_date, to_date)
            ).fetchall()
        
        data = [dict(d) for d in data]
        
        return jsonify(data), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        sensor_api_key = data.get('sensor_api_key')

        if sensor_api_key is None:
            return jsonify({'error': 'sensor_api_key is required'}), 400
        
        db = get_db()

        sensor_id = db.execute(
            'SELECT id FROM Sensor WHERE api_key = ?', (sensor_api_key,)
        ).fetchone()

        if sensor_id is None:
            return jsonify({'error': 'sensor_api_key is invalid'}), 400
        
        body = data['json_data']

        if body is None:
            return jsonify({'error': 'json_data is required'}), 400

        if not isinstance(body, (list, tuple)):
            body = [body]

        for data in body:
            fecha = data.get('fecha')
            humedad = data.get('humedad')
            temperatura = data.get('temperatura')
            luminosidad = data.get('luminosidad')
            potencia_senal = data.get('potencia_senal')

            if fecha is None:
                return jsonify({'error': 'fecha is required'}), 400
            
            if (humedad is None and temperatura is None) and (luminosidad is None and potencia_senal is None):
                return jsonify({'error': 'humedad and temperatura or luminosidad and potencia_senal are required'}), 400
            
            db.execute(
                'INSERT INTO SensorData (sensor_id, fecha, humedad, temperatura, luminosidad, potencia_senal) VALUES (?, ?, ?, ?, ?, ?)',
                (sensor_id['id'], fecha, humedad, temperatura, luminosidad, potencia_senal)
            )
            
        db.commit()

        return jsonify({'success': True}), 201
    
