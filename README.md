# Backend Wizards Stage 0: Dynamic Profile Endpoint - FastAPI

## 🎯 Task Overview

This project implements the Stage 0 task for the Backend Wizards challenge. It provides a robust, single RESTful API endpoint at `/me` that returns static profile information, a dynamic UTC timestamp, and a random cat fact fetched from an external API.

## 🛠️ Tech Stack

  * **Language:** Python 3.10+
  * **Framework:** FastAPI
  * **ASGI Server:** Uvicorn
  * **HTTP Client:** `httpx` (for asynchronous, robust external API calls)

-----

## 📦 Prerequisites

You must have **Python 3.10** or higher installed.

## ⚙️ Installation and Setup

### 1\. Clone the Repository

```bash
# Replace <YOUR_REPO_LINK> with the actual link
git clone <YOUR_REPO_LINK>
cd 1catfacts
```

### 2\. Create and Activate Virtual Environment

```bash
# Create the environment
python -m venv venv

# Activate the environment (on Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate the environment (on Linux/macOS or Git Bash)
source venv/bin/activate
```

### 3\. Install Dependencies

This project requires `fastapi`, `uvicorn`, and `httpx`.

```bash
# Install packages
pip install fastapi uvicorn httpx
```

-----

## ▶️ Instructions to Run Locally

### 1\. Start the API Server

Run the application using Uvicorn from the root project directory (assuming your main application file is at `api/main.py`):

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start, typically running on `http://127.0.0.1:8000`.

### 2\. Test the Endpoint

Access the required endpoint using your browser, Postman, or `curl`:

```bash
curl http://localhost:8000/me
```

-----

## 📋 Endpoint Details

| Field | Value | Notes |
| :--- | :--- | :--- |
| **Method** | `GET` |
| **Path** | `/me` |
| **Status Code (Success)** | `200 OK` | Required even if the external API fails. |
| **Content-Type** | `application/json` |

### **Successful Response Structure (Example)**

```json
{
  "status": "success",
  "user": {
    "email": "aukatsayal001@gmail.com",
    "name": "Abdullahi Umar Katsayal",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-16T17:30:00.123Z",
  "fact": "A cat's rough tongue is covered with tiny barbs called papillae."
}
```

### **Error Handling / Fallback**

The endpoint is designed to be resilient. If the external Cat Facts API (`https://catfact.ninja/fact`) is unreachable, times out (after **5.0 seconds**), or returns an error status:

  * The endpoint will still return a **`200 OK`** status.
  * The `fact` field will contain the fallback message:
    `"fact": "Could not fetch a cat fact at the moment."`

-----

## 🔑 Key Implementation Notes

  * **Dynamic Timestamp:** Uses `datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")` to ensure the correct ISO 8601 UTC format.
  * **Client Management (Best Practice):** The asynchronous `httpx.AsyncClient` is initialized and closed using FastAPI's modern **`lifespan`** event handler, ensuring proper resource cleanup.
  * **Logging:** Basic logging is configured to track successful fact fetches and report specific network/timeout errors, aiding in debugging.