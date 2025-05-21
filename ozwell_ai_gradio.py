import gradio as gr
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_token():
    """
    Load the API token from the .env file.
    """
    token = os.getenv("OZWELL_API")
    if not token:
        raise Exception("OZWELL_API key not found in .env file.")
    return token

def call_bluehive_api(prompt, system_message, token):
    url = "https://ai.bluehive.com/api/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "prompt": prompt,
        "systemMessage": system_message
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nResponse: {response.text}"
    except Exception as err:
        return f"Other error occurred: {err}"

def build_prompt(conversation):
    prompt_lines = []
    for role, text in conversation:
        if role == "user":
            prompt_lines.append(f"User: {text}")
        elif role == "assistant":
            prompt_lines.append(f"Assistant: {text}")
    return "\n".join(prompt_lines)

def respond(user_input, history):
    if history is None:
        history = []
    
    history.append(("user", user_input))
    prompt_text = build_prompt(history)
    
    token = load_token()
    system_message = "You are a helpful chatbot named Will. Always maintain context."
    response = call_bluehive_api(prompt_text, system_message, token)
    
    if isinstance(response, str):
        bot_reply = response
    else:
        try:
            bot_reply = response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            bot_reply = "Invalid response format received."
    
    history.append(("assistant", bot_reply))
    return history, history

# Build Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# BlueHive Conversational Demo")
    
    chatbot = gr.Chatbot()
    with gr.Row():
        user_input = gr.Textbox(
            show_label=False,
            placeholder="Type your message here...",
            lines=1
        )
        send_btn = gr.Button("Send")  # 👈 Add Send button next to textbox

    state = gr.State([])

    # Bind submit from textbox (Enter key)
    user_input.submit(
        fn=respond,
        inputs=[user_input, state],
        outputs=[chatbot, state]
    )

    # Bind Send button click
    send_btn.click(
        fn=respond,
        inputs=[user_input, state],
        outputs=[chatbot, state]
    )

if __name__ == "__main__":
    demo.launch(share=True)