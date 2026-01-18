from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import classify, health

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://email-ai-js-py.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas
app.include_router(health.router)
app.include_router(classify.router)
