# Identity-Reconciliation
Bitespeed Backend Task: Identity Reconciliation 

## 🔍 Identity Reconciliation API

This FastAPI-based service resolves user identities based on email and phone number inputs by linking them to primary and secondary contacts.

## 🌐 Live Endpoint

The API is hosted on Render and available at:

📍 **POST** [`/identify`](https://identity-reconciliation-n9a3.onrender.com/identify)  
Base URL: `https://identity-reconciliation-n9a3.onrender.com`

---

## 📫 API Endpoint

### `POST /identify`
This endpoint accepts only HTTP POST requests with Content-Type: application/json

<pre lang="markdown"> ```bash curl -X POST https://identity-reconciliation-n9a3.onrender.com/identify \ -H "Content-Type: application/json" \ -d "{\"email\": \"john@example.com\", \"phoneNumber\": \"1234567890\"}" ``` </pre>


Identifies and reconciles contact info.

#### Request Body

```json
{
  "email": "john@example.com",
  "phoneNumber": "1234567890"
}
````

#### Sample Response

```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["john@example.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": [2, 3]
  }
}
```

---

## 🛠 Tech Stack

* Python 3.10
* FastAPI
* MySQL
* Hosted on Render

---

## 📊 Database Schema

Schema of the `Contact` table used to maintain identity resolution:

```
+----------------+-----------------------------+------+-----+-------------------+-----------------------------------------------+
| Field          | Type                        | Null | Key | Default           | Extra                                         |
+----------------+-----------------------------+------+-----+-------------------+-----------------------------------------------+
| id             | int                         | NO   | PRI | NULL              | auto_increment                                |
| phoneNumber    | varchar(20)                 | YES  |     | NULL              |                                               |
| email          | varchar(255)                | YES  |     | NULL              |                                               |
| linkedId       | int                         | YES  | MUL | NULL              |                                               |
| linkPrecedence | enum('primary','secondary') | NO   |     | NULL              |                                               |
| createdAt      | datetime                    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updatedAt      | datetime                    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
| deletedAt      | datetime                    | YES  |     | NULL              |                                               |
+----------------+-----------------------------+------+-----+-------------------+-----------------------------------------------+
```

## ✅ Submission Checklist

- [x] POST `/identify` implemented
- [x] Accepts JSON body
- [x] Hosted on Render
- [x] API link in README
- [x] Clean commit history
