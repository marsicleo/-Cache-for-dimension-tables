import sqlite3
import json


with open('mongo_data/countries.json', 'r') as country_file:
    countries_data = json.load(country_file)

with open('mongo_data/users.json', 'r') as user_file:
    users_data = json.load(user_file)

with open('mongo_data/departments.json', 'r') as department_file:
    departments_data = json.load(department_file)


conn = sqlite3.connect('./database.db')  
cursor = conn.cursor()




cursor.execute('''CREATE TABLE countries (
                    code TEXT PRIMARY KEY,
                    name TEXT
                 )''')

for code, name in countries_data.items():
    cursor.execute('''INSERT INTO countries (code, name) VALUES (?, ?)''', (code, name))


cursor.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    address TEXT,
                    country_code TEXT,
                    department TEXT,
                    FOREIGN KEY(country_code) REFERENCES countries(code)
                 )''')

for user_id, user_info in users_data.items():
    cursor.execute('''INSERT INTO users (name, email, address, country_code, department)
                      VALUES (?, ?, ?, ?, ?)''', (user_info['name'], user_info['email'],
                                                 user_info['address'], user_info['country'],
                                                 user_info['department']))


cursor.execute('''CREATE TABLE departments (
                    name TEXT PRIMARY KEY,
                    description TEXT
                 )''')

for department_name, description in departments_data.items():
    cursor.execute('''INSERT INTO departments (name, description) VALUES (?, ?)''', (department_name, description))


conn.commit()
conn.close()
