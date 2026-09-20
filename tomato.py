from flask import Flask, render_template, flash, redirect, url_for, session, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# =====================================
#           Database Creation
# =====================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())



class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detected_value = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# ================================================
#           Global Email Configuration
# ================================================

# Sender ( send email from this mail )
EMAIL_SENDER = "shubhamkalekar148@gmail.com"
EMAIL_PASSWORD = "dkpb kipr qdno envw"



@app.route('/')
def base():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    # Get page numbers separately
    d_page = request.args.get('d_page', 1, type=int)
    c_page = request.args.get('c_page', 1, type=int)

    # Detection pagination
    detection_pagination = Detection.query.order_by(
        Detection.created_at.desc()
    ).paginate(page=d_page, per_page=10)

    detections = detection_pagination.items

    # Contact pagination
    contact_pagination = Contact.query.order_by(
        Contact.created_at.desc()
    ).paginate(page=c_page, per_page=10)

    contact_object = contact_pagination.items

    detection_count = Detection.query.count()
    contact_count = Contact.query.count()

    return render_template(
        'dashboard.html',
        detections=detections,
        contact=contact_object,
        detection_pagination=detection_pagination,
        contact_pagination=contact_pagination,
        detection_count=detection_count,
        contact_count=contact_count
    )


# ===============================================
#                  OTP Based Login
# ===============================================

from flask_mail import Mail, Message
import random
import time

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = EMAIL_SENDER  # replace with your email
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD  # replace with your email password

mail = Mail(app)

# Store OTP and timestamp
otp_storage = {}


# Function to send OTP
def send_otp(email):
    otp = random.randint(100000, 999999)

    otp_storage[email] = {
        "otp": otp,
        "time": time.time()
    }

    session['otp_email'] = email

    subject = "Your OTP for Login"
    from_email = app.config['MAIL_USERNAME']
    recipient_list = [email]

    # Dummy text_content (since your code used it but not defined)
    text_content = f"Your OTP is {otp}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background-color: #f4f6f8;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 500px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .title {{
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }}
            .subtitle {{
                color: #555;
                font-size: 14px;
                margin-bottom: 25px;
            }}
            .otp-box {{
                font-size: 34px;
                font-weight: bold;
                color: white;
                background: linear-gradient(135deg, #667eea, #764ba2);
                padding: 15px 25px;
                border-radius: 10px;
                display: inline-block;
                letter-spacing: 5px;
                margin-bottom: 20px;
            }}
            .note {{
                font-size: 13px;
                color: #888;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="title">🔐 AgriSight – Smart Fruit Harvesting Robot</div>
            <div class="subtitle">
                Use the OTP below to securely log in
            </div>

            <div class="otp-box">{otp}</div>

            <div class="subtitle">
                This OTP is valid for <b>10 minutes</b><br>
                Do not share it with anyone
            </div>

            <div class="note">
                If you didn't request this, please ignore this email.
            </div>
        </div>
    </body>
    </html>
    """

    msg = Message(subject, sender=from_email, recipients=recipient_list)
    msg.body = text_content
    msg.html = html_content
    mail.send(msg)

    print("OTP Storage:", otp_storage)


@app.route('/otp_login', methods=['GET', 'POST'])
def otp_login_home():
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            flash("Email is required",'danger')
            return redirect(url_for('otp_login_home'))

        # Django User.objects.filter(email=email).exists()
        # Replace with simple placeholder check
        check_user_email_exist = True

        if check_user_email_exist:
            send_otp(email)
            flash(f"OTP sent successfully to {email}",'success')
            return redirect(url_for('verify_otp'))
        else:
            flash("Email is not registered",'danger')
            return redirect(url_for('otp_login_home'))

    return render_template('OTP/otp_login_home.html')


# ================= VERIFY OTP =================
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == "POST":
        otp = request.form.get("otp")
        email = session.get("otp_email")
        current_time = time.time()

        if not otp:
            flash("OTP is required",'danger')
            return redirect(url_for('verify_otp'))

        if not email or email not in otp_storage:
            flash("No OTP found. Please request again.",'danger')
            return redirect(url_for('otp_login_home'))

        stored_otp = otp_storage[email]["otp"]
        otp_time = otp_storage[email]["time"]

        # Check expiry
        if current_time - otp_time > 600:
            del otp_storage[email]
            flash("OTP has expired. Please request a new one.",'danger')
            return redirect(url_for('otp_login_home'))

        # Match OTP
        if int(otp) == stored_otp:
            # user = User.objects.filter(email=email).first()
            session['user_id'] = email  # using email as placeholder

            del otp_storage[email]
            session.pop('otp_email', None)

            flash("Logged in Successfully",'success')
            return redirect('/user_home')

        flash("Invalid OTP",'danger')
        return redirect(url_for('verify_otp'))

    return render_template('OTP/verify_otp.html')


# ================= RESEND OTP =================
@app.route('/resend_otp')
def resend_otp():
    email = session.get("otp_email")

    if not email:
        flash("No email found. Please login again.")
        return redirect(url_for('otp_login_home'))

    otp = random.randint(100000, 999999)

    otp_storage[email] = {
        "otp": otp,
        "time": time.time()
    }

    subject = "Your OTP for Login (Resent)"
    from_email = app.config['MAIL_USERNAME']
    recipient_list = [email]

    text_content = f"Your OTP is {otp}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h2>🔐 AgriSight – Smart Fruit Harvesting Robot</h2>
        <p><b>OTP Resent</b></p>
        <h1>{otp}</h1>
        <p>Valid for 10 minutes</p>
    </body>
    </html>
    """

    msg = Message(subject, sender=from_email, recipients=recipient_list)
    msg.body = text_content
    msg.html = html_content
    mail.send(msg)

    flash(f"New OTP has been sent to {email}", "success")
    return redirect(url_for('verify_otp'))


# ==========================================
#           Regular Functions
# ==========================================


@app.route('/login/', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.password, password):

            session['user_id'] = user.id
            session['user_name'] = user.username
            session['logged_in'] = True
            flash('Logged in successful.', 'success')
            return redirect(url_for('user_home'))  # redirect to index

        else:
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('base'))

    else:
        flash('Email not registered. Please sign up first.', 'danger')
        return redirect(url_for('base'))


def login_required(f):
    """
    Decorator to protect routes that require authentication.
    Redirects to login page if user is not logged in.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('logged_in'):
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered. Please login.', 'warning')
            return redirect(url_for('login'))

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('base'))

    return render_template('register.html')


@app.route('/contact', methods=['POST'])
def contact():
    full_name = request.form.get('full-name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
        new_contact = Contact(
            full_name=full_name,
            email=email,
            message=message
        )

        db.session.add(new_contact)
        db.session.commit()

        flash("Thank you for reaching out. We will respond to you shortly.", "success")

    except Exception as e:
        db.session.rollback()
        flash("Something went wrong. Please try again.", "danger")
        print(e)

    return redirect('/')


@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    flash('Logout Successfully', 'danger')
    return redirect(url_for('base'))


@app.route('/user_home')
@login_required
def user_home():
    # Retrieve user data from session
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    user_email = session.get('user_email')


    # Pass data to template
    return render_template(
        'user_home_new.html',
        user_id=user_id,
        user_name=user_name.title(),
        user_email=user_email,
    )


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/detect')
@login_required
def detect():
    return render_template("detect.html")


# ==============================================
#          Detection using Raspberry PI
# ==============================================

from ultralytics import YOLO
import cv2
import threading

model = YOLO("tomato.pt")

camera_running = False
cap = None

# -------------------------
# START CAMERA
# -------------------------


@app.route('/start_camera')
def start_camera():
    global camera_running

    camera_running = True
    print("▶️ Camera started")

    return {"status": "started"}


@app.route('/stop_camera')
def stop_camera():
    global camera_running, cap

    camera_running = False

    # 🔥 Force release camera immediately
    if cap is not None:
        cap.release()
        cap = None
        print("🛑 Camera force stopped")

    return {"status": "stopped"}


import time
from flask import Response

last_detected = None
last_saved_time = 0
SAVE_INTERVAL = 1  # seconds gap between DB saves

def generate_frames():
    global camera_running, last_detected, last_saved_time, cap

    SAVE_INTERVAL = 5  # seconds

    # ✅ Open camera only if needed
    def generate_frames():
     global camera_running, last_detected, last_saved_time, cap

    SAVE_INTERVAL = 5  # seconds

    # ✅ Open camera only if needed
    if cap is None or not cap.isOpened():

        print("Trying Camera 0...")
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        if not cap.isOpened():
            print("Camera 0 failed. Trying Camera 1...")
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            print("Camera 1 failed. Trying Camera 2...")
            cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

        if not cap.isOpened():
            print("❌ No camera detected.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("✅ Camera initialized")
        time.sleep(1)

    while True:

        # 🔴 Stop camera completely
        if not camera_running:
            if cap is not None:
                cap.release()
                cap = None
                print("🛑 Camera released")
            break

        ret, frame = cap.read()

        if not ret or frame is None:
            print("⚠️ Frame failed")
            continue

        # ✅ Force same size (fix bounding box issue)
        frame = cv2.resize(frame, (640, 480))

        # ✅ YOLO detection (better accuracy)
        results = model(frame, imgsz=640, conf=0.5, iou=0.5)

        detected_in_frame = None
        best_conf = 0

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                conf = float(box.conf[0])

                # ✅ pick highest confidence object
                if conf > best_conf:
                    best_conf = conf

                    cls_id = int(box.cls[0])
                    detected_in_frame = model.names[cls_id]

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Clamp coordinates
                    h, w, _ = frame.shape
                    x1 = max(0, min(x1, w))
                    y1 = max(0, min(y1, h))
                    x2 = max(0, min(x2, w))
                    y2 = max(0, min(y2, h))

                    # Draw box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, f"{detected_in_frame} {conf:.2f}",
                                (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # ✅ Save to DB (ONLY ONCE EVERY 5 SECONDS)
        current_time = time.time()

        if detected_in_frame and (current_time - last_saved_time > SAVE_INTERVAL):
            try:
                with app.app_context():
                    new_detection = Detection(detected_value=detected_in_frame)
                    db.session.add(new_detection)
                    db.session.commit()

                print("✅ Saved:", detected_in_frame)

                last_saved_time = current_time
                last_detected = detected_in_frame

            except Exception as e:
                print("DB Error:", e)
                with app.app_context():
                    db.session.rollback()

        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
