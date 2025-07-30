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