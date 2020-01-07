import pymysql.cursors
import re

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='vehicle_emissions',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
# cursor.execute("SELECT * FROM `car_counts` WHERE `Model 1` != 'Missing'")
#
# for row in cursor.fetchall():
#     cursor.execute("SELECT * FROM `car_years` WHERE `Make` = %s AND `Model 1` = %s", (row['Make'], row['Model 1']))
#     year_row = cursor.fetchone()
#
#     cursor.execute("INSERT INTO cars (`make`, `model`, `description`, `fuel_type`) VALUES (%s, %s, %s, %s)", (row['Make'], year_row['Generic model 1'], year_row['Model 1'], row['Fuel Type'], ))
#     last_id = cursor.lastrowid
#     cursor.execute("UPDATE car_counts SET car_id = %s WHERE id = %s", (last_id, row['id']))
#     cursor.execute("UPDATE car_years SET car_id = %s WHERE id = %s", (last_id, year_row['id']))
#     connection.commit()


cursor.execute("SELECT * FROM `car_years` WHERE car_id IS NOT NULL")
for row in cursor.fetchall():
    for year in range(1900, 2019):
        if row[str(year)] == '' or row[str(year)] == None:
            continue
        if int(row[str(year)]) > 0.05 * int(row['Total']):
            cursor.execute("UPDATE cars SET first_license_year = %s WHERE id = %s", (year, row['car_id']))
            break
connection.commit()
