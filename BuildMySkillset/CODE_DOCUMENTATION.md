# Build My Skillset - Code Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Database Models](#database-models)
5. [Forms and Validation](#forms-and-validation)
6. [Routes and Views](#routes-and-views)
7. [Frontend Components](#frontend-components)
8. [Utilities](#utilities)
9. [Configuration](#configuration)
10. [Security Features](#security-features)
11. [Deployment](#deployment)

## Project Overview

**Build My Skillset** is a comprehensive e-learning platform built with Flask that provides:
- Course management and enrollment system
- Internship listings and application system
- Project showcase and request functionality
- Certificate verification system
- User authentication and role-based access
- Admin dashboard for content management
- Feedback and contact systems

**Key Features:**
- Modern ice blue and white responsive design
- User authentication with role-based access (user/admin)
- Course catalog with enrollment tracking
- Internship application system with file uploads
- Certificate generation and verification
- Admin dashboard with statistics and management tools
- Feedback system with approval workflow

## Architecture

### Technology Stack
- **Backend:** Flask (Python web framework)
- **Database:** PostgreSQL (production) / SQLite (development)
- **ORM:** SQLAlchemy with Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF with WTForms validation
- **Frontend:** Bootstrap 5.3.0, Font Awesome 6.0.0, Vanilla JavaScript
- **File Handling:** Werkzeug secure filename, Pillow for image processing

### Design Pattern
The application follows the **Model-View-Controller (MVC)** pattern:
- **Models:** Database models defined in `models.py`
- **Views:** Route handlers in `routes.py`
- **Templates:** Jinja2 templates in `templates/` directory
- **Controllers:** Form handling and business logic integrated in routes

## File Structure

```
build-my-skillset/
├── app.py                  # Flask app initialization and configuration
├── main.py                 # Entry point for the application
├── models.py               # Database models and relationships
├── routes.py               # URL routes and view functions
├── forms.py                # WTForms form definitions and validation
├── utils.py                # Utility functions for file handling and formatting
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── uploads/           # File upload directory
├── templates/             # Jinja2 templates
│   ├── base.html          # Base template with common structure
│   ├── index.html         # Homepage template
│   ├── auth/              # Authentication templates
│   ├── courses/           # Course-related templates
│   ├── internships/       # Internship templates
│   ├── admin/             # Admin dashboard templates
│   └── errors/            # Error page templates
└── replit.md              # Project documentation and preferences
```

## Database Models

### Core Models

#### User Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```
**Purpose:** Stores user account information with role-based access control
**Relationships:** One-to-many with Enrollment, Application, Certificate, Feedback

#### Course Model
```python
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(20), nullable=False)  # 'beginner', 'intermediate', 'advanced'
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```
**Purpose:** Represents courses available on the platform
**Relationships:** One-to-many with Enrollment

#### Enrollment Model
```python
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'cancelled'
```
**Purpose:** Many-to-many relationship between users and courses
**Status Values:** active, completed, cancelled

#### Internship Model
```python
class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    stipend = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```
**Purpose:** Stores internship opportunities
**Relationships:** One-to-many with Application

#### Application Model
```python
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    resume_path = db.Column(db.String(200), nullable=True)
    cover_letter = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
```
**Purpose:** Tracks internship applications with file upload support
**Status Values:** pending, accepted, rejected

#### Certificate Model
```python
class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    certificate_code = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='valid')  # 'valid', 'revoked'
```
**Purpose:** Digital certificates with unique verification codes
**Certificate Code Format:** BMS-XXXXXXXX (8-character hex)

#### Additional Models
- **Project:** Showcases project opportunities
- **Feedback:** User reviews with approval system
- **Contact:** Contact form submissions

## Forms and Validation

### Authentication Forms

#### LoginForm
```python
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
```

#### RegisterForm
```python
class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
```
**Custom Validation:**
- Email uniqueness check
- Password confirmation matching

### Content Management Forms

#### CourseForm
```python
class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired(), Length(max=50)])
    level = SelectField('Level', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    price = FloatField('Price', validators=[NumberRange(min=0)])
```

#### ApplicationForm
```python
class ApplicationForm(FlaskForm):
    resume = FileField('Resume', validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and DOC files allowed!')])
    cover_letter = TextAreaField('Cover Letter', validators=[Length(max=1000)])
```
**File Upload Security:**
- File type validation (PDF, DOC, DOCX only)
- Secure filename handling
- Size limitations (16MB max)

## Routes and Views

### Core Route Categories

#### Authentication Routes (`/auth`)
- **GET/POST** `/login` - User login with session management
- **GET/POST** `/register` - User registration with validation
- **GET** `/logout` - Session termination

#### Course Management (`/courses`)
- **GET** `/courses` - Course catalog with filtering
- **GET** `/courses/<id>` - Course details page
- **POST** `/courses/<id>/enroll` - Course enrollment (authenticated)
- **GET/POST** `/admin/courses` - Admin course management
- **GET/POST** `/admin/courses/add` - Add new course (admin only)

#### Internship System (`/internships`)
- **GET** `/internships` - Internship listings
- **GET** `/internships/<id>` - Internship details
- **GET/POST** `/internships/<id>/apply` - Application submission
- **GET** `/admin/applications` - Admin application management

#### Certificate System
- **GET/POST** `/verify-certificate` - Public certificate verification
- **GET/POST** `/admin/certificates` - Certificate issuance (admin)

#### Dashboard Routes
- **GET** `/dashboard` - User dashboard (role-based routing)
- **GET** `/admin/dashboard` - Admin statistics and management

### Route Protection
```python
@login_required  # Requires authentication
def protected_route():
    if current_user.role != 'admin':  # Role-based access
        abort(403)
```

### Key Route Implementations

#### User Registration
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)
```

#### Course Enrollment
```python
@app.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    course = Course.query.get_or_404(course_id)
    existing = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    
    if existing:
        flash('You are already enrolled in this course.', 'warning')
    else:
        enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash('Successfully enrolled!', 'success')
    
    return redirect(url_for('course_detail', course_id=course_id))
```

## Frontend Components

### Template Hierarchy
```
base.html (Base template with navigation, footer, flash messages)
├── index.html (Homepage with featured content)
├── auth/
│   ├── login.html
│   └── register.html
├── courses/
│   ├── courses.html (Course catalog)
│   └── course_detail.html
├── dashboard/
│   ├── user_dashboard.html
│   └── admin_dashboard.html
└── admin/ (Admin-only templates)
```

### CSS Framework
- **Bootstrap 5.3.0:** Responsive grid system and components
- **Font Awesome 6.0.0:** Icon library
- **Custom CSS:** Ice blue and white theme
  - Primary color: `#87CEEB` (Sky Blue)
  - Secondary colors: Various blue shades
  - Typography: Clean, modern fonts

### JavaScript Features
```javascript
// Form validation
function initializeFormValidation() {
    // Real-time form validation
}

// Search and filtering
function initializeSearchFilters() {
    // Course and internship filtering
}

// Interactive components
function initializeRatingSystem() {
    // Star rating system for feedback
}
```

### Key UI Components
- **Navigation Bar:** Responsive with user authentication status
- **Flash Messages:** Bootstrap alerts for user feedback
- **Form Validation:** Real-time client-side validation
- **Modal Dialogs:** Bootstrap modals for confirmations
- **Responsive Design:** Mobile-first approach

## Utilities

### File Handling (`utils.py`)

#### Image Processing
```python
def save_picture(form_picture, folder):
    """Save uploaded picture with random filename and resize"""
    random_hex = secrets.token_hex(8)
    picture_path = os.path.join(current_app.root_path, 'static', folder, random_hex + ext)
    
    output_size = (800, 600)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return random_hex + ext
```

#### File Validation
```python
def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
```

#### Date Formatting
```python
def format_date(date):
    """Format date for display"""
    return date.strftime('%B %d, %Y')

def format_datetime(datetime):
    """Format datetime for display"""
    return datetime.strftime('%B %d, %Y at %I:%M %p')
```

## Configuration

### App Configuration (`app.py`)
```python
# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///buildmyskillset.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Security configuration
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
```

### Environment Variables
- **DATABASE_URL:** PostgreSQL connection string
- **SESSION_SECRET:** Flask session secret key
- **PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE:** PostgreSQL credentials

### Login Manager Setup
```python
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

## Security Features

### Authentication Security
- **Password Hashing:** Werkzeug's `generate_password_hash()` with default settings
- **Session Management:** Flask-Login for secure session handling
- **CSRF Protection:** Flask-WTF automatic CSRF token generation

### File Upload Security
```python
# File type validation
FileField('Resume', validators=[FileAllowed(['pdf', 'doc', 'docx'])])

# Secure filename handling
from werkzeug.utils import secure_filename
filename = secure_filename(file.filename)

# File size limits
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
```

### Access Control
```python
# Role-based access control
@login_required
def admin_only_route():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
```

### Certificate Security
```python
def generate_certificate_code():
    """Generate unique certificate verification code"""
    return f"BMS-{uuid.uuid4().hex[:8].upper()}"
```

## Deployment

### Development Setup
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup:**
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/buildmyskillset"
   export SESSION_SECRET="your-secret-key"
   ```

3. **Run Application:**
   ```bash
   python main.py
   # or
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

### Production Configuration
- **Database:** PostgreSQL with connection pooling
- **Web Server:** Gunicorn with proxy fix for reverse proxies
- **File Storage:** Static file serving with secure upload handling
- **Environment Variables:** All sensitive data in environment variables

### Database Migration
```python
# Automatic table creation on startup
with app.app_context():
    import models
    db.create_all()
    
    # Create default admin user
    if not User.query.filter_by(email='admin@buildmyskillset.com').first():
        admin_user = User(...)
        db.session.add(admin_user)
        db.session.commit()
```

### Key Deployment Features
- **Proxy Fix:** Handles X-Forwarded headers for HTTPS
- **Connection Pooling:** Database connection management
- **Error Handling:** Custom 404 and 500 error pages
- **Logging:** Debug mode with comprehensive logging
- **Auto-initialization:** Database and admin user creation

## Default Admin Credentials
- **Email:** admin@buildmyskillset.com
- **Password:** admin123
- **Role:** admin

## API Endpoints Summary

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/` | GET | Homepage | No |
| `/login` | GET/POST | User login | No |
| `/register` | GET/POST | User registration | No |
| `/logout` | GET | User logout | Yes |
| `/dashboard` | GET | User/Admin dashboard | Yes |
| `/courses` | GET | Course catalog | No |
| `/courses/<id>` | GET | Course details | No |
| `/courses/<id>/enroll` | POST | Enroll in course | Yes |
| `/internships` | GET | Internship listings | No |
| `/internships/<id>` | GET | Internship details | No |
| `/internships/<id>/apply` | GET/POST | Apply for internship | Yes |
| `/projects` | GET | Project showcase | No |
| `/verify-certificate` | GET/POST | Certificate verification | No |
| `/feedback` | GET/POST | Submit feedback | Yes |
| `/contact` | GET/POST | Contact form | No |
| `/admin/*` | Various | Admin management | Yes (Admin) |

This documentation provides a comprehensive overview of the Build My Skillset platform's codebase, architecture, and implementation details.