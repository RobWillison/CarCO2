from flask import Flask, jsonify
from flask import render_template
import pymysql.cursors
from flask import request

def connection():
    return pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 db='vehicle_emissions',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

def find_range(range):
    return {'1.2':'1100cc to 1199cc', '1.3':'1200cc to 1299cc', '1.4':'1300cc to 1399cc', '1.5':'1400cc to 1499cc', '1.6':'1500cc to 1599cc'}[str(range)]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/make')
def make():
    cursor = connection().cursor()
    term = request.args['q']
    cursor.execute('SELECT make FROM cars WHERE make LIKE %s GROUP BY make LIMIT 5', term + '%')
    makes = [row['make'] for row in cursor.fetchall()]
    print(makes)
    cursor.close()
    return jsonify(makes)

@app.route('/model')
def model():
    cursor = connection().cursor()
    term = request.args['q']
    make, model = term.split('///')

    cursor.execute('SELECT cars.make, cars.model FROM cars WHERE cars.make = %s AND cars.description LIKE %s GROUP BY cars.model', (make, '%' + model + '%'))

    models = [row['model'] for row in cursor.fetchall()]
    cursor.close()
    return jsonify(models)

@app.route('/engine')
def engine():
    cursor = connection().cursor()
    term = request.args['q']
    make, model, year, fuel, term = term.split('///')

    cursor.execute('SELECT engine_size_max as size FROM cars INNER JOIN versions ON cars.id = car_id WHERE make = %s AND model LIKE %s AND fuel_type = %s AND first_license_year = %s AND co2 IS NOT NULL GROUP BY engine_size_max', (make, '%' + model + '%', fuel, year))
    print(cursor._last_executed)
    sizes = [int(row['size'] + 1) / 1000.0 for row in cursor.fetchall()]
    cursor.close()
    return jsonify(sizes)

@app.route('/data')
def data():
    data = request.args
    print(data)
    sql_params = []
    conditions = []

    if data['make']:
        conditions.append('make = %s')
        sql_params.append(data['make'])
    if data['model']:
        conditions.append('model LIKE %s')
        sql_params.append('%' + data['model'] + '%')
    if data['year']:
        conditions.append('first_license_year = %s')
        sql_params.append(data['year'])
    if data['fuel']:
        conditions.append('fuel_type = %s')
        sql_params.append(data['fuel'])
    if data['engine']:
        conditions.append('engine_size_min < %s AND engine_size_max > %s')
        sql_params.append((float(data['engine']) * 1000) -2)
        sql_params.append((float(data['engine']) * 1000) -2)
    print(conditions)

    sql = 'SELECT make, model, first_license_year, engine_size_max, fuel_type, co2, count FROM versions INNER JOIN cars ON cars.id = car_id WHERE co2 IS NOT NULL AND ' + ' AND '.join(conditions) + ' ORDER BY co2 ASC LIMIT 10'

    cursor = connection().cursor()
    cursor.execute(sql, sql_params)

    print(cursor._last_executed)

    results = cursor.fetchall()
    data = [{'co2': r['co2'], 'count': r['count'], 'make': r['make'], 'model': r['model'], 'year': r['first_license_year'], 'engine': (r['engine_size_max'] + 1) / 1000, 'fuel': r['fuel_type'], 'score': min(((r['co2'] - 80) / 160.0), 1)} for r in results]

    cursor.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
