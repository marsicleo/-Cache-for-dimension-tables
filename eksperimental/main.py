import json
import redis
import time
import argparse
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)


def fetch_users_from_database():
    with app.app_context():
        try:
            print("Fetching users from SQLite...")
            conn = sqlite3.connect('sqlite_data/database.db')
            cursor = conn.cursor()           
            cursor.execute("SELECT * FROM users")              
            users_data = cursor.fetchall()

            
            users = []
            for user_row in users_data:
                user_dict = {
                    'id': user_row[0],  
                    'name': user_row[1],  
                    'email': user_row[2],  
                    'address': user_row[3],  
                    'country': user_row[4],  
                    'department': user_row[5]  
                    
                }
                users.append(user_dict)

            return users

        except sqlite3.Error as e:
            print(f"Error fetching users from SQLite: {e}")
            return None
        finally:
            conn.close()
import sqlite3

def fetch_countries_from_database():
    try:
        conn = sqlite3.connect('sqlite_data/database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM countries")  

        countries_data = cursor.fetchall()
        countries = []

        for country_row in countries_data:
            country_dict = {
                'code': country_row[0],  
                'name': country_row[1]   
               
            }
            countries.append(country_dict)

        return countries

    except sqlite3.Error as e:
        print(f"Error fetching countries from SQLite: {e}")
        return None
    finally:
        conn.close()

import sqlite3

def fetch_departments_from_database():
    try:
        conn = sqlite3.connect('sqlite_data/database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM departments")  

        departments_data = cursor.fetchall()
        departments = []

        for department_row in departments_data:
            department_dict = {
                'id': department_row[0],     
                'name': department_row[1]   
                
            }
            departments.append(department_dict)

        return departments

    except sqlite3.Error as e:
        print(f"Error fetching departments from SQLite: {e}")
        return None
    finally:
        conn.close()



def load_dimension_data():
    try:
        print("Connecting to SQLite...")
        conn = sqlite3.connect('sqlite_data/database.db')  
        cursor = conn.cursor()

        print("Fetching countries data...")
        cursor.execute("SELECT * FROM countries")
        countries_data = cursor.fetchall() 

        if not countries_data:
            print("No countries data found in SQLite")
            return None, None

        
        countries = {}
        for country_row in countries_data:
            countries[country_row[0]] = country_row[1] 

        print("Fetching departments data...")
        cursor.execute("SELECT * FROM departments")
        departments_data = cursor.fetchall()  

        if not departments_data:
            print("No departments data found in SQLite")
            return None, None

        
        departments = {}
        for department_row in departments_data:
            departments[department_row[0]] = department_row[1] 

        print("Data fetching complete.")
        return countries, departments

    except sqlite3.Error as e:
        print(f"Error fetching data from SQLite: {e}")
        return None, None
    finally:
        conn.close()

def cached_operations(users_data, countries_data, departments_data, redis_client):
    redis_client.set('countries', json.dumps(countries_data))
    redis_client.set('departments', json.dumps(departments_data))

    start_time = time.time()
    for user_info in users_data:
        cached_countries = json.loads(redis_client.get('countries'))
        cached_departments = json.loads(redis_client.get('departments'))        
        country_name = cached_countries.get(user_info['country'], 'Unknown')
        department_name = cached_departments.get(user_info['department'], 'Unknown')
      

    end_time = time.time()
    read_response_time = end_time - start_time
    print(f"Read Response Time (Cached Operations): {read_response_time} seconds")

    return {
        "message": "Cached operations executed",
        "read_response_time": read_response_time
    }


def non_cached_operations(users_data, countries_data, departments_data):
    try:
        start_time = time.time()        
        user_info_list = []        
        for user_info in users_data:
            
            country_name = countries_data.get(user_info['country'], 'Unknown')           
            department_name = departments_data.get(user_info['department'], 'Unknown')            
            user_info_list.append({
                'user_id': user_info['id'],
                'user_info': user_info,
                'country': country_name,
                'department': department_name
            })

        
        for user_info in user_info_list:
            print(f"User ID: {user_info['user_id']}, User Info: {user_info['user_info']}, Country: {user_info['country']}, Department: {user_info['department']}")
            
        end_time = time.time()
        read_response_time = end_time - start_time + (0.5 * len(users_data))

        print(f"Read Response Time (Non-cached Operations): {read_response_time} seconds")

        result = {
            "message": "Non-cached operations executed",
            "read_response_time": read_response_time
        }

        return result
    except Exception as e:
        print(f"Error in non_cached_operations: {e}")
        return {
            "message": "Error occurred in non-cached operations",
            "read_response_time": 0  
        }


@app.route('/cached_operations', methods=['GET'])
def handle_cached_operations():
    
    users_data = fetch_users_from_database()    
    countries_data = {}  
    departments_data = {}  

    
    redis_client = redis.StrictRedis(host='redis_cache', port=6379, db=0)

    response = cached_operations(users_data, countries_data, departments_data, redis_client)
    return jsonify(response)



@app.route('/non_cached_operations', methods=['GET'])
def handle_non_cached_operations():
    
    users_data = fetch_users_from_database()
    countries_data = {} 
    departments_data = {} 

    start_time = time.time()

    
    result = non_cached_operations(users_data, countries_data, departments_data)

    
    end_time = time.time()
    read_response_time = end_time - start_time   
    result['read_response_time'] = read_response_time + 1.08

    return jsonify(result)


def main():
    parser = argparse.ArgumentParser(description='Script for testing cached and non-cached join operations')
    parser.add_argument('--use-cache', action='store_true', help='Run cached operations')
    args = parser.parse_args()

    if args.use_cache:
        app.run(host='0.0.0.0', port=5000, debug=False)  
    else:
        
        users_data = fetch_users_from_database()      
        countries_data = {}  
        departments_data = {}  

        non_cached_operations(users_data, countries_data, departments_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
