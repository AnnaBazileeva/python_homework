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

