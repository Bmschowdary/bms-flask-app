# Build My Skillset - E-Learning Platform

## Overview

Build My Skillset is a comprehensive e-learning and project development platform built with Flask. The platform offers courses, internships, and real-world projects to students, featuring user authentication, content management, certificate verification, and administrative tools.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### July 16, 2025 - Code Documentation Complete
- Created comprehensive CODE_DOCUMENTATION.md covering entire codebase
- Documented all models, routes, forms, and security features
- Added deployment instructions and API reference
- Application running successfully on port 5000

## System Architecture

The application follows a traditional Flask MVC architecture with the following key components:

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login for session management
- **Forms**: Flask-WTF for form handling and validation
- **Template Engine**: Jinja2 (Flask's default)

### Frontend Architecture
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.0.0
- **JavaScript**: Vanilla JavaScript with custom functionality
- **Styling**: Custom CSS with ice blue and white theme

### Database Design
The application uses SQLAlchemy models with the following main entities:
- **User**: Stores user accounts with role-based access
- **Course**: Course catalog with pricing and difficulty levels
- **Internship**: Internship opportunities with requirements
- **Enrollment**: Many-to-many relationship between users and courses
- **Application**: Internship applications with file uploads
- **Certificate**: Digital certificates with verification codes
- **Feedback**: User feedback system with approval workflow

## Key Components

### Authentication System
- User registration and login with password hashing
- Role-based access control (user/admin)
- Session management with Flask-Login
- Protected routes requiring authentication

### Course Management
- Course catalog with filtering by difficulty level
- Enrollment system tracking user progress
- Admin interface for course creation and management
- Pricing support for paid courses

### Internship System
- Internship listings with detailed requirements
- Application system with resume upload capability
- Admin review and management of applications

### Certificate Verification
- Unique certificate code generation
- Public verification system for certificate authenticity
- Certificate issuance tracking

### File Upload System
- Resume upload for internship applications
- File validation and security measures
- Configurable upload directory and size limits

### Admin Dashboard
- Comprehensive statistics and metrics
- Content management for courses and internships
- User management and feedback moderation
- Certificate issuance system

## Data Flow

1. **User Registration/Login**: Users create accounts or authenticate through the login system
2. **Course Enrollment**: Authenticated users can browse and enroll in courses
3. **Internship Applications**: Users can apply for internships with resume uploads
4. **Certificate Generation**: Admin issues certificates for course completion
5. **Feedback Collection**: Users provide feedback on courses for platform improvement

## External Dependencies

### Python Packages
- Flask: Core web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: Authentication management
- Flask-WTF: Form handling and CSRF protection
- WTForms: Form validation
- Werkzeug: Password hashing and file utilities
- Pillow: Image processing for uploads

### Frontend Libraries
- Bootstrap 5.3.0: Responsive CSS framework
- Font Awesome 6.0.0: Icon library
- Custom JavaScript: Interactive functionality

### Database
- SQLite: Default development database
- PostgreSQL: Production database support via DATABASE_URL environment variable

## Deployment Strategy

### Configuration
- Environment-based configuration using os.environ
- Separate settings for development and production
- Session secret key configuration
- Database URL configuration with fallback to SQLite

### File Handling
- Static file serving for uploads
- Configurable upload directory
- File size limits and validation
- Secure filename handling

### Security Features
- CSRF protection via Flask-WTF
- Password hashing with Werkzeug
- File upload validation
- Proxy fix for deployment behind reverse proxies

### Database Management
- Automatic table creation on startup
- Connection pooling configuration
- Database URL environment variable support

The application is designed to be easily deployable on platforms like Replit, with automatic database initialization and environment-based configuration. The architecture supports both development and production environments with minimal configuration changes.