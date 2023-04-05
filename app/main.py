from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import api_routers
app = FastAPI(
    title="My fast api base project"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_routers)
