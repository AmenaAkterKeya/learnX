# LearnX Backend

**LearnX** is a web platform designed for online learning. The backend API for LearnX provides endpoints for managing courses, instructors, and student interactions. It enables data retrieval and CRUD operations for user registration, course, enrollment, comments

---

## Main Features

- **User Authentication**: Secure user registration and login.
- **Course Catalog**: Browse various courses across various subjects.
- **Course Enrollment**: Easily enroll in courses of your choice.
- **Roles**: 
   - **Student**: View and manage enrolled courses, and deposit funds.
   - **Instructor**: Upload, edit, and delete courses and see students who enroll.

---
## Features Details

### User Management
- **User Registration**: New users can register an account via a registration link.
- **User Login**: Existing users can log in using their credentials.

### Role-Based Access
- **Student Role**:
  - **Course Enrollment**: Easily enroll in courses of your choice.
  - **View Enrolled Courses**: Students can see a list of their enrolled courses.
  - **Deposit Money**: Students can deposit money to their accounts for course payments.

- **Instructor Role**:
  - **Course Management**: Instructors can upload their courses, edit courses, and delete courses.

### Enrollment Features
- **Easy Enrollment**: Students can easily enroll in courses of their choice.
- **Single Enrollment Per Course**: Each student can enroll in a course only once.
- **View Enrolled Courses**: Students can see a list of their enrolled courses.
- 
### Course Management
- **Category Search**: Users can filter courses based on categories for easier navigation.
- 
### Financial Management
- **Deposit Money**: Students can deposit money to their accounts for course payments.

## Technologies Used

### Backend
- **Python 3.x**: Programming language.
- **Django**: Web framework for backend development.
- **Django REST Framework**: API development for seamless frontend-backend communication.

---

## Live Demo

- **LearnX Frontend**: [LearnX Frontend](https://amenaakterkeya.github.io/learnX_frontend/)
- **LearnX Backend**: [LearnX Backend](https://learn-x-seven.vercel.app/)

---

# LearnX API Endpoints

## User Management

- **POST** `/register/` - Register a new user.
- **POST** `/login/` - User login.
- **POST** `/logout/` - User logout.

## Department Management

- **GET** `/department/` - List all departments.
- **POST** `/department/` - Create a new department.

## Course Management

- **GET** `/courses/` - List all courses.
- **GET** `/courses/<int:pk>/` - Retrieve details of a specific course.
- **POST** `/courses/` - Create a new course (Admin/Instructor only).
- **PUT** `/courses/<int: pk>/` - Update a specific course (Admin/Instructor only).
- **DELETE** `/courses/<int: pk>/` - Delete a specific course (Admin/Instructor only).

## Comment Management

- **GET** `/comment/` - List all comments.
- **POST** `/comment/` - Add a new comment to a course.

## Enrollment Management

- **GET** `/enrollments/<int:student_id>/` - Retrieve all enrollments for a specific student.
- **POST** `/enrolls/<int:course_pk>/` - Enroll a user in a specific course.
- **GET** `/enrolls/<int:course_pk>/status/` - Get the enrollment status for a specific course.
- **GET** `/enrollview/<int:pk>/` - View enrollment details for a specific user.

## Balance Management

- **GET** `/balanceview/` - Retrieve the balance for the user.
- **POST** `/balance/` - Deposit money to the user's balance.
  
---

## Installation & Running the App

### Prerequisites
- **Python 3.x**
- **Django** and **Django REST Framework**

### Setup

1. **Clone the Repository**:
   ```bash
   
   git clone https://github.com/username/learnX.git
   cd workio
2. **Install Dependencies:**:
   ```bash
   
   pip install -r requirements.txt
3. **Run Database Migrations**:
   ```bash
   
   python manage.py migrate
4. **Start the Development Server**:
   ```bash
   
   python manage.py runserver
5. **Run Tests**:
   ```bash
   
   http://localhost:8000/
The backend server will be accessible at http://localhost:8000/api/.

## License

This project is licensed under the MIT License.
This version includes all information within a single structured flow in `README.md`. It’s designed for easy access and readability for anyone interacting with the repository.
