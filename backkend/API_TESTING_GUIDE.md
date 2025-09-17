# API Testing Guide - Postman Payloads

## Base URL
```
http://localhost:8000
```

## 🔐 Authentication Endpoints

### 1. User Signup
**Method:** `POST`
**URL:** `{{base_url}}/api/auth/signup`
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "email": "john.doe@university.edu",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Expected Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "64f8b1234567890abcdef123",
    "email": "john.doe@university.edu",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2025-09-18T10:30:00.000Z",
    "last_login": "2025-09-18T10:30:00.000Z"
  }
}
```

---

### 2. User Login
**Method:** `POST`
**URL:** `{{base_url}}/api/auth/login`
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "email": "john.doe@university.edu",
  "password": "securepassword123"
}
```

**Expected Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "64f8b1234567890abcdef123",
    "email": "john.doe@university.edu",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2025-09-18T10:30:00.000Z",
    "last_login": "2025-09-18T10:35:00.000Z"
  }
}
```

---

### 3. Get Current User Profile
**Method:** `GET`
**URL:** `{{base_url}}/api/auth/me`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body:** None

**Expected Response (200):**
```json
{
  "id": "64f8b1234567890abcdef123",
  "email": "john.doe@university.edu",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-09-18T10:30:00.000Z",
  "last_login": "2025-09-18T10:35:00.000Z"
}
```

---

### 4. Update User Profile
**Method:** `PUT`
**URL:** `{{base_url}}/api/auth/me`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "full_name": "John Smith",
  "email": "john.smith@university.edu"
}
```

**Expected Response (200):**
```json
{
  "id": "64f8b1234567890abcdef123",
  "email": "john.smith@university.edu",
  "full_name": "John Smith",
  "is_active": true,
  "created_at": "2025-09-18T10:30:00.000Z",
  "last_login": "2025-09-18T10:35:00.000Z"
}
```

---

### 5. Change Password
**Method:** `POST`
**URL:** `{{base_url}}/api/auth/change-password`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "current_password": "securepassword123",
  "new_password": "newsecurepassword456"
}
```

**Expected Response (200):**
```json
{
  "message": "Password updated successfully",
  "success": true
}
```

---

### 6. Logout
**Method:** `POST`
**URL:** `{{base_url}}/api/auth/logout`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body:** None

**Expected Response (200):**
```json
{
  "message": "Logged out successfully",
  "success": true
}
```

---

### 7. Get All Users (Admin)
**Method:** `GET`
**URL:** `{{base_url}}/api/auth/users?skip=0&limit=10`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body:** None

**Expected Response (200):**
```json
[
  {
    "id": "64f8b1234567890abcdef123",
    "email": "john.doe@university.edu",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2025-09-18T10:30:00.000Z",
    "last_login": "2025-09-18T10:35:00.000Z"
  },
  {
    "id": "64f8b1234567890abcdef124",
    "email": "jane.smith@university.edu",
    "full_name": "Jane Smith",
    "is_active": true,
    "created_at": "2025-09-18T11:00:00.000Z",
    "last_login": null
  }
]
```

---

## 🤖 RAG System Endpoints

### 8. Initialize Database with PDFs
**Method:** `POST`
**URL:** `{{base_url}}/api/rag/init-db`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "pdf_paths": [
    "/home/tashrif/Desktop/Study-Assistant/assets/lecture1.pdf",
    "/home/tashrif/Desktop/Study-Assistant/assets/lecture2.pdf",
    "/home/tashrif/Desktop/Study-Assistant/assets/programming_basics.pdf"
  ]
}
```

**Expected Response (201):**
```json
{
  "status": "success",
  "message": "ChromaDB initialized successfully with PDFs",
  "documents_processed": 3,
  "chunks_created": 156
}
```

---

### 9. Add PDFs to Existing Database
**Method:** `POST`
**URL:** `{{base_url}}/api/rag/add-pdf`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "pdf_paths": [
    "/home/tashrif/Desktop/Study-Assistant/assets/advanced_topics.pdf",
    "/home/tashrif/Desktop/Study-Assistant/assets/exam_preparation.pdf"
  ]
}
```

**Expected Response (200):**
```json
{
  "status": "success",
  "message": "PDFs added to existing ChromaDB successfully",
  "new_documents_added": 89,
  "total_documents": 245
}
```

---

### 10. Ask Question to RAG System
**Method:** `POST`
**URL:** `{{base_url}}/api/rag/ask`
**Headers:**
```json
{
  "Authorization": "Bearer {{jwt_token}}",
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "question": "What is object-oriented programming and how does inheritance work in Java?"
}
```

**Expected Response (200):**
```json
{
  "answer": "Object-oriented programming (OOP) is a programming paradigm that uses **objects** and **classes** to structure code. In Java, inheritance allows a class to inherit properties and methods from another class using the `extends` keyword.\n\n## Key Concepts:\n\n### Inheritance in Java:\n```java\npublic class Vehicle {\n    protected String brand;\n    \n    public void start() {\n        System.out.println(\"Vehicle starting...\");\n    }\n}\n\npublic class Car extends Vehicle {\n    private int doors;\n    \n    public void honk() {\n        System.out.println(\"Car honking!\");\n    }\n}\n```\n\n### Benefits:\n- **Code Reusability**: Child classes inherit parent methods\n- **Method Overriding**: Child classes can override parent methods\n- **Polymorphism**: Objects can be treated as instances of their parent class\n\nThis creates a hierarchical relationship where `Car` inherits all public and protected members from `Vehicle`.",
  "sources": [
    {
      "source": "java_programming_basics.pdf",
      "chunk_id": "chunk_45",
      "content_preview": "Object-oriented programming is a programming paradigm based on the concept of objects..."
    },
    {
      "source": "inheritance_tutorial.pdf",
      "chunk_id": "chunk_12",
      "content_preview": "In Java, inheritance is implemented using the extends keyword. This allows..."
    },
    {
      "source": "oop_concepts.pdf",
      "chunk_id": "chunk_78",
      "content_preview": "The main benefits of inheritance include code reusability, method overriding..."
    }
  ],
  "conversation_length": 1
}
```

---

## 🧪 Error Response Examples

### Authentication Error (401)
```json
{
  "detail": "Could not validate credentials"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters",
      "input": "123"
    }
  ]
}
```

### User Already Exists (400)
```json
{
  "detail": "Email already registered"
}
```

### Invalid Credentials (401)
```json
{
  "detail": "Incorrect email or password"
}
```

### No Database Found (400)
```json
{
  "detail": "No ChromaDB found. Use /init-db first to create knowledge base."
}
```

---

## 📝 Postman Environment Variables

Create these variables in Postman:

```json
{
  "base_url": "http://localhost:8000",
  "jwt_token": "{{access_token_from_login_response}}"
}
```

## 🔄 Testing Workflow

1. **Start Backend Server**
   ```bash
   cd /home/tashrif/Desktop/Study-Assistant/backkend
   source venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Test Authentication Flow:**
   - Signup new user → Copy `access_token`
   - Set `jwt_token` variable in Postman
   - Test protected endpoints

3. **Test RAG System:**
   - Initialize database with PDFs
   - Add more PDFs (optional)
   - Ask questions

4. **Test Error Cases:**
   - Invalid credentials
   - Missing authentication
   - Invalid PDF paths
   - Empty questions

## 🎯 Sample Test Users

```json
// User 1
{
  "email": "student1@university.edu",
  "password": "password123",
  "full_name": "Alice Johnson"
}

// User 2
{
  "email": "professor@university.edu", 
  "password": "securepass456",
  "full_name": "Dr. Robert Smith"
}

// User 3
{
  "email": "admin@university.edu",
  "password": "adminpass789",
  "full_name": "System Administrator"
}
```

## 🚀 Quick Start Commands

```bash
# 1. Start server
uvicorn main:app --reload

# 2. Test with curl (signup)
curl -X POST "http://localhost:8000/api/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123","full_name":"Test User"}'

# 3. Test with curl (login)
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123"}'
```

This comprehensive guide covers all endpoints with realistic payloads and expected responses! 🎯
