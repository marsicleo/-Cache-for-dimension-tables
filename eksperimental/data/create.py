from faker import Faker
import json
import random


fake = Faker()

countries_data = {
    'USA': 'United States',
    'CAN': 'Canada',
    'UK': 'United Kingdom',
    'ZMB': 'Zambia',
    'FRA': 'France',
    'GER': 'Germany',
    'AUS': 'Australia',
    'JPN': 'Japan',
    'BRA': 'Brazil',
    'ITA': 'Italy',
    'CHN': 'China',
    'IND': 'India',
    'RUS': 'Russia'
    
}


with open('data/countries.json', 'w') as country_file:
    json.dump(countries_data, country_file, indent=4)


users_data = {}
for i in range(1, 100001): 
    user_key = f'user_{i}'
    users_data[user_key] = {
        'name': fake.name(),
        'email': fake.email(),
        'address': fake.address(),
        'country': random.choice(list(countries_data.keys())),
        'department': fake.random_element(elements=('Sales', 'Marketing', 'IT', 'HR'))
        
    }


with open('data/users.json', 'w') as user_file:
    json.dump(users_data, user_file, indent=4)


departments_data = {
    'Sales': 'Sales Department',
    'Marketing': 'Marketing Department',
    'IT': 'IT Department',
    'HR': 'Human Resources Department'
    
}


with open('data/departments.json', 'w') as department_file:
    json.dump(departments_data, department_file, indent=4)
