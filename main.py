from flask import Flask, request, jsonify
import json
import face_recognition
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ENCODINGS_FILE = "encodings.json"  # Changed to JSON file
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_encodings():
    try:
        with open(ENCODINGS_FILE, "r") as file:
            encodings = json.load(file)
            return {user_id: np.array(encoding) for user_id, encoding in encodings.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_encodings(encodings):
    with open(ENCODINGS_FILE, "w") as file:
        json.dump({user_id: encoding.tolist() for user_id, encoding in encodings.items()}, file)

def encode_face(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None  # Avoid IndexError

def match_face(input_encoding, stored_encodings):
    matches = face_recognition.compare_faces(stored_encodings, input_encoding)
    return any(matches)

@app.route("/signup", methods=["POST"])
def signup():
    if "image" not in request.files or "user_id" not in request.form:
        return jsonify({"error": "Missing image or user_id"}), 400
    
    image = request.files["image"]
    user_id = request.form["user_id"]
    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(image_path)
    
    encoding = encode_face(image_path)
    if encoding is None:
        return jsonify({"error": "No face detected"}), 400
    
    users = load_encodings()
    users[user_id] = encoding  # Store encoding as NumPy array
    save_encodings(users)
    
    return jsonify({"message": "Signup successful", "user_id": user_id})

@app.route("/login", methods=["POST"])
def login():
    if "image" not in request.files:
        return jsonify({"error": "Missing image"}), 400
    
    image = request.files["image"]
    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(image_path)
    
    input_encoding = encode_face(image_path)
    if input_encoding is None:
        return jsonify({"error": "No face detected"}), 400
    
    users = load_encodings()
    for user_id, stored_encoding in users.items():
        if match_face(input_encoding, [stored_encoding]):  # Ensure stored_encoding is a NumPy array
            return jsonify({"message": "Login successful", "user_id": user_id})
    
    return jsonify({"error": "Not in the system"}), 401

if __name__ == "__main__":
    app.run(debug=True)
