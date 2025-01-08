# Task Management API: Authentication Setup

This document explains the authentication setup for the Task Management API using **JWT (JSON Web Token)**.

## **Authentication Overview**

The API uses **token-based authentication** provided by the Django REST Framework (DRF) and Simple JWT. Users authenticate with their credentials to receive an **access token** and **refresh token**.

- **Access Token**: Short-lived token for API requests.
- **Refresh Token**: Long-lived token used to get a new access token.

---

## **How to Obtain Tokens**

### **1. Obtain Access and Refresh Tokens**
Send a POST request to the `/api/token/` endpoint with your credentials:

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
-H "Content-Type: application/json" \
-d "{\"username\":\"<your_username>\", \"password\":\"<your_password>\"}"
```

**Response:**
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```

---

## **How to Use the Access Token**

Include the **access token** in the `Authorization` header for all protected endpoints:

```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer <your_access_token>"
```

---

## **Refreshing the Access Token**

When the access token expires, use the **refresh token** to get a new access token.

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
-H "Content-Type: application/json" \
-d "{\"refresh\":\"<your_refresh_token>\"}"
```

**Response:**
```json
{
    "access": "<new_access_token>"
}
```

---

## **Testing Authentication**

1. Run the server:
   ```bash
   python manage.py runserver
   ```

2. Use the following endpoints:
   - **Login/Obtain Token**: `/api/token/`
   - **Refresh Token**: `/api/token/refresh/`
   - **Protected Endpoint (Tasks)**: `/api/tasks/`

3. Test using tools like **Postman** or `curl` commands.

---

## **Code Reference**

- Authentication implemented using **Django REST Framework** and **Simple JWT**.
- DRF configuration can be found in `settings.py` under `REST_FRAMEWORK` and `SIMPLE_JWT`.

---