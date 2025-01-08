# Task Management API: Evidence of Functionality (Using Curl Commands)

This document provides evidence that the implemented API endpoints work correctly. All commands use **curl** to demonstrate authentication and task management functionality.

---

## **Step 1: Obtain JWT Tokens**

### **Endpoint**: `/api/token/`  
Send user credentials to obtain **access** and **refresh** tokens.

**Command:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
-H "Content-Type: application/json" \
-d "{\"username\":\"admin\", \"password\":\"Admin123!\"}"
```

**Response:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## **Step 2: Test Protected Endpoints**

### **2.1 GET Tasks (Empty Task List)**

**Endpoint**: `/api/tasks/`  
Requires the **access token**.

**Command:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer <your_access_token>"
```

**Response:**
```json
[]
```

---

### **2.2 POST Create a Task**

**Endpoint**: `/api/tasks/`  
Create a new task using the **access token**.

**Command:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer <your_access_token>" \
-H "Content-Type: application/json" \
-d "{\"title\":\"New Task\", \"description\":\"Testing task creation\", \"due_date\":\"2024-12-31\", \"priority\":\"High\"}"
```

**Response:**
```json
{
    "id": 1,
    "title": "New Task",
    "description": "Testing task creation",
    "due_date": "2024-12-31",
    "priority": "High",
    "status": false
}
```

---

### **2.3 GET Tasks (After Creating a Task)**

**Endpoint**: `/api/tasks/`  
Verify the task was successfully created.

**Command:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer <your_access_token>"
```

**Response:**
```json
[
    {
        "id": 1,
        "title": "New Task",
        "description": "Testing task creation",
        "due_date": "2024-12-31",
        "priority": "High",
        "status": false
    }
]
```

---

### **2.4 Refresh the Access Token**

**Endpoint**: `/api/token/refresh/`  
Refresh the access token using the **refresh token**.

**Command:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
-H "Content-Type: application/json" \
-d "{\"refresh\":\"<your_refresh_token>\"}"
```

**Response:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## **Summary of Functionality**

1. **Token-Based Authentication**:
   - Access and refresh tokens are generated using user credentials.
   - Access tokens are required for all protected endpoints.

2. **Task Management**:
   - Tasks can be created, listed, and managed using authenticated requests.

3. **Access Token Refresh**:
   - Expired access tokens can be refreshed using the refresh token.