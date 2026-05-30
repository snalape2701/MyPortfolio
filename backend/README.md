# Luxury Portfolio FastAPI Backend API

This is the high-performance Python backend server supporting contact submissions, payload validations, and persistence for Sahil Talape's luxury developer portfolio.

## 🚀 Standard Architecture

* **Framework**: FastAPI (Asynchronous API endpoints with automatic Swagger documentation)
* **Model Validation**: Pydantic v2 (Strictly validates email formatting, string lengths, and prevents malicious payloads)
* **Storage Strategy**: Local file persistence (`app/submissions.json`) for quick mock configurations.
* **Security Middleware**: Configured CORS middleware allowing visual frontends to interact seamlessly.

## 💻 Standalone Dev Start

If you choose to run this API separately without using the root `run.bat`:

1. **Activate virtual environment**:
   ```bash
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
2. **Execute Uvicorn**:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

## 📍 Endpoint References

| Method | Endpoint | Description | Payload Schema |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Root developer meta-information | None |
| **POST** | `/api/contact` | Deploys form submissions & saves data | `ContactSubmission` (name, email, message) |
| **GET** | `/api/submissions` | Developer debug utility (reads saved files) | None |

---
Designed with care by Antigravity AI.
