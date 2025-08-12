#task1
import json
import pandas as pd
import numpy as np

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print("Original DataFrame:")
print(task1_data_frame)

task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print("DataFrame with Salary:")
print(task1_with_salary)

task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print("DataFrame with incremented Age:")
print(task1_older)

task1_older.to_csv('employees.csv', index=False)
print("DataFrame saved to employees.csv")
print("CSV file contents:")
with open('employees.csv', 'r') as f:
    print(f.read())

#task2

task2_employees = pd.read_csv('employees.csv')
print("Employees loaded from CSV:")
print(task2_employees)

additional_data = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open('additional_employees.json', 'w') as f:
    json.dump(additional_data, f)

json_employees = pd.read_json('additional_employees.json')
print("Employees loaded from JSON:")
print(json_employees)

more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print("Combined employees:")
print(more_employees)


#task3

first_three = more_employees.head(3)
print("First three employees:")
print(first_three)

last_two = more_employees.tail(2)
print("Last two employees:")
print(last_two)

employee_shape = more_employees.shape
print("Shape of DataFrame:")
print(employee_shape)

print("DataFrame info:")
more_employees.info()

#task4

dirty_data = pd.read_csv('/Users/anna/IdeaProjects/python_homework/assignment3/dirty_data.csv')
print(dirty_data)

clean_data = dirty_data.copy()
print(clean_data)


clean_data = clean_data.drop_duplicates()
print("After removing duplicates:")
print(clean_data)

clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print("\n=== Age to Numeric ===")
print(clean_data)

clean_data["Salary"] = clean_data["Salary"].replace(["unknown", "n/a"], np.nan)
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors="coerce")
print("\n=== Salary to Numeric ===")
print(clean_data)

clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print("After filling missing values:")
print(clean_data)

clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce')
print("\n=== Hire Date to Datetime ===")
print(clean_data)

clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print("Final Cleaned Data:")
print(clean_data)
