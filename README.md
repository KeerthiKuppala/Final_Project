# Clinical Data Warehouse System

## Overview
The Clinical Data Warehouse System is a Python application designed to manage patient information in a hospital setting. It provides functionalities such as adding, removing, and retrieving patient records, counting visits on a specific date, generating key statistics, and logging user actions.
## How to Run
You can run my code using the syntax "Python Keerthi_Project.py"

Ensure you have Python 3 installed on your system.
Navigate to the directory containing the Python files.
Install the required packages
we have use the TKinter package (https://docs.python.org/3/library/tkinter.html)

6. Follow the on-screen instructions to log in and use the application.

## Packages Required

- `tkinter`: Python's standard GUI (Graphical User Interface) toolkit.

## Functionality

1. **Login**: Users can log in with their username and password. Different roles such as management, clinician, nurse, and admin are supported, each with different access permissions.

2. **Add Patient**: Users can add new patient records to the system. If a patient with the provided ID already exists, the user is prompted to enter visit details.

3. **Remove Patient**: Users can remove existing patient records from the system.

4. **Retrieve Patient**: Users can retrieve and view detailed information about a specific patient, including their demographic data and visit history.

5. **Count Visits**: Users can count the total number of visits on a specific date.

6. **Generate Key Statistics**: Management and admin users can generate key statistics such as total patients, patients by insurance, gender, race, ethnicity, and visit department.

7. **Logging**: All user actions are logged, including login attempts and performed actions. These logs are stored in a usage statistics file.

## Additional Information

- The program reads and writes patient information to a CSV file named `Project_patient_information.csv`.
- Usage statistics and user logs are stored in a separate file 'usage_statistics.csv' for auditing and tracking purposes.
- Ensure that the CSV files have the appropriate permissions for reading and writing.
- For any issues or feedback, please contact me.

