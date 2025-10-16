from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import httpx
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CAT_FACT_API_URL = "https://catfact.ninja/fact"
CAT_FACT_TIMEOUT = 5.0


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Initializes the httpx client on startup and closes it on shutdown.
    """
    logger.info("Application starting up: Initializing HTTP client...")
    app.state.http_client = httpx.AsyncClient() 
    
    yield 
    
    logger.info("Application shutting down: Closing HTTP client...")
    await app.state.http_client.aclose()


app = FastAPI(lifespan=lifespan) 


@app.get("/me", response_class=JSONResponse)
async def read_profile():
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    cat_fact = "Could not fetch a cat fact at the moment."
    
    try:
        response = await app.state.http_client.get(
            CAT_FACT_API_URL, 
            timeout=CAT_FACT_TIMEOUT
        )
        
        response.raise_for_status() 

        data = response.json()
        cat_fact = data.get("fact", cat_fact) 
        
        logger.info("Successfully fetched cat fact.")

    except httpx.TimeoutException:
        logger.error(f"Cat Facts API call timed out after {CAT_FACT_TIMEOUT}s.")
    except httpx.NetworkError as e:
        logger.error(f"Network error while calling Cat Facts API: {e.__class__.__name__}")
    except httpx.HTTPStatusError as e:
        logger.error(f"Cat Facts API returned non-200 status: {e.response.status_code}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e.__class__.__name__}")
    
    return {
        "status": "success",
        "user": {
            "email": "aukatsayal001@gmail.com",
            "name": "Abdullahi Umar Katsayal",
            "stack": "Python/FastAPI"
        },
        "timestamp": timestamp,
        "fact": cat_fact 
    }

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Backend Wizards Stage 0 API.",
        "instructions": "Navigate to the /me endpoint to see the dynamic profile information and a random cat fact.",
        "endpoint": "/me"
    }