from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('Passwords must match.')

class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired(), Length(max=50)])
    level = SelectField('Level', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], validators=[DataRequired()])
    price = FloatField('Price', validators=[NumberRange(min=0)])

class InternshipForm(FlaskForm):
    title = StringField('Internship Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired(), Length(max=50)])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    location = StringField('Location', validators=[Length(max=100)])
    stipend = StringField('Stipend', validators=[Length(max=50)])

class ApplicationForm(FlaskForm):
    resume = FileField('Resume', validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Only PDF and DOC files allowed!')])
    cover_letter = TextAreaField('Cover Letter', validators=[Length(max=1000)])

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    tech_stack = StringField('Technology Stack', validators=[DataRequired(), Length(max=200)])
    budget_range = StringField('Budget Range', validators=[Length(max=50)])
    timeline = StringField('Timeline', validators=[Length(max=50)])

class CertificateForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    course_name = StringField('Course Name', validators=[DataRequired(), Length(max=200)])

class FeedbackForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired(), Length(max=200)])
    rating = SelectField('Rating', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], coerce=int, validators=[DataRequired()])
    message = TextAreaField('Review', validators=[DataRequired(), Length(max=1000)])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])

class CertificateVerifyForm(FlaskForm):
    certificate_code = StringField('Certificate Code', validators=[DataRequired(), Length(max=50)])
