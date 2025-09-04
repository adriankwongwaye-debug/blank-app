import openai

# Replace with your own OpenAI API key
openai.api_key = "your-api-key-here"

def get_ai_response(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",  # or gpt-3.5, gpt-4 if available
        prompt=f"User: {user_input}\nAI: ",
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def chatbot():
    print("🤖 Hello! I'm your health assistant bot.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("AI: Goodbye! Stay healthy!")
            break
        
        ai_response = get_ai_response(user_input)
        print(f"AI: {ai_response}")

chatbot()
