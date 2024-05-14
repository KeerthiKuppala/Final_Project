import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
import random
import string

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Patient:
    def __init__(self, patient_id, gender, race, age, ethnicity, insurance, zip_code):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

class Visit:
    def __init__(self, visit_id, visit_time, department, chief_complaint):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.chief_complaint = chief_complaint
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

class Note:
    def __init__(self, note_id, note_type):
        self.note_id = note_id
        self.note_type = note_type

class Hospital:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]
            print("Patient and associated records removed successfully.")
        else:
            print("Patient not found.")

    def retrieve_patient(self, patient_id):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            return patient
        else:
            return None

    def count_visits_on_date(self, date):
        total_visits = 0
        for patient in self.patients.values():
            for visit in patient.visits:
                if visit.visit_time.date() == date.date():
                    total_visits += 1
        return total_visits

    def get_patient_count_by_insurance(self):
        insurance_count = {}
        for patient in self.patients.values():
            if patient.insurance not in insurance_count:
                insurance_count[patient.insurance] = 1
            else:
                insurance_count[patient.insurance] += 1
        return insurance_count

    def get_patient_count_by_demographics(self, attribute):
        count_by_attribute = {}
        for patient in self.patients.values():
            value = getattr(patient, attribute)
            if value not in count_by_attribute:
                count_by_attribute[value] = 1
            else:
                count_by_attribute[value] += 1
        return count_by_attribute

    def get_patient_count_by_department(self):
        department_count = {}
        for patient in self.patients.values():
            for visit in patient.visits:
                department = visit.department
                if department not in department_count:
                    department_count[department] = 1
                else:
                    department_count[department] += 1
        return department_count

def read_patient_data(file_path):
    hospital = Hospital()
    with open(file_path, 'r') as file:
        if file_path.lower().endswith('.csv'):
            reader = csv.DictReader(file)
            for row in reader:
                patient_id = row.get('Patient_ID')
                if patient_id:
                    gender = row.get('Gender', '')
                    race = row.get('Race', '')
                    age = int(row.get('Age', 0))
                    ethnicity = row.get('Ethnicity', '')
                    insurance = row.get('Insurance', '')
                    zip_code = row.get('Zip_code', '')  # Check if Zip_code exists
                    patient = Patient(patient_id, gender, race, age, ethnicity, insurance, zip_code)
                    hospital.add_patient(patient)
                    visit_id = row.get('Visit_ID', '')
                    visit_time_str = row.get('Visit_time', '')
                    visit_time = datetime.strptime(visit_time_str, '%Y-%m-%d') if visit_time_str else None
                    visit_department = row.get('Visit_department', '')
                    chief_complaint = row.get('Chief_complaint', '')
                    if visit_id and visit_time and visit_department and chief_complaint:
                        visit = Visit(visit_id, visit_time, visit_department, chief_complaint)
                        patient.add_visit(visit)
    return hospital


def write_patient_data(file_path, hospital):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Patient_ID', 'Gender', 'Race', 'Age', 'Ethnicity', 'Insurance', 'Zip code', 'Visit_ID', 'Visit_time', 'Visit_department', 'Chief_complaint'])
        for patient in hospital.patients.values():
            for visit in patient.visits:
                writer.writerow([patient.patient_id, patient.gender, patient.race, patient.age, patient.ethnicity, patient.insurance, patient.zip_code, visit.visit_id, visit.visit_time.strftime('%Y-%m-%d'), visit.department, visit.chief_complaint])

def generate_key_statistics(hospital):
    # Generate and display key statistics
    total_patients = len(hospital.patients)
    insurance_count = hospital.get_patient_count_by_insurance()
    gender_count = hospital.get_patient_count_by_demographics('gender')
    race_count = hospital.get_patient_count_by_demographics('race')
    ethnicity_count = hospital.get_patient_count_by_demographics('ethnicity')
    department_count = hospital.get_patient_count_by_department()

    key_stats = f"Total Patients: {total_patients}\n"
    key_stats += "Patients by Insurance:\n"
    for insurance, count in insurance_count.items():
        key_stats += f"{insurance}: {count}\n"

    key_stats += "\nPatients by Gender:\n"
    for gender, count in gender_count.items():
        key_stats += f"{gender}: {count}\n"

    key_stats += "\nPatients by Race:\n"
    for race, count in race_count.items():
        key_stats += f"{race}: {count}\n"

    key_stats += "\nPatients by Ethnicity:\n"
    for ethnicity, count in ethnicity_count.items():
        key_stats += f"{ethnicity}: {count}\n"

    key_stats += "\nPatients by Visit Department:\n"
    for department, count in department_count.items():
        key_stats += f"{department}: {count}\n"

    return key_stats


def add_patient_ui(hospital, patient_id, visit_time, visit_department, chief_complaint):
    if patient_id in hospital.patients:
        # Generate a unique visit ID
        visit_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Create a new visit instance
        visit = Visit(visit_id, datetime.strptime(visit_time, '%Y-%m-%d'), visit_department, chief_complaint)

        # Add the visit to the patient's records
        hospital.patients[patient_id].add_visit(visit)

        return "Patient visit added successfully."
    else:
        return "Patient not found."

def remove_patient_ui(hospital, patient_id):
    if patient_id in hospital.patients:
        hospital.remove_patient(patient_id)
        return "Patient and associated records removed successfully."
    else:
        return "Patient not found."

def retrieve_patient_ui(hospital, patient_id):
    patient = hospital.retrieve_patient(patient_id)
    if patient:
        patient_info = f"Patient information for ID: {patient_id}\n"
        patient_info += f"Gender: {patient.gender}\n"
        patient_info += f"Race: {patient.race}\n"
        patient_info += f"Age: {patient.age}\n"
        patient_info += f"Ethnicity: {patient.ethnicity}\n"
        patient_info += f"Insurance: {patient.insurance}\n"
        patient_info += f"Zip code: {patient.zip_code}\n"
        patient_info += "Visits:\n"
        for visit in patient.visits:
            patient_info += f"Visit ID: {visit.visit_id}\n"
            patient_info += f"Visit time: {visit.visit_time.strftime('%Y-%m-%d')}\n"
            patient_info += f"Department: {visit.department}\n"
            patient_info += f"Chief complaint: {visit.chief_complaint}\n"
        return patient_info
    else:
        return "Patient not found."

def count_visits_ui(hospital, visit_date):
    try:
        visit_date = datetime.strptime(visit_date, '%Y-%m-%d')
        total_visits = hospital.count_visits_on_date(visit_date)
        return f"Total visits on {visit_date.strftime('%Y-%m-%d')}: {total_visits}"
    except ValueError:
        return "Invalid date format. Please enter date in YYYY-MM-DD format."

def validate_login(username, password):
    # Modify for your own credential validation
    valid_users = read_users('Project_credentials.csv')
    for user in valid_users:
        if user.username == username and user.password == password:
            return user.role
    return None

def read_users(file_path):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Fetch values based on column names
            username = row.get('username')
            password = row.get('password')
            role = row.get('role')
            users.append(User(username, password, role))
    return users

def write_usage_statistics(file_path, username, role, action):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, role, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), action])

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 700

def main():
    root = tk.Tk()
    root.title("Clinical Data Warehouse")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    hospital = None
    current_user_role = None

    def login():
        nonlocal hospital, current_user_role
        username = username_entry.get()
        password = password_entry.get()
        role = validate_login(username, password)
        if role:
            messagebox.showinfo("Login Successful", f"Welcome, {role}!")
            current_user_role = role
            hospital = read_patient_data('Project_patient_information.csv')
            show_menu()
            write_usage_statistics('usage_statistics.csv', username, role, 'Login')
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            write_usage_statistics('usage_statistics.csv', username, 'Unknown', 'Failed Login Attempt')

    def show_menu():
        menu_window = tk.Toplevel(root)
        menu_window.title("Menu")
        menu_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        if current_user_role == "management":
            generate_statistics_button = tk.Button(menu_window, text="Generate Key Statistics", command=generate_key_stats)
            generate_statistics_button.pack(pady=10)
        elif current_user_role in ["clinician", "nurse"]:
            retrieve_patient_button = tk.Button(menu_window, text="Retrieve Patient", command=retrieve_patient)
            retrieve_patient_button.pack(pady=10)

            add_patient_button = tk.Button(menu_window, text="Add Patient", command=add_patient)
            add_patient_button.pack(pady=10)

            remove_patient_button = tk.Button(menu_window, text="Remove Patient", command=remove_patient)
            remove_patient_button.pack(pady=10)

            count_visits_button = tk.Button(menu_window, text="Count Visits", command=count_visits)
            count_visits_button.pack(pady=10)

        elif current_user_role == "admin":
            count_visits_button = tk.Button(menu_window, text="Count Visits", command=count_visits)
            count_visits_button.pack(pady=10)

        exit_button = tk.Button(menu_window, text="Exit", command=root.destroy)
        exit_button.pack(pady=10)

        menu_window.mainloop()


    def generate_key_stats():
        if current_user_role in ["admin", "management"]:
            stats = generate_key_statistics(hospital)
            messagebox.showinfo("Key Statistics", stats)
            write_usage_statistics('usage_statistics.csv', username_entry.get(), current_user_role, 'Generate Key Statistics')
        else:
            messagebox.showerror("Unauthorized", "You are not authorized to view key statistics.")

    def add_patient():
        add_patient_window = tk.Toplevel(root)
        add_patient_window.title("Add Patient")
        add_patient_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        patient_id_label = tk.Label(add_patient_window, text="Patient ID:")
        patient_id_label.grid(row=0, column=0, padx=10, pady=10)

        patient_id_entry = tk.Entry(add_patient_window)
        patient_id_entry.grid(row=0, column=1, padx=10, pady=10)

        check_patient_button = tk.Button(add_patient_window, text="Check Patient", command=lambda: check_patient(patient_id_entry.get(), add_patient_window))
        check_patient_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def check_patient(patient_id, window):
        if patient_id in hospital.patients:
            visit_time_window = tk.Toplevel(window)
            visit_time_window.title("Enter Visit Time")
            visit_time_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

            visit_time_label = tk.Label(visit_time_window, text="Visit Time (YYYY-MM-DD):")
            visit_time_label.grid(row=0, column=0, padx=10, pady=10)

            visit_time_entry = tk.Entry(visit_time_window)
            visit_time_entry.grid(row=0, column=1, padx=10, pady=10)

            visit_department_label = tk.Label(visit_time_window, text="Visit Department:")
            visit_department_label.grid(row=1, column=0, padx=10, pady=10)

            visit_department_entry = tk.Entry(visit_time_window)
            visit_department_entry.grid(row=1, column=1, padx=10, pady=10)

            chief_complaint_label = tk.Label(visit_time_window, text="Chief Complaint:")
            chief_complaint_label.grid(row=2, column=0, padx=10, pady=10)

            chief_complaint_entry = tk.Entry(visit_time_window)
            chief_complaint_entry.grid(row=2, column=1, padx=10, pady=10)

            add_visit_button = tk.Button(visit_time_window, text="Add Visit", command=lambda: add_visit(patient_id, visit_time_entry.get(), visit_department_entry.get(), chief_complaint_entry.get(), visit_time_window))
            add_visit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        else:
            add_patient_details(patient_id, window)

    def add_patient_details(patient_id, window):
        add_patient_details_window = tk.Toplevel(window)
        add_patient_details_window.title("Add Patient Details")
        add_patient_details_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        gender_label = tk.Label(add_patient_details_window, text="Gender:")
        gender_label.grid(row=0, column=0, padx=10, pady=10)

        gender_entry = tk.Entry(add_patient_details_window)
        gender_entry.grid(row=0, column=1, padx=10, pady=10)

        race_label = tk.Label(add_patient_details_window, text="Race:")
        race_label.grid(row=1, column=0, padx=10, pady=10)

        race_entry = tk.Entry(add_patient_details_window)
        race_entry.grid(row=1, column=1, padx=10, pady=10)

        age_label = tk.Label(add_patient_details_window, text="Age:")
        age_label.grid(row=2, column=0, padx=10, pady=10)

        age_entry = tk.Entry(add_patient_details_window)
        age_entry.grid(row=2, column=1, padx=10, pady=10)

        ethnicity_label = tk.Label(add_patient_details_window, text="Ethnicity:")
        ethnicity_label.grid(row=3, column=0, padx=10, pady=10)

        ethnicity_entry = tk.Entry(add_patient_details_window)
        ethnicity_entry.grid(row=3, column=1, padx=10, pady=10)

        insurance_label = tk.Label(add_patient_details_window, text="Insurance:")
        insurance_label.grid(row=4, column=0, padx=10, pady=10)

        insurance_entry = tk.Entry(add_patient_details_window)
        insurance_entry.grid(row=4, column=1, padx=10, pady=10)

        zip_code_label = tk.Label(add_patient_details_window, text="Zip Code:")
        zip_code_label.grid(row=5, column=0, padx=10, pady=10)

        zip_code_entry = tk.Entry(add_patient_details_window)
        zip_code_entry.grid(row=5, column=1, padx=10, pady=10)

        visit_time_label = tk.Label(add_patient_details_window, text="Visit Time (YYYY-MM-DD):")
        visit_time_label.grid(row=6, column=0, padx=10, pady=10)

        visit_time_entry = tk.Entry(add_patient_details_window)
        visit_time_entry.grid(row=6, column=1, padx=10, pady=10)

        visit_department_label = tk.Label(add_patient_details_window, text="Visit Department:")
        visit_department_label.grid(row=7, column=0, padx=10, pady=10)

        visit_department_entry = tk.Entry(add_patient_details_window)
        visit_department_entry.grid(row=7, column=1, padx=10, pady=10)

        chief_complaint_label = tk.Label(add_patient_details_window, text="Chief Complaint:")
        chief_complaint_label.grid(row=8, column=0, padx=10, pady=10)

        chief_complaint_entry = tk.Entry(add_patient_details_window)
        chief_complaint_entry.grid(row=8, column=1, padx=10, pady=10)

        add_patient_button = tk.Button(add_patient_details_window, text="Add Patient", command=lambda: add_patient_with_details(patient_id, gender_entry.get(), race_entry.get(), age_entry.get(), ethnicity_entry.get(), insurance_entry.get(), zip_code_entry.get(), visit_time_entry.get(), visit_department_entry.get(), chief_complaint_entry.get(), add_patient_details_window))
        add_patient_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def add_patient_with_details(patient_id, gender, race, age, ethnicity, insurance, zip_code, visit_time, visit_department, chief_complaint, window):
        patient = Patient(patient_id, gender, race, int(age), ethnicity, insurance, zip_code)
        hospital.add_patient(patient)
        add_patient_ui(hospital, patient_id, visit_time, visit_department, chief_complaint)
        messagebox.showinfo("Patient Added", "Patient added successfully.")
        window.destroy()
        write_patient_data('Project_patient_information.csv', hospital)
        write_usage_statistics('usage_statistics.csv', username_entry.get(), current_user_role, 'Add Patient')
        show_menu()  # Return to menu after action

    def add_visit(patient_id, visit_time, visit_department, chief_complaint, window):
        result = add_patient_ui(hospital, patient_id, visit_time, visit_department, chief_complaint)
        messagebox.showinfo("Add Visit", result)
        window.destroy()
        write_patient_data('Project_patient_information.csv', hospital)
        write_usage_statistics('usage_statistics.csv', username_entry.get(), current_user_role, 'Add Visit')
        show_menu()  # Return to menu after action

    def remove_patient():
        remove_patient_window = tk.Toplevel(root)
        remove_patient_window.title("Remove Patient")
        remove_patient_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        patient_id_label = tk.Label(remove_patient_window, text="Patient ID:")
        patient_id_label.pack(pady=10)

        patient_id_entry = tk.Entry(remove_patient_window)
        patient_id_entry.pack(pady=10)

        remove_button = tk.Button(remove_patient_window, text="Remove", command=lambda: remove(patient_id_entry.get(), remove_patient_window))
        remove_button.pack(pady=10)

    def remove(patient_id, window):
        result = remove_patient_ui(hospital, patient_id)
        messagebox.showinfo("Remove Patient", result)
        window.destroy()
        write_patient_data('Project_patient_information.csv', hospital)
        write_usage_statistics('usage_statistics.csv', username_entry.get(), current_user_role, 'Remove Patient')
        show_menu()  # Return to menu after action

    def retrieve_patient():
        retrieve_patient_window = tk.Toplevel(root)
        retrieve_patient_window.title("Retrieve Patient")
        retrieve_patient_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        patient_id_label = tk.Label(retrieve_patient_window, text="Patient ID:")
        patient_id_label.pack(pady=10)

        patient_id_entry = tk.Entry(retrieve_patient_window)
        patient_id_entry.pack(pady=10)

        retrieve_button = tk.Button(retrieve_patient_window, text="Retrieve", command=lambda: retrieve(patient_id_entry.get(), retrieve_patient_window))
        retrieve_button.pack(pady=10)

    def retrieve(patient_id, window):
        result = retrieve_patient_ui(hospital, patient_id)
        messagebox.showinfo("Retrieve Patient", result)
        window.destroy()
        write_usage_statistics('usage_statistics.csv', username_entry.get(), current_user_role, 'Retrieve Patient')
        show_menu()  # Return to menu after action

    def count_visits():
        count_visits_window = tk.Toplevel(root)
        count_visits_window.title("Count Visits")
        count_visits_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        visit_date_label = tk.Label(count_visits_window, text="Visit Date (YYYY-MM-DD):")
        visit_date_label.pack(pady=10)

        visit_date_entry = tk.Entry(count_visits_window)
        visit_date_entry.pack(pady=10)

        count_button = tk.Button(count_visits_window, text="Count Visits", command=lambda: count(visit_date_entry.get(), count_visits_window))
        count_button.pack(pady=10)

    def count(visit_date, window):
        result = count_visits_ui(hospital, visit_date)
        messagebox.showinfo("Count Visits", result)
        window.destroy()
        write_usage_statistics('usage_statistics.csv', username_entry.get(), current_user_role, 'Count Visits')
        show_menu()  # Return to menu after action

    login_frame = tk.Frame(root)
    login_frame.pack(pady=50)

    username_label = tk.Label(login_frame, text="Username:")
    username_label.grid(row=0, column=0, padx=10, pady=10)

    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = tk.Label(login_frame, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10)

    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
