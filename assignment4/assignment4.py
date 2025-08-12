#task1

import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print("Original DataFrame:")
print(task1_data_frame)
print()

task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print("DataFrame with Salary:")
print(task1_with_salary)
print()

task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print("DataFrame with incremented Age:")
print(task1_older)
print()

task1_older.to_csv('employees.csv', index=False)
print("DataFrame saved to employees.csv")
print("CSV file contents:")
with open('employees.csv', 'r') as f:
    print(f.read())

#task2

task2_employees = pd.read_csv('employees.csv')
print("Employees loaded from CSV:")
print(task2_employees)
print()

import json

additional_data = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open('additional_employees.json', 'w') as f:
    json.dump(additional_data, f)

json_employees = pd.read_json('additional_employees.json')
print("Employees loaded from JSON:")
print(json_employees)
print()

more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print("Combined employees:")
print(more_employees)
print()


#task3

first_three = more_employees.head(3)
print("First three employees:")
print(first_three)
print()

last_two = more_employees.tail(2)
print("Last two employees:")
print(last_two)
print()

employee_shape = more_employees.shape
print("Shape of DataFrame:")
print(employee_shape)
print()

print("DataFrame info:")
more_employees.info()
