import os
import uuid
from urllib.parse import urlparse
from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Course, Internship, Application, Project, Certificate, Feedback, Contact, Enrollment
from forms import *
import logging

# Helper function to generate certificate code
def generate_certificate_code():
    return f"BMS-{uuid.uuid4().hex[:8].upper()}"

# Helper function to validate safe redirects
def is_safe_url(target):
    """Check if the redirect URL is safe (internal to the application)"""
    if not target:
        return False
    # Parse the URL
    parsed = urlparse(target)
    # Allow only relative URLs (no netloc) or URLs with empty/None netloc
    return not parsed.netloc

# Home page
@app.route('/')
def index():
    courses = Course.query.limit(6).all()
    internships = Internship.query.limit(3).all()
    projects = Project.query.limit(3).all()
    feedback = Feedback.query.filter_by(approved=True).limit(4).all()
    return render_template('index.html', courses=courses, internships=internships, projects=projects, feedback=feedback)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
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
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    user_enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    user_applications = Application.query.filter_by(user_id=current_user.id).all()
    user_certificates = Certificate.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard/user_dashboard.html', 
                         enrollments=user_enrollments, 
                         applications=user_applications, 
                         certificates=user_certificates)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_courses = Course.query.count()
    total_internships = Internship.query.count()
    total_applications = Application.query.count()
    pending_feedback = Feedback.query.filter_by(approved=False).count()
    pending_contacts = Contact.query.filter_by(status='pending').count()
    
    return render_template('dashboard/admin_dashboard.html',
                         total_users=total_users,
                         total_courses=total_courses,
                         total_internships=total_internships,
                         total_applications=total_applications,
                         pending_feedback=pending_feedback,
                         pending_contacts=pending_contacts)

# Courses
@app.route('/courses')
def courses():
    page = request.args.get('page', 1, type=int)
    level = request.args.get('level', '')
    
    query = Course.query
    if level:
        query = query.filter_by(level=level)
    
    courses = query.paginate(page=page, per_page=9, error_out=False)
    return render_template('courses/courses.html', courses=courses, selected_level=level)

@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    is_enrolled = False
    if current_user.is_authenticated:
        is_enrolled = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first() is not None
    return render_template('courses/course_detail.html', course=course, is_enrolled=is_enrolled)

@app.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    course = Course.query.get_or_404(course_id)
    existing_enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    
    if existing_enrollment:
        flash('You are already enrolled in this course.', 'info')
    else:
        enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash('Successfully enrolled in the course!', 'success')
    
    return redirect(url_for('course_detail', course_id=course_id))

# Admin course management
@app.route('/admin/courses')
@login_required
def admin_courses():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses)

@app.route('/admin/courses/add', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            duration=form.duration.data,
            level=form.level.data,
            price=form.price.data or 0.0
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin_courses'))
    
    return render_template('admin/add_course.html', form=form)

# Internships
@app.route('/internships')
def internships():
    page = request.args.get('page', 1, type=int)
    internships = Internship.query.paginate(page=page, per_page=6, error_out=False)
    return render_template('internships/internships.html', internships=internships)

@app.route('/internships/<int:internship_id>')
def internship_detail(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    has_applied = False
    if current_user.is_authenticated:
        has_applied = Application.query.filter_by(user_id=current_user.id, internship_id=internship_id).first() is not None
    return render_template('internships/internship_detail.html', internship=internship, has_applied=has_applied)

@app.route('/internships/<int:internship_id>/apply', methods=['GET', 'POST'])
@login_required
def apply_internship(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    existing_application = Application.query.filter_by(user_id=current_user.id, internship_id=internship_id).first()
    
    if existing_application:
        flash('You have already applied for this internship.', 'info')
        return redirect(url_for('internship_detail', internship_id=internship_id))
    
    form = ApplicationForm()
    if form.validate_on_submit():
        resume_path = None
        if form.resume.data:
            filename = secure_filename(form.resume.data.filename)
            filename = f"{current_user.id}_{internship_id}_{filename}"
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.resume.data.save(resume_path)
        
        application = Application(
            user_id=current_user.id,
            internship_id=internship_id,
            resume_path=resume_path,
            cover_letter=form.cover_letter.data
        )
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('internship_detail', internship_id=internship_id))
    
    return render_template('internships/apply.html', form=form, internship=internship)

# Projects
@app.route('/projects')
def projects():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.paginate(page=page, per_page=6, error_out=False)
    return render_template('projects/projects.html', projects=projects)

@app.route('/projects/<int:project_id>/request')
@login_required
def request_project(project_id):
    project = Project.query.get_or_404(project_id)
    # Create a contact entry for project request
    contact = Contact(
        name=current_user.name,
        email=current_user.email,
        subject=f"Project Request: {project.title}",
        message=f"I am interested in the project: {project.title}. Please contact me for further discussion."
    )
    db.session.add(contact)
    db.session.commit()
    flash('Project request sent successfully! We will contact you soon.', 'success')
    return redirect(url_for('projects'))

# Certificate verification
@app.route('/verify-certificate', methods=['GET', 'POST'])
def verify_certificate():
    form = CertificateVerifyForm()
    certificate = None
    
    if form.validate_on_submit():
        certificate = Certificate.query.filter_by(certificate_code=form.certificate_code.data).first()
        if not certificate:
            flash('Certificate not found. Please check the code and try again.', 'danger')
    
    return render_template('certificates/verify.html', form=form, certificate=certificate)

# Feedback
@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            user_id=current_user.id,
            course_name=form.course_name.data,
            rating=form.rating.data,
            message=form.message.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback! It will be reviewed before being published.', 'success')
        return redirect(url_for('feedback'))
    
    return render_template('feedback/feedback.html', form=form)

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact/contact.html', form=form)

# Admin certificate management
@app.route('/admin/certificates', methods=['GET', 'POST'])
@login_required
def admin_certificates():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = CertificateForm()
    form.user_id.choices = [(u.id, f"{u.name} ({u.email})") for u in User.query.all()]
    
    if form.validate_on_submit():
        certificate = Certificate(
            user_id=form.user_id.data,
            course_name=form.course_name.data,
            certificate_code=generate_certificate_code()
        )
        db.session.add(certificate)
        db.session.commit()
        flash(f'Certificate generated successfully! Code: {certificate.certificate_code}', 'success')
        return redirect(url_for('admin_certificates'))
    
    certificates = Certificate.query.all()
    return render_template('admin/certificates.html', form=form, certificates=certificates)

# Admin feedback management
@app.route('/admin/feedback')
@login_required
def admin_feedback():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    pending_feedback = Feedback.query.filter_by(approved=False).all()
    approved_feedback = Feedback.query.filter_by(approved=True).all()
    
    return render_template('admin/feedback.html', 
                         pending_feedback=pending_feedback, 
                         approved_feedback=approved_feedback)

@app.route('/admin/feedback/<int:feedback_id>/approve', methods=['POST'])
@login_required
def approve_feedback(feedback_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    feedback = Feedback.query.get_or_404(feedback_id)
    feedback.approved = True
    db.session.commit()
    flash('Feedback approved successfully!', 'success')
    return redirect(url_for('admin_feedback'))

# File uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
