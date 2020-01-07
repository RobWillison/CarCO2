from flask import Flask, jsonify
from flask import render_template
import pymysql.cursors
from flask import request

def connection():
    return pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='vehicle_emissions',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

def find_range(range):
    return {'1.2':'1100cc to 1199cc', '1.3':'1200cc to 1299cc', '1.4':'1300cc to 1399cc'}[str(range)]

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
    make, model, year, fuel, engine = term.split('///')

    cursor.execute('SELECT cars.make, cars.model FROM cars INNER JOIN car_counts ON car_counts.car_id = cars.id WHERE cars.make = %s AND cars.description LIKE %s AND cars.first_license_year = %s AND cars.fuel_type = %s AND `' + find_range(engine) + '` > 0 GROUP BY cars.model', (make, '%' + model + '%', year, fuel))
    models = [row['model'].replace(row['make'], '').strip() for row in cursor.fetchall()]
    cursor.close()
    return jsonify(models)

@app.route('/data')
def data():
    data = request.args
    cursor = connection().cursor()
    cursor.execute('SELECT * FROM dataset WHERE `Manufacturer` = %s AND `Model` LIKE %s AND year = %s AND `Engine Capacity` BETWEEN %s AND %s AND `Fuel Type` = %s', (data['make'], '%' + data['model'] + '%', data['year'], (float(data['engine']) * 1000) - 50, (float(data['engine']) * 1000) + 50, data['fuel']))
    co2 = [row['CO2 g/km'] for row in cursor.fetchall()]
    cursor.execute('SELECT car_counts.`' + find_range(data['engine']) + '` as total FROM cars INNER JOIN car_counts ON car_counts.car_id = cars.id WHERE cars.make = %s AND cars.model LIKE %s AND cars.first_license_year = %s AND cars.fuel_type = %s AND `' + find_range(data['engine']) + '` > 0', (data['make'], '%' + data['model'] + '%', data['year'], data['fuel']))
    total = [row['total'] for row in cursor.fetchall()]
    print(total)
    data = {}
    data['co2'] = int(sum([int(c) for c in co2]) / len(co2))
    data['total'] = int(sum([int(t) for t in total]) / len(total))
    cursor.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
