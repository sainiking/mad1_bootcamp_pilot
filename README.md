# Admate - Influencer and Sponsor Management System

Admate is a web application that connects influencers with sponsors. It allows sponsors to create campaigns and influencers to participate in those campaigns. The application provides a comprehensive dashboard for managing and tracking campaign performance.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [License](#license)
- [Contact](#contact)

## Features

- User authentication and role-based access control
- Influencer and sponsor profiles
- Campaign creation and management
- Search functionality for influencers and campaigns
- Performance metrics for influencers
- Flagging and unflagging of inappropriate profiles and campaigns

**Installation**

**Prerequisites**

- Python 3.7+
- Flask
- SQLAlchemy
- Other dependencies listed in `requirements.txt`

**Steps**

1. Clone the repository:

   ```sh
   git clone (https://github.com/sainiking/mad1_bootcamp_pilot)
   cd admate

2. Create and activate a virtual environment:
   # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    
   # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

3. Install the dependencies:
   pip install -r requirements.txt

4. Set up the database:
   python -c "from application import create_app; app = create_app(); with app.app_context(): from application.models import db; db.create_all()"

5. Run the application:
   main.py

**Usage:**
1. Register as a sponsor or influencer:
    Go to the registration page and choose your role (Sponsor or Influencer).

2. Create and manage campaigns:
    Sponsors can create new campaigns, assign influencers, and track campaign performance.

3. Participate in campaigns:
   Influencers can view available campaigns and apply to participate.

4. Admin dashboard:
   Admin users can manage users, campaigns, and view performance statistics.

**Technologies**
Backend:
  *Flask
  *SQLAlchemy
  *Flask-Migrate
Frontend:
  *HTML5
  *CSS3
  *Bootstrap
Database:
  *SQLite (for development)
  *PostgreSQL (for production)
