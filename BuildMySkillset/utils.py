import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture, folder):
    """Save uploaded picture with a random filename"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', folder, picture_fn)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    # Resize image if it's too large
    output_size = (800, 600)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fn

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_date(date):
    """Format date for display"""
    return date.strftime('%B %d, %Y')

def format_datetime(datetime):
    """Format datetime for display"""
    return datetime.strftime('%B %d, %Y at %I:%M %p')
