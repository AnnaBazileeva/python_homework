import csv

with open('../csv/employees.csv', 'r') as file:
    reader = csv.reader(file)
    employees = list(reader)

employee_names = [f"{row[1]} {row[2]}" for row in employees[1:]]

print("All employee names:")
print(employee_names)

names_with_e = [name for name in employee_names if 'e' in name]

print("\nNames containing 'e':")
print(names_with_e)
