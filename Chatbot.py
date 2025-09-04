import streamlit as st
import pandas as pd
import spacy

# Load a simple medical NER model (scispaCy)
@st.cache_resource
def load_model():
    return spacy.load("en_ner_bc5cdr_md")  # For diseases and chemicals

nlp = load_model()

# Simplified mapping of test results to common diseases
diagnosis_map = {
    "Hemoglobin": ["Anemia"],
    "Glucose": ["Diabetes"],
    "Platelet": ["Dengue", "Thrombocytopenia"],
    "WBC": ["Infection"],
    "Cholesterol": ["High Cholesterol", "Heart Risk"],
}

st.title("🩺 Simple AI-Powered Blood Test Analyzer")

st.markdown("This tool helps analyze basic blood test results and detect common conditions. For any serious or persistent symptoms, please consult a healthcare professional.")

uploaded_file = st.file_uploader("📤 Upload a blood test CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Report")
    st.write(df)

    st.subheader("🚦 Abnormal Results & Possible Conditions")
    results = []

    for _, row in df.iterrows():
        try:
            test = row["Test"]
            value = float(row["Value"])
            norm_range = row["NormalRange"]
            low, high = map(float, norm_range.split("-"))

            if value < low or value > high:
                possible_conditions = diagnosis_map.get(test, [])
                results.append({
                    "Test": test,
                    "Value": value,
                    "NormalRange": norm_range,
                    "PossibleCondition": ", ".join(possible_conditions) if possible_conditions else "N/A"
                })
        except Exception as e:
            st.error(f"Error processing row: {row}. Error: {e}")

    if results:
        abnormal_df = pd.DataFrame(results)
        st.dataframe(
            abnormal_df.style.applymap(
                lambda x: "color:red" if isinstance(x, (int, float, float)) else None,
                subset=["Value"]
            )
        )
        st.warning("⚠ Some results are outside the normal range. Please consult a doctor if you are experiencing symptoms.")
    else:
        st.success("✅ All test values are within normal range!")

    st.subheader("🧠 Extracted Health Terms from Doctor Notes")

    text_input = st.text_area("Paste doctor's notes or describe your symptoms:")

    if st.button("Analyze Text"):
        if text_input:
            doc = nlp(text_input)
            found_terms = []

            for ent in doc.ents:
                if ent.label_.lower() in ["disease", "chemical"]:
                    found_terms.append(ent.text)

            if found_terms:
                st.write("### 🔍 Possible medical terms found:")
                for term in set(found_terms):
                    st.write(f"- *{term}*")

                st.warning("⚠ This tool is for *educational purposes only. If symptoms are serious or persist, seek **professional medical advice*.")
            else:
                st.success("✅ No major medical terms detected.")
        else:
            st.info("Please enter some notes to analyze.")

st.markdown("---")
st.info("📌 *Disclaimer:* This tool is not a substitute for professional medical advice. Always consult a licensed doctor for health concerns.")