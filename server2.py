# server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.utils import secure_filename
from functools import wraps
from flask import abort

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Upload folder setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Firebase Admin
# Path to Firebase Admin SDK JSON
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Dummy admin credentials (replace with env variables or secure method later)
ADMIN_EMAIL = "marcionaiene4@gmail.com"
ADMIN_PASSWORD = ""

# In-memory token for simplicity
auth_tokens = set()


def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f"Received Authorization token: '{token}'")  # Debug log
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------

# Admin Login Endpoint
# ---------------------------


@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data['email'] == ADMIN_EMAIL and data['password'] == ADMIN_PASSWORD:

        return jsonify({"status": "success", "token": token})
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

# Middleware-like function to check token


def check_auth(request):
    token = request.headers.get("Authorization")
    return token in auth_tokens

# ---------------------------
# Get All Students
# ---------------------------


@app.route('/admin/students', methods=['GET'])
@require_admin
def get_students():
    students = []
    docs = db.collection("students").stream()
    for doc in docs:
        student = doc.to_dict()
        student['id'] = doc.id
        students.append(student)
    return jsonify(students)

# ---------------------------
# Get Specific Student
# ---------------------------


@app.route('/admin/students/<id>', methods=['GET'])
@require_admin
def get_student(id):
    doc_ref = db.collection("students").document(id)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({"message": "Not found"}), 404

# ---------------------------
# Update Student Payment
# ---------------------------


@app.route('/admin/students/<id>', methods=['PATCH'])
@require_admin
def update_payment(id):
    data = request.json
    isPaid = data.get("isPaid")
    db.collection("students").document(id).update({"isPaid": isPaid})
    return jsonify({"message": "Payment status updated."})

# ---------------------------
# Delete Student
# ---------------------------


@app.route('/admin/students/<id>', methods=['DELETE'])
@require_admin
def delete_student(id):
    db.collection("students").document(id).delete()
    return jsonify({"message": "Student deleted."})


# ---------------------------
# File Upload Endpoint
# ---------------------------
@app.route('/upload', methods=['POST'])
@require_admin
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'fail', 'message': 'No file part'}), 400

    file = request.files['file']
    file_type = request.form.get('type')

    if file.filename == '':
        return jsonify({'status': 'fail', 'message': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({'status': 'success', 'filename': filename})


@app.route('/videos', methods=['GET'])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify(files)
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500


@app.route('/videos/<path:filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({'status': 'fail', 'message': 'File not found'}), 404


# Replace existing require_admin_login and auth_tokens with:
ADMIN_TOKEN = 'ENI9300'  # Set this to match frontend token


def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f"Received Authorization token: '{token}'")  # Debug log
        if token != ADMIN_TOKEN:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# File Delete Endpoint
# ---------------------------


@app.route('/delete/<filename>', methods=['DELETE'])
@require_admin
def delete_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'status': 'success', 'message': f'{filename} deleted'})
        else:
            return jsonify({'status': 'fail', 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500


# ---------------------------
# Run App
# ---------------------------
if __name__ == '__main__':
    app.run(port=5050)
