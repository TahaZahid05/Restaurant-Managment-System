import pyodbc

# Replace these with your own database connection details
server = 'TAHA\\SQLSERVER1'
database = 'Northwind'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = 'Fall2022.dbms'  # Specify a password if not using Windows Authentication


# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish a connection to the database
connection = pyodbc.connect(connection_string)

# Create a cursor to interact with the database
cursor = connection.cursor()

# CREATE - Insert a new employee record
new_employee = (
    'Doe',
    'John',
    'Sales Manager',
    'Mr.',
    '1975-01-15',
    '2023-10-06',
    '123 Main St',
    'New York',
    'NY',
    '10001',
    'USA',
    '555-123-4567',
    '1234',
    None,  # You can insert the binary image data for the "Photo" field here if needed
    'Notes about John Doe',
    2,  # Replace with the actual ReportsTo value if applicable
    'images/johndoe.jpg'  # Update with the actual file path for the "PhotoPath" field
)
insert_query = """
    INSERT INTO Employees
    ([LastName], [FirstName], [Title], [TitleOfCourtesy], [BirthDate], [HireDate],
    [Address], [City], [Region], [PostalCode], [Country], [HomePhone], [Extension],
    [Photo], [Notes], [ReportsTo], [PhotoPath])
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
cursor.execute(insert_query, new_employee)
connection.commit()  # Commit the transaction

# READ - Fetch and print all employees
select_query = "SELECT FirstName,LastName FROM Employees"
cursor.execute(select_query)
print("All Employees:")
for row in cursor.fetchall():
    print(row)

# # UPDATE - Update an employee record
# update_query = "UPDATE Employees SET Region = ? WHERE FirstName = ? AND LastName = ?"
# updated_region = 'WA'
# cursor.execute(update_query, (updated_region, 'John', 'Doe'))
# connection.commit()  # Commit the transaction

# # READ - Fetch and print the updated employee
# cursor.execute("select FirstName,LastName, Region from Employees WHERE FirstName = ? AND LastName = ?",('John', 'Doe'))
# print("\nUpdated Employee:")
# for row in cursor.fetchall():
#     print(row)

# # DELETE - Delete an employee record
# delete_query = "DELETE FROM Employees WHERE FirstName = ? AND LastName = ?"
# cursor.execute(delete_query, ('John', 'Doe'))
# connection.commit()  # Commit the transaction

# # READ - Fetch and print all employees after deletion
# cursor.execute(select_query)
# print("\nEmployees After Deletion:")
# for row in cursor.fetchall():
#     print(row)

# Close the cursor and connection
cursor.close()
connection.close()
