# Smart Cooking Chatbot

A **Smart Cooking Customer Support Chatbot** built with **React, TypeScript, TailwindCSS, and FastAPI**, featuring PWA support, chat history, and AI-powered responses. Designed to provide instant cooking assistance and tips to users in a modern, responsive interface.

---

## Features

- **Real-time Chat** with AI-powered responses.
- **User Login** via mobile number.
- **Chat History** saved per user.
- **Progressive Web App (PWA)** support with install button.
- **Dark/Light Theme** support.
- **Offline Support** using Service Workers.
- **Responsive Design** for mobile and desktop.

---

## Tech Stack

- **Frontend:** React, TypeScript, TailwindCSS, ShadCN UI, Framer Motion
- **Backend:** FastAPI, Uvicorn
- **PWA:** Manifest + Service Worker
- **State Management:** Cookies for session storage
- **Deployment:** Localhost / HTTPS for PWA

---

## Project Structure
appname/
├─ public/
│ ├─ favicon-192.png
│ ├─ favicon-512.png
│ ├─ index.html
│ ├─ manifest.json
│ └─ service-worker.js
├─ App.tsx
├─ index.tsx
├─ PWAInstaller.tsx
├─ serviceWorkerRegistration.ts
├─ components/
│ ├─ ChatWindow.tsx
│ ├─ MessageInput.tsx
│ ├─ Header.tsx
│ └─ LoginModal.tsx
├─ utils/
│ ├─ api.ts
│ └─ cookies.ts
└─ types.ts

---

## Installation & Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd appname
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
http://127.0.0.1:8000
