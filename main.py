from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Import both of your engines!
from donor_engine import MatchingEngine
from triage_engine import TriageEngine 

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_URL = "postgresql://triage_db_i5sf_user:Um5MLaKyiwkE6Vd4wNWFQOTv1t6nOUhV@dpg-d8kpgjegvqtc73fm34b0-a.oregon-postgres.render.com/triage_db_i5sf"
donor_engine = MatchingEngine(DB_URL)
triage_engine = TriageEngine()

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- The Blood Donor Route (Already working) ---
@app.post("/request_blood", response_class=HTMLResponse)
def handle_blood_request(request: Request, blood_group: str = Form(...), urgency: str = Form(...)):
    matched_donors = donor_engine.find_optimal_donors(blood_group)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "donors": matched_donors, 
        "searched_group": blood_group
    })

# --- The NEW Symptom Triage Route ---
@app.post("/triage", response_class=HTMLResponse)
def handle_triage(request: Request, symptoms: str = Form(...)):
    
    # Pass the text to your ML engine
    disease, advice = triage_engine.diagnose(symptoms)
    
    # Send the results back to the frontend
    return templates.TemplateResponse("index.html", {
        "request": request,
        "symptoms_entered": symptoms,
        "predicted_disease": disease,
        "triage_advice": advice
    })