# POD OCR Backend

A backend system built using **FastAPI** to manage Proof of Delivery (POD) documents. This backend offers user authentication, job scheduling, file management, and notifications.

---

## Project Overview

The **POD OCR Backend** automates the management of Proof of Delivery documents by providing APIs for:

* User authentication
* Job management
* File management (update, delete, search)
* Notifications and history tracking

## Features

* **User Authentication** : Signup, login, and password reset.
* **Job Management** : Create, retrieve, delete, and schedule jobs.
* **File Management** : search, delete files, and manage auto-confirmation for specific files.
* **Notifications** : Retrieve notifications related to files and jobs.
* **History Tracking** : Track changes and events for each file.

## Setup and Installation

1. **Clone the repository** :

```
git clone https://github.com/SAIN-CUBE/POD-OCR-Project.git
cd POD-OCR-Project
```

2. **Create a virtual environment** :

```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3. **Install dependencies** :

```
pip install -r requirements.txt

```

## Environment Variables

Create a `.env` file in the project root and add the following variables:


## Running the Server

Before runing the server, go to out of the app directory by using following code:

```
cd ..
```

To run the server locally, use:

```
uvicorn app.main:app --reload

```

The API will be accessible at `http://127.0.0.1:8000`. You need to open the swagger UI by using /docs at the end of url!
