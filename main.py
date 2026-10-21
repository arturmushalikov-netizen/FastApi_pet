from contextlib import asynccontextmanager

from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from db import Base, add_request_data, engine, get_user_request
from gemini_client import get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("DB created")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Chat API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/requests")
async def get_my_request(request: Request):
    ip_address = request.client.host
    user_requests = get_user_request(user_ip=ip_address)
    return user_requests


@app.post("/requests")
async def send_prompt(
        request: Request, 
        prompt: str = Body(embed=True)
    ):
    ip_address = request.client.host
    answer = get_answer_from_gemini(prompt)
    add_request_data(
        user_ip = ip_address, 
        prompt = prompt, 
        response = answer
        )
    return {"answer": answer}
