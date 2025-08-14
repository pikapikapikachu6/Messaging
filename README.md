# Messaging Platform – Secure & User-Centred Web Application

## 📌 Overview
This project is a **secure, user-centred, full-stack messaging and forum application** designed to support communication and information sharing in an academic environment.  
It integrates **real-time messaging**, **role-based access control**, and **forum discussion features** with a strong focus on **security principles, usability, and maintainability**.

Developed as part of an academic project, it demonstrates practical skills in **Python web frameworks**, **front-end development**, **database design**, and **secure software engineering**, aligning with the requirements for advanced software development roles.

---

## 🚀 Key Features

### **Messaging Module**
- Add/remove friends with request validation.
- Private, secure, one-to-one messaging.
- Real-time update simulation.
- Admin capabilities for account moderation.

### **Forum Module**
- Create, view, and comment on posts.
- Upload and share documents.
- Role-specific interfaces: **Admin** and **Normal User**.
- Admin moderation tools (delete/edit any post).

### **Security**
- User authentication and role-based authorization.
- Secure password handling and session management.
- Input validation to prevent SQL injection/XSS.
- File upload validation to prevent malicious content.

### **Usability**
- Developed using a **User-Centred Design** process.
- Applied usability heuristics: visibility, feedback, constraints, consistency.
- Iterative testing: PACT analysis, card sorting, low-fi & hi-fi prototypes, guerrilla testing.
- Achieved **87.5%+ task success rate** in usability tests.

---

## 🛠 Technology Stack

**Frontend**
- Vue 3 + Vite + TailwindCSS
- HeroIcons + SweetAlert2
- Axios for API requests

**Backend**
- Python Flask (easily portable to Django)
- SQLite database

**Security**
- Role-Based Access Control (RBAC)
- Secure session management
- Input validation & sanitation

---

## 📐 Development Process

1. **Research & Requirements**
   - Collected user feedback through surveys.
   - Created personas to represent different user needs.

2. **Navigation Design**
   - Open and closed card sorting to define sitemap.
   - Wireframes for role-based UI flow.

3. **Prototype & Iteration**
   - Low-fidelity and high-fidelity designs.
   - Guerrilla usability testing and improvements.

4. **Implementation**
   - Modular front-end and back-end structure.
   - RESTful API between Vue frontend and Flask backend.

5. **Security Enhancements**
   - Applied OWASP recommendations for authentication & data handling.
   - Enforced file type & size checks for uploads.

---

## 📊 Skills Demonstrated
- **Python Web Development** (Flask, transferable to Django)
- **Frontend Development** (Vue 3, TailwindCSS)
- **Secure Software Design** (RBAC, input validation, secure file handling)
- **Database Management** (Schema design, SQL queries, normalization)
- **User Interface Design** (Heuristics, iterative testing)
- **Cross-role System Architecture** (Admin vs User workflows)

---

## 📂 Run Instruction
### Front end Get Started

1. **Install dependency**

```
npm i
```

2. **Run dev server**

```
npm run dev
```

### Back end Get Started
1. **Run back end:**

```
python3 run.py
```

2. **If permissions problem, run back end:**

```
sudo python3 run.py
```

3. **Other lack of python package**
```
pip3 install {package name}
```
