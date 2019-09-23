from datetime import datetime
import json
import mysql.connector as sql

db = sql.connect(user='python', password='python',
                host='127.0.0.1', database='akpsi')

cursor = db.cursor()

# print(type(cursor))

# -----------------------------------------------------------------------------
# function definitions

def get_semester_data(data, cursor):
    sem_query = "SELECT * FROM semester"
    cursor.execute(sem_query)

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

        if row[3] != None:
            s = row[3].strftime("%Y-%m-%d")
            record['fields'].update({"semester_induction": s})
        if row[4] != None:
            s = row[4].strftime("%Y-%m-%d")
            record['fields'].update({"semester_initiation": s})
        if row[5] != None:
            record['fields'].update({"beginning_actives": row[5]})
        if row[6] != None:
            record['fields'].update({"applications": row[6]})
        if row[7] != None:
            record['fields'].update({"prospect_interviews": row[7]})
        if row[8] != None:
            record['fields'].update({"bids_extended": row[8]})
        if row[9] != None:
            record['fields'].update({"pledges_pinned": row[9]})
        if row[10] != None:
            record['fields'].update({"brothers_initiated": row[10]})
        if row[11] != None:
            record['fields'].update({"sponsorships": row[11]})
        if row[12] != None:
            record['fields'].update({"fundraising": row[12]})
        
        data.append(record)

    return data

def get_chapter_data(data, cursor):

    stuff = [{"model": "akpsi_core.university","pk": "Louisiana State University","fields": {"university_city": "Baton Rouge","university_state": "Louisiana","university_country": "United States"}},{"model": "akpsi_core.area","pk": 4,"fields":{}},{"model": "akpsi_core.region","pk": "Southern Delta","fields": {"area_number": 4}},{"model": "akpsi_core.chapter","pk": "Beta Chi","fields":{"chapter_university": "Louisiana State University","region_name": "Southern Delta"}},{"model": "akpsi_core.area","pk": 1,"fields":{}},{"model": "akpsi_core.area","pk": 2,"fields":{}},{"model": "akpsi_core.area","pk": 3,"fields":{}}]
    for i in stuff:
        data.append(i)

    return data

def get_officer_data(data, cursor):
    # this is a temp set, update to pull from db later
    stuff = [
        {
            "model": "akpsi_core.officer",
            "pk": 1,
            "fields": {
                "member_code": "f16joprc",
                "sem_code": "F2017",
                "position": "evp"
            }
        },
        {
            "model": "akpsi_core.officer",
            "pk": 2,
            "fields": {
                "member_code": "f16joprc",
                "sem_code": "S2018",
                "position": "evp"
            }
        }
    ]
    for i in stuff:
        data.append(i)
    return data

# -----------------------------------------------------------------------------
# main shit

data = []

data = get_semester_data(data, cursor)
data = get_chapter_data(data, cursor)
data = get_officer_data(data, cursor)

with open('akpsi_core/fixtures/data.json', 'w') as file:
    json.dump(data, file)