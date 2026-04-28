from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
# AUTH (NO DATABASE)
# =========================
@app.post("/signup")
def signup(user: User):
    return {"message": "Signup successful"}

@app.post("/login")
def login(user: User):
    return {"success": True, "message": "Login successful"}

# =========================
# VOLUNTEER
# =========================
@app.post("/add-volunteer")
def add_volunteer(volunteer: Volunteer):
    return {"message": "Volunteer added"}

# =========================
# NEED HELP
# =========================
@app.post("/help-request")
def help_request(data: HelpRequest):
    return {"message": "Help request submitted"}

# =========================
# WANT TO HELP
# =========================
@app.post("/offer-help")
def offer_help(data: HelpOffer):
    return {"message": "Offer submitted successfully"}

# =========================
# PROFILE
# =========================
@app.post("/profile")
def save_profile(data: Profile):
    return {"message": "Profile saved"}

@app.get("/profile")
def get_profile():
    return {"message": "Profile data"}

# =========================
# COMMUNITY
# =========================
@app.post("/add-post")
def add_post(post: Post):
    return {"message": "Post added"}

@app.get("/get-posts")
def get_posts():
    return []

# =========================
# CONTACT
# =========================
@app.post("/contact")
def contact(data: ContactMessage):
    return {"message": "Message sent"}

# =========================
# VOICE HELP
# =========================
@app.post("/voice-help")
def voice_help(data: VoiceRequest):
    return {"message": "Voice request submitted"}
