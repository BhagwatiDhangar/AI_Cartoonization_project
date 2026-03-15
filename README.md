# 🎨 AI Cartoonizer Web Application

## 📌 Project Overview
AI Cartoonizer is a web-based application that allows users to upload images and convert them into cartoon-style images using image processing techniques. The application provides multiple cartoon effects, payment simulation, image downloads, and history tracking.

The project is developed using Python, Streamlit, OpenCV, and SQLite.

---

# 🚀 Features

## 👤 User Authentication
- User Registration
- User Login
- Secure session management

## 🖼 Image Processing
- Upload images (JPG, PNG, JPEG)
- Multiple cartoon styles
- Image processing using OpenCV
- Real-time preview

## 🔄 Image Comparison
- Before and After comparison slider

## 💳 Payment System
- Payment simulation (Success / Failed / Cancelled)
- Transaction ID generation
- Payment history tracking

## ⬇ Download System
- Download processed image after payment
- Multiple formats (PNG, JPG)
- Download history tracking
- Re-download previously purchased images

## 🖼 Gallery
- View previously processed images
- Filter images by style
- Image history stored in database

## 👤 User Profile
- Username
- Email
- Account statistics
- Processing history

## 🎨 Modern UI
- Animated landing page
- Glassmorphism cards
- Gradient buttons
- Dark mode toggle
- Professional navbar

---

# 🛠 Technology Stack

Frontend:
- Streamlit
- HTML
- CSS

Backend:
- Python

Libraries:
- OpenCV
- Pillow
- NumPy
- SQLite3
- UUID
- Datetime

Database:
- SQLite

---

# 📂 Project Folder Structure

AI_Cartoonization_Project

frontend  
│── app.py  
│── styles.py  

uploads  

downloads  

database  
│── database.db  

README.md

---

# ⚙ Installation Guide

1. Clone the repository

git clone https://github.com/your-repo/cartoonizer-project.git

2. Open the project folder

cd AI_Cartoonization_Project

3. Install required libraries

pip install streamlit  
pip install opencv-python  
pip install pillow  
pip install numpy  

4. Run the application

streamlit run app.py

---

# 🖥 How to Use the Application

Step 1  
Register a new account.

Step 2  
Login to the application.

Step 3  
Upload an image.

Step 4  
Choose a cartoon style.

Step 5  
Click **Process Image**.

Step 6  
Go to the **Payment tab**.

Step 7  
Simulate payment.

Step 8  
Download the cartoonized image.

---

# 🗄 Database Tables

Users Table
- id
- username
- email
- password
- created_at

Image History Table
- id
- username
- image_path
- effect
- created_at

Transactions Table
- id
- user_id
- order_id
- payment_id
- amount
- status
- created_at

Downloads Table
- id
- user_id
- image_path
- download_time

---

# 🔒 Security Features
- Session-based login
- File type validation
- Secure database queries
- Error handling

---

# 🧪 Testing
The application was tested for:

- User registration validation
- Login authentication
- Image upload validation
- Image processing functionality
- Payment simulation
- Download functionality
- Database operations

---

# ⚠ Known Limitations
- Payment gateway is simulated (Razorpay not integrated).
- Large images may take longer to process.
- Limited cartoon styles.

---

# 🔮 Future Enhancements
- Real payment gateway integration
- More AI cartoon styles
- Cloud image storage
- Mobile responsive UI
- AI-based cartoon models

---

# 🎥 Demo
Users can register, upload an image, process it, simulate payment, and download the cartoonized image.

---

# 👨‍💻 Author
AI Cartoonizer Project  
Developed using Python and Streamlit.