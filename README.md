# Identity-Reconciliation
Bitespeed Backend Task: Identity Reconciliation 

## 🔍 Identity Reconciliation API

This FastAPI-based service resolves user identities based on email and phone number inputs by linking them to primary and secondary contacts.

🌐 **Live API**: [https://identity-reconciliation-n9a3.onrender.com](https://identity-reconciliation-n9a3.onrender.com)

---

## 📫 API Endpoint

### `POST /identify`

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
    "primaryContatctId": 1,
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

