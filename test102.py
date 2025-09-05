import streamlit as st
import pandas as pd
from transformers import pipeline
import google.generativeai as genai

# Step 1: Configure your API key
genai.configure(api_key="YOUR_API_KEY_HERE")

# Step 2: Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Step 3: Simple chat assistant loop
def ai_assistant():
    print("👋 Hi! I'm your AI assistant powered by Google Gemini.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break

        response = model.generate_content(user_input)
        print("Gemini:", response.text.strip())

# Run the assistant
ai_assistant()
