# Build My Skillset - E-Learning Platform

A comprehensive e-learning platform built with Flask featuring course management, internships, certificate verification, and admin functionality.

## Features

- **User Authentication**: Secure login/register with role-based access
- **Course Management**: Browse courses, enroll, and track progress
- **Internship System**: Apply for internships with resume upload
- **Certificate Verification**: Digital certificates with unique codes
- **Admin Dashboard**: Complete management interface
- **Modern Design**: Professional navy blue and white theme

## Quick Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export DATABASE_URL="your-database-url"
   export SESSION_SECRET="your-secret-key"
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```
   
   The application will be available at: http://localhost:5000

## Default Admin Login
- **Email**: admin@buildmyskillset.com
- **Password**: admin123

## Project Structure

```
buildmyskillset/
├── app.py              # Flask app configuration
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routes and views
├── forms.py            # WTForms definitions
├── utils.py            # Utility functions
├── static/             # CSS, JS, and uploads
├── templates/          # Jinja2 templates
└── CODE_DOCUMENTATION.md  # Complete code documentation
```

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: Bootstrap 5, Font Awesome, Vanilla JS
- **Security**: Password hashing, CSRF protection, file validation

## Color Scheme

The platform uses a professional navy blue theme:
- Primary Navy: #2C3E50
- Light Navy: #34495E
- Accent Blue: #3498DB
- Light Background: #ECF0F1

## Documentation

Complete technical documentation is available in `CODE_DOCUMENTATION.md` which includes:
- Database models and relationships
- API endpoints
- Security features
- Deployment instructions

## Support

For technical questions or issues, refer to the comprehensive documentation included in this package.