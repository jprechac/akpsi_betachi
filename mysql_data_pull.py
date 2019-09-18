import json
import mysql.connector as sql

db = sql.connect(user='python', password='python',
                host='127.0.0.1', database='akpsi')

cursor = db.cursor()

sem_query = "SELECT * FROM semester"

cursor.execute(sem_query)

semesters = []
for row in cursor:
    # print(row)
    record = {
        "model": "akpsi_core.semester",
        "pk": row[0],
        "fields": {
            "semester_term": row[1],
            "semester_year": row[2]
        }
    }

    if row[5] != None:
        record['fields'].update({"beginning_actives": row[5]})
    if row[6] != None:
        record['fields'].update({"applications": row[6]})
    
    semesters.append(record)


with open('akpsi_core/fixtures/semester.json', 'w') as file:
    json.dump(semesters, file)
