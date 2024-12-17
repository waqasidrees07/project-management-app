
## **Project Management System**

A Django-based project management system that allows users to create projects, manage tasks, assign team members, and track task dependencies. This system includes core functionalities like task prioritization, status management, and email notifications.

---

### **Table of Contents**
1. [Project Setup](#project-setup)
2. [Features](#features)
3. [Models](#models)
4. [Testing](#testing)
5. [Usage](#usage)

---

### **Project Setup**

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**  
   Clone the project from the repository using the following command:
   ```bash
   cd project-management-app
   ```

2. **Create a Virtual Environment**  
   Use `venv` or any virtual environment tool to isolate dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**  
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**  
   Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser**  
   Create an admin user to access the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**  
   Start the local server:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**  
   Open your browser and visit:
   ```
   http://127.0.0.1:8000/
   ```

---

### **Features**

- **User Authentication:** Secure login/logout functionality.
- **Project Management:** Create, update, and delete projects.
- **Task Management:** Add tasks, set priorities, statuses, and dependencies.
- **Team Management:** Assign team members to projects and tasks.
- **Email Notifications:** Send email notifications when tasks are created or updated.
- **Dependencies Tracking:** Manage task dependencies.

---

### **Models**

1. **Project Model**  
   - Fields: `title`, `description`, `start_date`, `end_date`, `team_members`  
   - Relationships: Many-to-Many with `User`.

2. **Task Model**  
   - Fields: `title`, `description`, `priority`, `due_date`, `status`  
   - Relationships: ForeignKey to `Project` and `User`, Many-to-Many for dependencies.

3. **User Model**  
   - Extended user model with `email` for email notifications.

---

### **Testing**

Run the unit tests using the following command:
```bash
python manage.py test
```

Tests include:
- Creating projects and tasks.
- Validating task dependencies.
- Ensuring email notifications are sent correctly.

---

### **Usage**

1. **Create a Project**  
   Go to the "Projects" page and click "Create Project". Fill in the details and save.

2. **Add a Task**  
   Navigate to the desired project and click "Add Task". Assign a user, set dependencies, and save.

3. **Track Dependencies**  
   View task details to see dependent tasks.

4. **Email Notifications**  
   Assigned users will receive an email whenever tasks are created or updated.

---

### **Contact**
For support, please contact: `waqasidrees15@gmail.com`
