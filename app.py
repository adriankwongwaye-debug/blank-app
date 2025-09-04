import streamlit as st
import pandas as pd
from transformers import pipeline

# Load OpenMed NER model (for disease extraction)
@st.cache_resource
def load_model():
    return pipeline("token-classification",
                    model="OpenMed/OpenMed-NER-OncologyDetect-SnowMed-568M",
                    aggregation_strategy="simple")

ner = load_model()

# Simple mapping of lab tests -> possible conditions
diagnosis_map = {
    "Hemoglobin": ["Anemia", "Iron deficiency"],
    "Glucose": ["Diabetes Mellitus", "Stress hyperglycemia"],
    "Platelet": ["Dengue", "Bone marrow disorder"],
    "WBC": ["Infection", "Leukemia"],
}

st.title("🩸 AI-Powered Blood Test Analyzer (Demo)")

uploaded_file = st.file_uploader("Upload a blood test CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Report")
    st.write(df)

    st.subheader("🚦 Abnormal Results & Possible Diagnoses")
    results = []

    for _, row in df.iterrows():
        test, value, norm = row["Test"], float(row["Value"]), row["NormalRange"]
        low, high = map(float, norm.split("-"))

        if value < low or value > high:
            # Find mapped diagnoses
            possible_diag = diagnosis_map.get(test, [])

            results.append({
                "Test": test,
                "Value": value,
                "NormalRange": norm,
                "PossibleDiagnosis": ", ".join(possible_diag) if possible_diag else "N/A"
            })

    if results:
        abnormal_df = pd.DataFrame(results)
        st.dataframe(abnormal_df.style.applymap(
            lambda x: "color:red" if isinstance(x, (int, float)) else None,
            subset=["Value"]
        ))
    else:
        st.success("✅ All parameters are within normal range!")

    st.subheader("🧠 AI Disease Entity Extraction (NER)")
    text_input = st.text_area("Paste report notes / doctor's comments here:")

    if st.button("Extract Medical Entities"):
        if text_input:
            entities = ner(text_input)
            for e in entities:
                st.write(f"**{e['word']}** → {e['entity_group']} (score: {e['score']:.2f})")
        else:
            st.warning("Please enter some text to analyze.")
