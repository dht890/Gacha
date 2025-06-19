# Full-Stack Desktop App: React + Flask + MongoDB + Electron + Tailwind

This is a full-stack desktop application built with:

- ⚛️ React (frontend)
- 🐍 Flask (backend API)
- 🍃 MongoDB (database)
- 🖥️ Electron (desktop wrapper)
- 🎨 Tailwind CSS (styling)

---

## 📁 Project Structure

```
my-app/
├── frontend/        # React + Tailwind frontend
├── backend/         # Flask + MongoDB backend
├── main.js          # Electron entry point
├── package.json     # Electron config and shared deps
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fullstack-desktop-app.git
cd fullstack-desktop-app
```

---

### 2. Set Up the Frontend (React + Tailwind)

```bash
cd frontend
npm install
npm run dev   # Use `npm run build` for production
```

---

### 3. Set Up the Backend (Flask + MongoDB)

```bash
cd ../backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

> Make sure MongoDB is running (default: `mongodb://localhost:27017`)

---

### 4. Launch Electron App

```bash
cd ..
npm install        # installs Electron if not already
npx electron .
```

---

## 🔁 Git Workflow

### Daily development

```bash
git status                  # See what changed
git add .                   # Stage all changes
git commit -m "message"     # Commit changes
git pull origin main        # Get latest version
git push origin main        # Upload your changes
```

---

## 🌿 Branching Workflow

```bash
git checkout -b feature/your-feature-name    # Create new feature branch
# Make changes
git add .
git commit -m "Add feature"
git push origin feature/your-feature-name

git checkout main
git pull origin main
git merge feature/your-feature-name
git push origin main
```

---

## 🧼 .gitignore Suggestions

```
# Node
node_modules/
build/
dist/

# Python
__pycache__/
venv/

# Environment
.env

# OS
.DS_Store
Thumbs.db
```

---

## 📦 Production Build

### React

```bash
cd frontend
npm run build
```

### Electron

In `main.js`, load the React build:

```js
win.loadFile(path.join(__dirname, 'frontend', 'build', 'index.html'));
```

Then package using:

```bash
npm install --save-dev electron-builder
npx electron-builder
```

---

## 🛠 Tech Stack Summary

| Layer       | Tool/Tech              |
|-------------|------------------------|
| Frontend    | React, Tailwind CSS    |
| Backend     | Flask (Python)         |
| Database    | MongoDB                |
| Desktop     | Electron               |
| Styling     | Tailwind CSS           |
| Versioning  | Git + GitHub           |

---

## 📄 License

MIT License © David Tran
