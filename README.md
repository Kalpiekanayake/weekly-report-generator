# 📊 Weekly Report Generator

A full-stack web application developed to streamline weekly reporting, project tracking, and team management within software development teams.

The system enables managers to monitor project progress, review weekly reports, and gain insights through an interactive dashboard, while team members can easily submit and manage their weekly reports.

---

## ✨ Features

### 🔐 Authentication
- User Registration
- Secure Login (JWT Authentication)
- Role-Based Access Control (Manager & Team Member)

### 📋 Weekly Reports
- Create Weekly Reports
- Edit Draft Reports
- Submit Reports
- View Report History
- Track Submission Status

### 📁 Project Management
- Create Projects
- Edit Projects
- Delete Projects
- Assign Members to Projects

### 📈 Dashboard
#### Manager Dashboard
- Total Users
- Total Projects
- Total Reports
- Draft Reports
- Submitted Reports
- Pending Reports
- Late Reports
- Recent Activity
- Project Summary
- Team Reports
- Analytics Charts

#### Team Member Dashboard
- Personal Weekly Reports
- Assigned Projects
- Report Status

### 🤖 AI Assistant
- Weekly Progress Summary
- Pending Report Detection
- Blocker Identification
- Project Insights
- Report Analysis

> **Note:** The current AI Assistant uses rule-based backend logic to analyze project data. The architecture can be extended to integrate Gemini or other LLMs in the future.

---

# 🛠️ Tech Stack

## Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router

## Backend
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Uvicorn

## Database
- PostgreSQL (Supabase)

---

# 📂 Project Structure

```
weekly-report-generator/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── seed.py
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── ...
│
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Kalpiekanayake/weekly-report-generator.git
```

---

## Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# ⚙️ Environment Variables

Create a `.env` file inside the **backend** directory.

```env
DATABASE_URL=your_database_url

JWT_SECRET_KEY=your_secret_key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=1440
```


# 🌱 Seed Sample Data

Populate the database with sample users, projects, and reports.

```bash
python -m app.seed
```

---

# 👤 Demo Login Credentials

### Manager

```
Email:
manager@example.com

Password:
password123
```

### Team Member

```
Email:
member1@example.com

Password:
password123
```

---

# 📸 Screenshots

Add screenshots here.

- Login Page
  <img width="1352" height="584" alt="image" src="https://github.com/user-attachments/assets/35ab001c-4457-4d96-84b9-d9b6a59e3f0e" />

- Registration Page
  <img width="1351" height="586" alt="image" src="https://github.com/user-attachments/assets/09070fbe-ecb3-4e24-8c9d-28ac437fce61" />

- Manager Dashboard
  <img width="1333" height="634" alt="image" src="https://github.com/user-attachments/assets/41e782f6-ee62-47ea-bc76-1d798d3f5fdd" />
  <img width="1335" height="632" alt="image" src="https://github.com/user-attachments/assets/b3b8d46d-006f-456d-87b6-0c22bf1983e0" />
  <img width="1328" height="634" alt="image" src="https://github.com/user-attachments/assets/cfb85523-93b2-4e54-b404-4ce7b9aabd8b" />
  <img width="1329" height="634" alt="image" src="https://github.com/user-attachments/assets/58f2f2e9-f402-40cc-be4b-6d2f9d20d484" />

- Weekly Reports
  <img width="1346" height="632" alt="image" src="https://github.com/user-attachments/assets/4a11e392-07b1-4c08-888f-39e229ed13c1" />

- Projects
  <img width="1341" height="632" alt="image" src="https://github.com/user-attachments/assets/4ce93608-bde2-443c-859e-d080099b4128" />

- AI Assistant
<img width="1341" height="634" alt="image" src="https://github.com/user-attachments/assets/f594d051-b2c8-4c60-9820-cba985f3c2d5" />

---
#  ER-Diagram
![Uploading Weekly Report Generator.drawio.png…]()


# 🔮 Future Improvements

- Gemini AI Integration
- Email Notifications
- PDF Export
- File Attachments
- Calendar Integration
- Email Reminders
- Advanced Analytics
- Mobile Application

---

# 👩‍💻 Author

**Kalpani Ekanayake**

GitHub:
https://github.com/Kalpiekanayake

LinkedIn:
https://www.linkedin.com/in/kalpaniekanayake/


