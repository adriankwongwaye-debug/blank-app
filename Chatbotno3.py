import gradio as gr
from transformers import pipeline

# Load a free conversational AI model
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-small")

# Function to handle user input
def health_bot(user_input, history=[]):
    # Rule-based check for severe symptoms
    severe_symptoms = ["chest pain", "difficulty breathing", "severe headache", "high fever", "fainting"]
    if any(symptom in user_input.lower() for symptom in severe_symptoms):
        reply = "⚠ That sounds serious. Please seek professional medical help immediately."
    else:
        # Generate a conversational response
        reply = chatbot(user_input, max_length=100, num_return_sequences=1)[0]["generated_text"]

    history.append((user_input, reply))
    return history, history

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Free Health Chatbot\nChat with me about how you're feeling. (Type 'exit' to quit)")

    chatbot_ui = gr.Chatbot()
    msg = gr.Textbox(placeholder="How are you feeling today?")
    clear = gr.Button("Clear Chat")

    def user_message(user_input, history):
        return "", health_bot(user_input, history)[0]

    msg.submit(user_message, [msg, chatbot_ui], [msg, chatbot_ui])
    clear.click(lambda: None, None, chatbot_ui, queue=False)

# Run app
demo.launch()