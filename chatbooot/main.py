from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model_interface import ModelInterface

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# LAZY LOADING DU MODELE (IMPORTANT)
# ======================================
model_interface = None

def get_model():
    global model_interface
    if model_interface is None:
        print("⏳ Chargement du modèle RH...")
        model_interface = ModelInterface()
        print("✅ Modèle RH chargé")
    return model_interface

# ======================================
# MODELES
# ======================================
class LoginInput(BaseModel):
    identifiant: str
    mdp: str

class ChatInput(BaseModel):
    input_text: str
    profil: str

# ======================================
# ROUTES
# ======================================
@app.get("/status/")
def status():
    return {"status": "OK"}

@app.get("/warmup/")
def warmup():
    get_model()
    return {"status": "model loaded"}

@app.post("/login/")
def login(data: LoginInput):
    model = get_model()
    profil = model.authenticate_user(data.identifiant, data.mdp)
    if profil:
        return {"success": True, "profil": profil}
    return {"success": False}

@app.post("/chat_messages/")
def chat_messages(data: ChatInput):
    model = get_model()
    response = model.get_message_response(
        data.input_text,
        data.profil
    )
    return {"agent": response}

@app.get("/kpis/")
def kpis():
    model = get_model()
    return model.get_kpis()
