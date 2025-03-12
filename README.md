# Face Recognition Authentication API

This is a Flask-based API for face recognition authentication. It allows users to sign up using their face images and log in by matching their facial features.

## Features
- User sign-up with face encoding storage.
- User login with face recognition authentication.
- Secure file uploads and encodings storage.
- JSON-based response handling.

## Technologies Used
- Python
- Flask
- face_recognition (Dlib-based face recognition library)
- NumPy
- Werkzeug

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/face-recognition-auth.git
   cd face-recognition-auth      

2. Install dependencies

   ```sh
   pip install -r requirements.txt

3. Run the Flask application
   ```sh
   python app.py

## API Endpoints 

1. User Signup (/signup)
 - Method: POST
- Description: Registers a new user by storing their face encoding.
- Form Data:
- image (file) - The image of the user.
- user_id (string) - Unique user identifier.
- Example CURL Request:

   ```sh
   curl -X POST http://127.0.0.1:5000/signup \
   -F "image=@path_to_your_image.jpg" \
   -F "user_id=example_user"
   
- Response
   ```sh
      {
     "message": "Signup successful",
     "user_id": "example_user"
      }

2. User Login(/login)
- Method: POST
- Description: Authenticates a user by comparing the uploaded face with stored encodings.
- Form Data:
    - image (file) - The image of the user.
- Example CURL Request:
   ```sh
   curl -X POST http://127.0.0.1:5000/login \
   -F "image=@path_to_your_image.jpg"

- Response (Successful Login):
  ```sh
  {
  "message": "Login successful",
  "user_id": "example_user"
   }
- Response (Failed Login):
  ```sh
  {
  "error": "Not in the system"
   }

# File Structure
 ```bash
face-recognition-auth/
│── uploads/           # Directory where uploaded images are stored
│── app.py             # Main Flask application
│── requirements.txt   # Required dependencies
│── encodings.txt      # JSON file storing face encodings
│── README.md          # Documentation






