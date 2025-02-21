from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from models import db, Realtor, Property, PropertyPhoto
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u2cch0htlm8mg2:p79a5b6c1cdc7e523a1978c34d01c651f82ebb1c599d9e3b0dd95a0e27898d8cf@c9mq4861d16jlm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d32ncghf1gn534'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# S3 configuration at root level
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)
BUCKET_NAME = 'inmota'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'@login_manager.user_loader
def load_user(user_id):
    return Realtor.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        realtor = Realtor.query.filter_by(email=email).first()
        if realtor and check_password_hash(realtor.password_hash, password):
            login_user(realtor)
            return redirect(url_for('properties'))
        
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        if Realtor.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        realtor = Realtor(
            name=name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(realtor)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/properties')
@login_required
def properties():
    properties = Property.query.filter_by(realtor_id=current_user.id).all()
    return render_template('properties.html', properties=properties)




def upload_file_to_s3(file, filename):
      try:
          s3.upload_fileobj(
              file,
              BUCKET_NAME,
              filename,
              ExtraArgs={'ACL': 'public-read'}
          )
          return f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
      except ClientError as e:
          return None
@app.route('/properties/add', methods=['GET', 'POST'])
@login_required
def add_property():
      if request.method == 'POST':
          property = Property(
              realtor_id=current_user.id,
              title=request.form.get('title'),
              description=request.form.get('description'),
              location=request.form.get('location'),
              price=float(request.form.get('price')),
              property_type=request.form.get('property_type'),
              area=float(request.form.get('area')),
              bedrooms=int(request.form.get('bedrooms')),
              bathrooms=int(request.form.get('bathrooms')),
              status='available'
          )
        
          db.session.add(property)
          db.session.commit()
        
          # Handle photo uploads
          if 'photos' in request.files:
              photos = request.files.getlist('photos')
              for photo in photos:
                  if photo.filename:
                      filename = secure_filename(photo.filename)
                      s3_url = upload_file_to_s3(photo, filename)
                      if s3_url:
                          property_photo = PropertyPhoto(
                              property_id=property.id,
                              photo_url=s3_url
                          )
                          db.session.add(property_photo)
            
              db.session.commit()
        
          flash('Property added successfully!', 'success')
          return redirect(url_for('properties'))
    
      return render_template('property_form.html')
@app.route('/properties/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_property(id):
    property = Property.query.get_or_404(id)
    
    if property.realtor_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('properties'))
    
    if request.method == 'POST':
        property.title = request.form.get('title')
        property.description = request.form.get('description')
        property.location = request.form.get('location')
        property.price = float(request.form.get('price'))
        property.property_type = request.form.get('property_type')
        property.area = float(request.form.get('area'))
        property.bedrooms = int(request.form.get('bedrooms'))
        property.bathrooms = int(request.form.get('bathrooms'))
        
        # Handle new photo uploads
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            for photo in photos:
                if photo.filename:
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    
                    property_photo = PropertyPhoto(
                        property_id=property.id,
                        photo_url=f'/static/uploads/{filename}'
                    )
                    db.session.add(property_photo)
        
        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('properties'))
    
    return render_template('property_form.html', property=property)

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        db.create_all()
    app.run(debug=True)
