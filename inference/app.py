from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# CORS middleware to allow requests from frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in production
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define message model for API
class Message(BaseModel):
    role: str
    content: str

# Chat history management
class ChatManager:
    def __init__(self):
        self.sessions = {}

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, [])

    def add_message(self, session_id: str, message: Message):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(message)

chat_manager = ChatManager()

# Define endpoint for OpenAI chat completions
@app.post("/chat")
def chat_endpoint(session_id: str, message: Message):
    chat_manager.add_message(session_id, message)
    history = chat_manager.get_history(session_id)
    print(history)

    # Convert history to OpenAI API format
    formatted_history = [
        {"role": msg.role, "content": msg.content} for msg in history
    ]

    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=formatted_history
        )

        # Get assistant's response
        assistant_message = response.choices[0].message.content
        chat_manager.add_message(session_id, Message(role="assistant", content=assistant_message))

        return {"role": "assistant", "content": assistant_message}
    except Exception as e:
        raise e

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = None

    try:
        while True:
            data = await websocket.receive_json()
            if "session_id" in data:
                session_id = data["session_id"]

            user_message = Message(role="user", content=data["message"])
            chat_manager.add_message(session_id, user_message)

            # Convert chat history to OpenAI API format
            history = chat_manager.get_history(session_id)
            formatted_history = [
                {"role": msg.role, "content": msg.content} for msg in history
            ]

            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=formatted_history
            )
            assistant_message = response["choices"][0]["message"]

            # Add assistant's message to history and send it to the client
            chat_manager.add_message(session_id, Message(role="assistant", content=assistant_message["content"]))
            await websocket.send_json({"reply": assistant_message["content"]})

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")

# Run with: uvicorn app:app --reload
