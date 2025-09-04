import re
import streamlit as st

# --- Knowledge base (simplified) ---

SYMPTOM_SYNONYMS = {
    "fever": ["fever", "temperature", "hot", "chills"],
    "cough": ["cough", "coughing"],
    "sore throat": ["sore throat", "throat pain", "scratchy throat", "tonsil"],
    "runny nose": ["runny nose", "stuffy nose", "congestion", "blocked nose", "sneezing"],
    "headache": ["headache", "migraine", "head pain"],
    "fatigue": ["tired", "fatigue", "exhausted", "weak"],
    "body aches": ["body ache", "muscle pain", "aches", "soreness"],
    "nausea": ["nausea", "queasy", "nauseous"],
    "vomiting": ["vomit", "vomiting", "throwing up"],
    "diarrhea": ["diarrhea", "loose stools"],
    "stomach pain": ["stomach ache", "stomach pain", "abdominal pain", "cramps"],
    "shortness of breath": ["shortness of breath", "trouble breathing", "breathless", "wheezing"],
    "chest pain": ["chest pain", "pressure in chest", "tightness chest"],
    "dizziness": ["dizzy", "lightheaded"],
    "rash": ["rash", "hives", "skin rash"],
    "ear pain": ["earache", "ear pain"],
    "eye irritation": ["red eye", "itchy eye", "watery eye"],
}

REMEDIES = {
    "fever": ["Rest and drink plenty of fluids.",
              "Use a cool compress on the forehead.",
              "Over-the-counter fever reducers may help (check label & safety)."],
    "cough": ["Sip warm fluids (herbal tea with honey if not for infants).",
              "Try steam inhalation or a humidifier."],
    "sore throat": ["Gargle warm salt water.",
                    "Drink warm liquids (honey + lemon, not for infants)."],
    "runny nose": ["Use saline sprays.",
                   "Stay hydrated and rest."],
    "headache": ["Rest in a quiet, dark room.",
                 "Stay hydrated."],
    "fatigue": ["Prioritize rest.",
                "Stay hydrated and eat balanced meals."],
    "nausea": ["Small sips of clear fluids.",
               "Eat bland foods like bananas, rice, toast."],
    "vomiting": ["Rehydrate slowly with small sips of fluids.",
                 "Seek help if you can't keep fluids down."],
    "diarrhea": ["Drink oral rehydration solutions.",
                 "Eat simple, low-fat foods."],
    "stomach pain": ["Apply a warm compress to abdomen.",
                     "Eat bland foods and avoid irritants."],
}

RED_FLAG_PATTERNS = [
    r"\b(chest pain|pressure in chest|tightness chest)\b",
    r"\b(shortness of breath|trouble breathing|breathless|bluish lips)\b",
    r"\b(confusion|fainting|unresponsive|seizure)\b",
    r"\b(severe headache|stiff neck)\b",
    r"\b(continuous vomiting|vomiting blood)\b",
    r"\b(blood in stool|black tarry stools)\b",
    r"\b(severe abdominal pain)\b",
    r"\b(very high fever|> ?39\.?5? ?c|> ?103 ?f)\b",
]

# --- Helpers ---
def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def detect_symptoms(user_text: str):
    found = set()
    text = normalize(user_text)
    for canon, keys in SYMPTOM_SYNONYMS.items():
        for k in keys:
            if k in text:
                found.add(canon)
                break
    return sorted(found)

def has_red_flags(user_text: str) -> bool:
    text = normalize(user_text)
    for pat in RED_FLAG_PATTERNS:
        if re.search(pat, text):
            return True
    return False

# --- Streamlit app ---
st.title("🩺 Simple Health Check Chatbot")
st.caption("This is for *information only* — not a medical diagnosis. Seek professional care if unsure.")

with st.form("chat_form"):
    feeling = st.text_area("How are you feeling today?", placeholder="Example: I have a sore throat and mild fever")
    duration = st.text_input("How long has this been going on?", placeholder="e.g., 2 days")
    temp = st.text_input("Temperature (optional)", placeholder="e.g., 38.5 C or 101 F")
    more = st.text_area("Other symptoms/details?", placeholder="e.g., nausea, chest tightness")
    submitted = st.form_submit_button("Check")

if submitted:
    all_text = " ".join([feeling, duration, temp, more])
    red_flag = has_red_flags(all_text)
    symptoms = detect_symptoms(all_text)

    st.subheader("Summary")
    if symptoms:
        st.write("*Detected symptoms:*", ", ".join(symptoms))
    else:
        st.write("I couldn’t match specific symptoms, but here’s some general advice.")

    if red_flag:
        st.error("⚠ Important: Some of what you shared suggests this may be serious. Please seek medical attention immediately or call your local emergency number if you feel unsafe.")
    else:
        tips = []
        for s in symptoms:
            tips.extend(REMEDIES.get(s, []))
        tips.extend([
            "Rest as needed and keep well hydrated.",
            "If you use over-the-counter medicines, read the label and follow local guidance.",
            "If symptoms persist, worsen, or you are concerned, seek medical care."
        ])

        seen, filtered = set(), []
        for t in tips:
            if t not in seen:
                filtered.append(t)
                seen.add(t)

        st.subheader("General Self-Care Tips")
        for t in filtered[:10]:
            st.markdown(f"- {t}")

    st.divider()
    st.caption("⚠ This chatbot is for *educational purposes only*. It is not a substitute for professional medical advice, diagnosis, or treatment.")