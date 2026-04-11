# 📝 BlogBOOHub — Full Stack Blog Application

🌐 **Live Demo:** https://blog-application-xyz.vercel.app
🔧 **API Backend:** https://blog-application-g4io.onrender.com
📁 **GitHub:** https://github.com/Upadhyayme/blog-application

## 🚀 About The Project

BlogBOOHub is a full stack blog platform where users can register, log in, write blog posts with cover images, like posts, leave comments, and search for content. It is built with a Python Flask REST API backend and a clean Vanilla JavaScript frontend — no frameworks needed.

This project demonstrates full stack development skills including REST API design, JWT authentication, database management, image uploads, and cloud deployment.

---

## ✨ Features

- 🔐 **User Authentication** — Register and login with JWT tokens
- 🔒 **Secure Passwords** — bcrypt hashing, never stored in plain text
- 📝 **Full Blog CRUD** — Create, read, update, and delete posts
- 🖼️ **Image Uploads** — Upload a cover image for every post
- ❤️ **Likes System** — Like and unlike posts (one per user)
- 💬 **Comments** — Add and delete comments on posts
- 🔍 **Search** — Search posts by title, content, or tags
- 🏷️ **Tags** — Tag posts and filter by tag
- 📄 **Pagination** — 6 posts per page with navigation
- 📱 **Responsive Design** — Works on mobile and desktop

---

## 🧩 Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python 3.11 | Programming language |
| Flask | Web framework |
| SQLAlchemy | ORM and database management |
| SQLite | Database |
| JWT (PyJWT) | Authentication tokens |
| bcrypt | Password hashing |
| Flask-CORS | Cross-origin requests |
| Gunicorn | Production web server |

### Frontend
| Technology | Purpose |
|---|---|
| HTML5 | Page structure |
| CSS3 | Styling and responsive design |
| Vanilla JavaScript | Dynamic functionality |
| Fetch API | HTTP requests to backend |
| localStorage | Token and user storage |

### Deployment
| Service | Purpose |
|---|---|
| Render.com | Backend Flask API hosting |
| Vercel | Frontend static site hosting |
| GitHub | Version control |

---

## 🗂️ Project Structure

```
blog-application/
│
├── backend/
│   ├── app.py              ← Flask app factory and entry point
│   ├── config.py           ← All configuration settings
│   ├── models.py           ← Database models (User, Post, Comment, Like)
│   ├── requirements.txt    ← Python dependencies
│   ├── runtime.txt         ← Python version for Render
│   ├── static/
│   │   └── uploads/        ← Uploaded cover images stored here
│   └── routes/
│       ├── __init__.py
│       ├── auth.py         ← /register /login JWT middleware
│       └── posts.py        ← All blog post endpoints
│
└── frontend/
    ├── index.html          ← Home page with search and pagination
    ├── login.html          ← Login page
    ├── register.html       ← Registration page
    ├── create-post.html    ← Create and edit posts with image upload
    ├── post.html           ← Single post view with likes and comments
    ├── css/
    │   └── style.css       ← All styles with CSS variables
    └── js/
        └── api.js          ← Shared API client Auth toast and navbar
```

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | No | Create new account |
| POST | `/login` | No | Login and receive JWT |
| GET | `/me` | Yes | Get current user profile |

### Posts
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/posts` | No | Get all posts paginated |
| GET | `/posts?search=flask` | No | Search posts |
| GET | `/posts?tag=python` | No | Filter by tag |
| GET | `/posts/<id>` | No | Get single post with comments |
| POST | `/posts` | Yes | Create a new post |
| PUT | `/posts/<id>` | Yes | Update post — author only |
| DELETE | `/posts/<id>` | Yes | Delete post — author only |
| POST | `/posts/<id>/like` | Yes | Toggle like or unlike |
| POST | `/posts/<id>/comments` | Yes | Add a comment |
| DELETE | `/posts/<id>/comments/<cid>` | Yes | Delete a comment |
| POST | `/upload` | Yes | Upload a cover image |

---

## ⚙️ Local Setup Guide

### Prerequisites
- Python 3.11 or higher
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/Upadhyayme/blog-application.git
cd blog-application
```

### Step 2 — Set up the backend
```bash
cd backend
python -m venv venv

# Activate on Mac or Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 3 — Start the backend server
```bash
python app.py
```

You should see:
```
✅ Database tables created / verified.
✅ Upload folder ready.
🚀 Starting Flask Blog API on http://127.0.0.1:5000
```

### Step 4 — Start the frontend server
Open a second terminal window:
```bash
cd frontend
python -m http.server 8080
```

### Step 5 — Open in your browser
```
http://localhost:8080/index.html
```

---

## 🔐 Security Features

- Passwords hashed with **bcrypt** — never stored in plain text
- **JWT tokens** expire after 24 hours automatically
- **Authorization checks** — only the author can edit or delete their own content
- **Input validation** on all API endpoints with proper error messages
- **File type validation** on image uploads — PNG, JPG, GIF, WEBP only
- **File size limit** — images must be under 5 MB

---

## 🌐 Deployment Details

### Backend on Render.com
- Python 3.11 runtime
- Gunicorn WSGI production server
- SQLite database auto-created on first run
- Environment variables for all secret keys

### Frontend on Vercel
- Static site hosting
- Auto-deploys from GitHub main branch
- Global CDN for fast loading worldwide

---

## 📦 Python Dependencies

```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Cors==4.0.1
PyJWT==2.8.0
bcrypt==4.1.3
SQLAlchemy==2.0.30
werkzeug==3.0.3
gunicorn==21.2.0
```

---

## 👩‍💻 Developer

**Shreya Upadhyay**

- GitHub: [@Upadhyayme](https://github.com/Upadhyayme)
- Email: upadhyayshreya830@gmail.com

---

## 📄 License

This project is open source and available under the MIT License.

---

*Built with ❤️ by Shreya Upadhyay*
