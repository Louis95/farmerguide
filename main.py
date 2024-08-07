import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from modules.routers import (
    crop,
    crop_disease,
    farming_advice,
    soil_health,
    users,
    weather_forcast,
)
from modules.utilities.responses import base_responses

# region Environment Variables and Global Variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

ENVIRONMENT = os.getenv("RUN_ENV", "local")

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Driven Farming Guide API",
    description="An AI driven farming guide ",
    responses={**base_responses},
    openapi_url="/api/v1/openapi.json",
    version="1.0",
    redoc_url="/docs",
)


app.include_router(users.router)
app.include_router(crop_disease.router)
app.include_router(farming_advice.router)
app.include_router(soil_health.router)
app.include_router(weather_forcast.router)
app.include_router(crop.router)

if __name__ == "__main__":
    load_dotenv()
    if "DATABASE_URL" in os.environ:
        # noinspection PyTypeChecker
        api_host = os.getenv("API_HOST", "0.0.0.0")  # noqa: S104 - binding to all interfaces on purpose
        api_port = int(os.getenv("API_PORT", "8000"))
        if ENVIRONMENT == "local":
            uvicorn.run(
                "main:app",
                host=api_host,
                port=api_port,
                reload=True,
            )
        else:
            uvicorn.run(app, host=api_host, port=api_port)
    else:
        sys.stderr.write(
            "Variable DATABASE_URL cannot be found in environment. Put it in .env or in "
            "the DATABASE_URL environment variable\n"
        )
