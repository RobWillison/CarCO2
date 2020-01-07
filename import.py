import csv
import pymysql.cursors
import re

def import_file(filename, year):
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='vehicle_emissions',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_NAME`='dataset';")

    columns_names = [r['COLUMN_NAME'].lower() for r in cursor.fetchall()]

    with open(file, 'r', encoding='utf-8', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(spamreader)

        for header in headers:
            if header == '':
                continue
            if not header.lower() in columns_names:
                sql = "ALTER TABLE dataset ADD COLUMN `" + header + "` TEXT"
                cursor.execute(sql)
                connection.commit()

        for row in spamreader:
            columns = []
            data = []
            for i in range(len(row)):
                if len(row) <= i or len(headers) <= i or row[i] == '' or headers[i] == '':
                    continue
                data.append(row[i])
                columns.append(headers[i])
            colunmns = ','.join(['`' + h +'`' for h in columns])
            placeholders = ','.join(['%s' for d in data])
            if len(data) == 0:
                continue
            sql = "INSERT INTO `dataset` (`year`, " + colunmns + ") VALUES (" + year + ", " + placeholders + ")"
            print(sql)
            cursor.execute(sql, data)


    connection.commit()



import glob, os
os.chdir("data")
for file in glob.glob("*.csv"):
    print(file)
    year = (re.search("[0-9]{4}", file) or ['NULL'])[0]
    print(year)
    import_file(file, year)
