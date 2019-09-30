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

def get_member_data(data, cursor):
    mem_query = "SELECT * FROM akpsi.membership m WHERE m.chapter = 'Beta Chi'"
    cursor.execute(mem_query)

    for row in cursor:
        # print(row)

        # convert ISDS to fully written out
        if row[11] == 'ISDS':
            major = "Information Systems and Decision Sciences"
        else:
            major = row[11]
        
        # convert active status to collegiate
        if row[5] == 'Active':
            status = "Collegiate"
        else:
            status = row[5]
        
        # convert genders to single characters
        if row[18] == "Male":
            gender = 'm'
        elif row[18] == 'Female':
            gender = 'f'
        else:
            gender = None

        # convert birthday to string
        if row[17] != None:
            birthday = row[17].strftime("%Y-%m-%d")
        else: birthday = None

        record = {
            "model": "akpsi_core.member",
            "pk": row[0],
            "fields": {
                "first_name": row[1],
                "middle_name": row[2],
                "last_name": row[3],
                "nickname": row[4],
                "akpsi_status": status,
                "chapter_status": row[6],
                'chapter': row[7],
                "email1": row[8],
                "email2": row[9],
                "phone": row[10],
                'major': major,
                "pledge_classification": row[12],
                "pledge_semester": row[13],
                "graduate_semester": row[14],
                "suspension_semester": row[15],
                "reinstate_semester": row[16],
                "birthday": birthday, # convert the datetime to a string
                "gender": gender,
                "dietary_restrictions": row[19],
                "home_city": row[20],
                "home_state": row[21],
                "home_country": row[22],
                "graduate_program": row[23],
                # "graduate_university": row[24], #wrong index?
                "work_company": row[25],
                "work_city": row[26],
                "work_state": row[27],
                "work_country": row[28],
                "notes": row[29]
            }
        }

        data.append(record)
    return data

# -----------------------------------------------------------------------------
# main shit

data = []
member_data = []

data = get_semester_data(data, cursor)
data = get_chapter_data(data, cursor)
data = get_officer_data(data, cursor)

with open('akpsi_core/fixtures/data.json', 'w') as dFile:
    json.dump(data, dFile)


member_data = get_member_data(member_data, cursor)
# print(member_data)

with open('akpsi_core/fixtures/member_data.json', 'w') as memFile:
    json.dump(member_data, memFile)

# cursor.execute("SELECT * FROM akpsi.college")
# for row in cursor:
#     print(row)