# Real-Time Individual Chat Application

A real-time one-to-one chat application built using **Django**, **Django Channels**, and **WebSockets**.

This project allows users to chat in real time with message delivery and read status indicators.

---

## Features

- User registration and login
- Custom user model
- Real-time chat using WebSockets
- Online / offline status
- Message delivery status (✓)
- Message read status (✓✓)
- Message history
- One-to-one private chat
- Django MVT architecture

---

## Tech Stack

- Python
- Django
- Django Channels
- WebSocket
- SQLite
- HTML, CSS, JavaScript

---

## Project Structure

```
chat_project/
│
├── chat_project/
│   ├── settings.py
│   ├── asgi.py
│   ├── urls.py
│
├── apps/
│   ├── accounts/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │
│   ├── chat_app/
│       ├── consumers.py
│       ├── routing.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│
├── templates/
│
├── manage.py
```

---

# Setup Steps

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/chat_project.git
cd chat_project
```

---

## 2. Create Virtual Environment

```bash
python -m venv virtual_env
```

Activate it:

### Windows
```bash
virtual_env\Scripts\activate
```

### Mac/Linux
```bash
source virtual_env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install django channels daphne
```

or

```bash
pip install -r requirements.txt
```

---

# Installation Instructions

## Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

# How to Run the Project

Start the development server:

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000
```

---

# Testing Real-Time Chat

1. Register two users
2. Open two browsers (or incognito mode)
3. Login with different users
4. Start chatting

You will see:

- Real-time messaging
- Delivered ticks
- Read receipts
- Online status

---

# WebSocket URL

```
ws://127.0.0.1:8000/ws/chat/<user_id>/
```

---

# Author

Akhil S

---


