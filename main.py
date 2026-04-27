from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from datetime import datetime

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE CONNECTION
# =========================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Preet@5680",
        database="helpbridge_db"
    )

# =========================
# MODELS
# =========================

class User(BaseModel):
    name: str = None
    email: str
    password: str

class HelpRequest(BaseModel):
    name: str
    phone: str
    location: str
    help_type: str
    description: str

class HelpOffer(BaseModel):
    name: str
    phone: str
    location: str
    help_type: str
    description: str

class Volunteer(BaseModel):
    name: str
    dob: str
    gender: str
    phone: str
    email: str
    idType: str
    idNumber: str
    address: str
    skills: str
    availability: str

class Profile(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile: str
    address: str

class Post(BaseModel):
    username: str
    role: str
    content: str

class ContactMessage(BaseModel):
    name: str
    email: str
    message: str

class VoiceRequest(BaseModel):
    name: str
    mode: str
    type: str
    details: str

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# =========================
# AUTH
# =========================
@app.post("/signup")
def signup(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
        (user.name, user.email, user.password)
    )
    conn.commit()
    conn.close()
    return {"message": "Signup successful"}

@app.post("/login")
def login(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (user.email, user.password)
    )
    result = cursor.fetchone()
    conn.close()
    return {"success": True} if result else {"success": False}

# =========================
# VOLUNTEER
# =========================
@app.post("/add-volunteer")
def add_volunteer(volunteer: Volunteer):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO volunteers
        (name,dob,gender,phone,email,idType,idNumber,address,skills,availability)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        volunteer.name, volunteer.dob, volunteer.gender,
        volunteer.phone, volunteer.email,
        volunteer.idType, volunteer.idNumber,
        volunteer.address, volunteer.skills,
        volunteer.availability
    ))
    conn.commit()
    conn.close()
    return {"message": "Volunteer added"}

# =========================
# NEED HELP
# =========================
@app.post("/help-request")
def help_request(data: HelpRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO help_requests
        (name,phone,location,help_type,description)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        data.name, data.phone, data.location,
        data.help_type, data.description
    ))

    cursor.execute("""
        INSERT INTO activity_logs (title, description, time)
        VALUES (%s,%s,%s)
    """, (
        data.help_type,
        f"{data.name} requested help",
        datetime.now().strftime("%d %b %Y, %I:%M %p")
    ))

    conn.commit()
    conn.close()

    return {"message": "Help request submitted"}

# =========================
# ✅ WANT TO HELP (FIXED)
# =========================
@app.post("/offer-help")
def offer_help(data: HelpOffer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO help_offers
        (name,phone,location,help_type,description)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        data.name,
        data.phone,
        data.location,
        data.help_type,
        data.description
    ))

    conn.commit()
    conn.close()

    return {"message": "Offer submitted successfully"}

# =========================
# PROFILE
# =========================
@app.post("/profile")
def save_profile(data: Profile):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_profile
        (first_name,last_name,email,mobile,address)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        data.first_name,
        data.last_name,
        data.email,
        data.mobile,
        data.address
    ))
    conn.commit()
    conn.close()
    return {"message": "Profile saved"}

@app.get("/profile")
def get_profile():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    return data

# =========================
# COMMUNITY
# =========================
@app.post("/add-post")
def add_post(post: Post):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO community_posts (username,role,content) VALUES (%s,%s,%s)",
        (post.username, post.role, post.content)
    )
    conn.commit()
    conn.close()
    return {"message": "Post added"}

@app.get("/get-posts")
def get_posts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM community_posts ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# =========================
# CONTACT
# =========================
@app.post("/contact")
def contact(data: ContactMessage):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contact_messages (name,email,message)
        VALUES (%s,%s,%s)
    """, (data.name, data.email, data.message))
    conn.commit()
    conn.close()
    return {"message": "Message sent"}

# =========================
# VOICE HELP
# =========================
@app.post("/voice-help")
def voice_help(data: VoiceRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO voice_requests (name,mode,type,details)
        VALUES (%s,%s,%s,%s)
    """, (
        data.name,
        data.mode,
        data.type,
        data.details
    ))

    conn.commit()
    conn.close()

    return {"message": "Voice request submitted"}