# Luxury Portfolio FastAPI Backend API

This is the high-performance Python backend server supporting contact submissions, email delivery, payload validations, and persistence for Sahil Talape's luxury developer portfolio.

## 🚀 Standard Architecture

* **Framework**: FastAPI (Asynchronous API endpoints with automatic Swagger documentation)
* **Model Validation**: Pydantic v2 (Strictly validates email formatting, string lengths, and prevents malicious payloads)
* **Email Delivery**: Resend API for sending contact form submissions directly to your inbox
* **Backup Storage**: Local file persistence (`app/submissions.json`) as a fallback log for all submissions
* **Security Middleware**: Configured CORS middleware allowing visual frontends to interact seamlessly.

## 💻 Standalone Dev Start

If you choose to run this API separately without using the root `run.bat`:

1. **Set up your `.env`** with your Resend API key:
   ```
   RESEND_API_KEY=re_your_actual_api_key
   CONTACT_TO_EMAIL=sahiltalape2701@gmail.com
   CONTACT_FROM_EMAIL=sahiltalape01@gmail.com
   ```
2. **Activate virtual environment**:
   ```bash
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. **Execute Uvicorn**:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

## 📍 Endpoint References
| Method | Endpoint | Description | Payload Schema |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Root developer meta-information & email service status | None |
| **GET** | `/api/projects` | Returns portfolio project listings | None |
| **GET** | `/api/experiences` | Returns work experience entries | None |
| **POST** | `/api/contact` | Sends email via Resend & saves submission locally | `ContactSubmission` (name, email, message) |
| **GET** | `/api/submissions` | Developer debug utility (reads saved files) | None |

---
Designed with care by Antigravity AI.
