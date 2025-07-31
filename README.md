# Creating a Project
 
1. Create a folder, name it appropriately, open the folder in VS Code, and run the following command in the terminal to create a virtual environment (you can choose your own name for the environment):
    ```
    python -m venv venv
    ```
 
2. Activate the virtual environment by running the command (replace env with your environment name if different):
    ```
    .\env\Scripts\activate
    ```
 
3. Install the required packages from requirements.txt:
    ```
    pip install -r requirements.txt
    ```
 
4. Create the main Django project by running:
    ```
    django-admin startproject congig
    ```
 
5. Create a sub-apps using the command:
    ```
    python manage.py startapp users
 
    ```
 
6. Register the sub-app:
    
    - Open settings.py in the main project folder (config) and add 'users'  to the INSTALLED_APPS list.
    
7. Define your models:

   - Open models.py inside the user and define the database tables you need.
 
8. Apply the migrations:
   - Run the following commands to create and apply the database migrations:
    ```
    python manage.py makemigrations
 
    python manage.py migrate
    ```
 
9. To start the Django development server, run the following command:
    ```
    python manage.py runserver
    ```
   
10. API Endpoints:

| Endpoint                                    | Method         | Access        | Description                               |
| ------------------------------------------- | -------------- | ------------- | ----------------------------------------- |
| `/api/users/register/`                      | POST           | Admin         | Register a student or teacher             |
| `/api/users/login/`                         | POST           | Public        | Authenticate and get token                |
| `/api/users/teachers/`                      | GET            | Admin         | List all teachers                         |
| `/api/users/teachers/<id>/`                 | GET/PUT/DELETE | Admin         | Retrieve/Update/Delete a specific teacher |
| `/api/users/students/`                      | GET            | Admin/Teacher | List all students                         |
| `/api/users/students/<id>/`                 | PUT/DELETE     | Admin         | Update or delete a student                |
| `/api/users/subjects/create/`               | POST           | Admin         | Create new subject with teacher           |
| `/api/users/subjects/<id>/`                 | PUT/DELETE     | Admin         | Update/Delete subject                     |
| `/api/users/subjects/department/<dept_id>/` | GET            | Any           | List subjects in a department             |
| `/api/users/marks/`                         | POST           | Teacher       | Add marks for a student                   |
| `/api/users/marks/<id>/`                    | PUT/DELETE     | Teacher       | Update or delete a student's mark         |
| `/api/users/student/marks/`                 | GET            | Student       | View logged-in student's marks            |
| `/api/users/student/report/`                | GET            | Student       | Full report card with stats               |
| `/api/users/subjects/<id>/topper/`          | GET            | HOD/Admin     | Get topper of a subject                   |
| `/api/users/hod/department-marks/`          | GET            | HOD           | View all marks in department              |
| `/api/users/hod/stats/`                     | GET            | HOD           | Department performance summary            |

   
     
 
# school-management-system

A RESTful API-based School Management System built using Django and Django REST Framework.

Created school-management system new project
start new app as users inside the project
Started a CustomUser imported from abstractUser
created profiles for student and teacher

# Django School Management System API

This project is a School Management System built using **Django** and **Django REST Framework**. It provides functionality for managing departments, users (students and teachers), subjects, marks, and role-based access controls.

---

## 🔧 Features

- Custom user model with roles: `Student`, `Teacher`.
- Departments with one assigned Head of Department (HOD)
- Teachers assigned to specific subjects and departments
- Subject-teacher mapping
- Students assigned to departments
- Marks management:
  - Only subject teachers can add/update/delete marks for students
  - HODs can view all marks of students in their department
  - Students can view only their own marks
- Automatic department creation on registration (if not exists)
- Role-based permission system
- Token/Basic Authentication

## 📊 Advanced Features
- Report Card API: Shows total, average, pass/fail status, and subject-wise breakdown.

- Pass/Fail Logic: If student scores >= 40 in a subject, they pass; otherwise fail.

- Mark Percentage: Calculates percentage for each subject based on max marks.

- Subject-wise Topper API: Shows student with highest mark per subject.

- Department Stats (HOD only): Average marks, pass percentage for each subject.
---

## 🏗️ Project Structure

```bash
SCHOOL-MANAGEMENT-SYSTEM/
├── manage.py
├── config/          
│   ├── settings.py
│   └── urls.py
├── users/                 
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── urls.py
│   └── admin.py
└── README.md
```

## Roles & Access
| Role        | Permissions                                                           |
| ----------- | --------------------------------------------------------------------- |
| **Admin**   | Create users, assign departments, assign HODs                         |
| **Teacher** | View/update their own profile, add marks only for subjects they teach |
| **HOD**     | All teacher permissions + view all student marks in their department  |
| **Student** | View only their own marks                                             |

# 🧪 Sample Dataset (for Testing)

| Department | Teachers  | Subjects             | Students   |
| ---------- | --------- | -------------------- | ---------- |
| CSE        | 3 (1 HOD) | Python, Java, Data Science | 5 students |
| ECE        | 3 (1 HOD) | Digital Electronics, Signals and Systems,Control Systems  | 5 students |
| MECH       | 3 (1 HOD) | Thermodynamics, Machine Design, Fluid Mechanics  | 5 students |



## Tech Stack
Python 3.x

Django

Django REST Framework

SQLite (default, can switch to PostgreSQL/MySQL)

JWT/Basic Authentication

## Permissions & Security
Custom permission classes (e.g.,IsAdmin, IsHOD, IsTeacher, IsStudent,IsTeacherorAdmin)

Only authenticated users can access protected endpoints

Data isolation: Students can only access their data

### 👨‍💻 Contribution
Feel free to fork this project and create pull requests. For major changes, please open an issue first.

