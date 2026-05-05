# JWT Decoder API 🚀

A simple Flask API to decode JWT tokens.  
Powered by **XEROX_MOD** | TG: [@SEXTYMOD](https://t.me/SEXTYMODS)

---

## Features

- Decode JWT Header, Payload, and Signature
- Simple GET request API
- Works instantly on Vercel deployment

---

## API Endpoint
```json
GET /decode?jwt=<your_jwt_token>
```

**Parameters:**

| Parameter | Type   | Description          |
|-----------|--------|--------------------|
| jwt       | string | JWT token to decode |

**Response:**

Success:

```json
{
  "status": "success",
  "header": { /* decoded JWT header */ },
  "payload": { /* decoded JWT payload */ },
  "signature": "..." 
}
```
If JWT is missing or invalid:
```Json

{
  "status": "error",
  "message": "JWT token missing or invalid"
}
```
Installation (Local)
Bash
Copy code
git clone <repo_url>
cd <repo_folder>
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
python app.py
Visit http://127.0.0.1:5000/decode?jwt=<your_jwt> in your browser or Postman.
Deployment on Vercel
Install Vercel CLI:
Bash
Copy code
npm i -g vercel
Deploy:
Bash
Copy code
vercel
Your API will be live.
Example: https://your-project.vercel.app/decode?jwt=<token>
Credits
API by XEROX_MOD
Telegram: @SEXTYMODS⁠�
