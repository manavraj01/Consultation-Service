# Telemed

## Setup Instructions
1. **Follow these steps to run the application. Make sure you have Docker, Docker Compose, and Git installed.**

2. **Clone the repository and navigate to the project folder**

```bash
git clone <repo-url>
cd <repo-folder>
```

# Build and Start the Application
**Notes:**  
- This will install all dependencies for both frontend and backend.  
- Backend server will run on port 8000.  
- Frontend server will run on port 3000.  
- Sample data will be automatically seeded into the backend database.  

```bash
docker-compose build
docker-compose up
```

# API Documentation

## Roles API

### Get All Roles

**Endpoint:** 127.0.0.1:8000/roles/all/

**Description:**  
Fetch all roles available in the system.

**Request:**  
No body is required for this GET request.

**Response:**  
Returns a paginated list of roles with their `id` and `title`.

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "title": "Nurse"
        },
        {
            "id": 2,
            "title": "Patient"
        },
        {
            "id": 1,
            "title": "Doctor"
        }
    ]
}
```

| Field         | Type    | Description                          |
| ------------- | ------- | ------------------------------------ |
| count         | integer | Total number of roles                |
| next          | string  | URL for next page (null if none)     |
| previous      | string  | URL for previous page (null if none) |
| results       | array   | List of role objects                 |
| results.id    | integer | Role ID                              |
| results.title | string  | Role title (Doctor, Patient, Nurse)  |

### Create Role

**Endpoint:** 127.0.0.1:8000/roles/all/

**Description:**  
Create a new role in the system.

**Request:**  
```json
{
   "title":"Nurse"   
}
```

**Response:**  
```json
{
    "id": 3,
    "title": "Nurse",
    "date_created": "2025-10-24T08:35:56.342665Z",
    "date_modified": "2025-10-24T08:35:56.343071Z",
    "archive": false
}
```

| Field          | Type    | Description                          |
| -------------- | ------- | ------------------------------------ |
| id             | integer | Role ID                               |
| title          | string  | Role title                            |
| date_created   | string  | Timestamp when role was created       |
| date_modified  | string  | Timestamp of last modification        |
| archive        | boolean | Indicates if the role is archived     |

### Role Detail API

#### Retrieve, Update, or Delete a Role

**Endpoint:** 127.0.0.1:8000/roles/3/

**Description:**  
Retrieve, update, or delete a specific role by its ID.  
- **GET**: Fetch the role details.  
- **PUT**: Update the role details. Provide `title` in the request body.  
- **DELETE**: Archive (delete) the role.  

**Request (PUT example):**  
```json
{
    "title": "Admin"
}
```

**Response (example GET/PUT):**  
```json
{
    "id": 3,
    "title": "Admin",
    "date_created": "2025-10-24T08:35:56.342665Z",
    "date_modified": "2025-10-24T09:42:16.438543Z",
    "archive": false
}
```

| Field          | Type    | Description                          |
| -------------- | ------- | ------------------------------------ |
| id             | integer | Role ID                               |
| title          | string  | Role title (e.g., Admin, Doctor)     |
| date_created   | string  | Timestamp when role was created       |
| date_modified  | string  | Timestamp of last modification        |
| archive        | boolean | Indicates if the role is archived     |

## Consultations API

### Get All Consultations

**Endpoint:** 127.0.0.1:8000/consultations/all/

**Description:**  
Fetch all consultations available in the system.

**Request:**  
No body is required for this GET request.

**Response:**  
Returns a paginated list of consultations with their details.

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "patient": 5,
            "patient_username": "Priya Sharma",
            "doctor": 2,
            "doctor_username": "Dr. Ekta",
            "date_created": "2024-10-16T14:30:00Z",
            "date_modified": "2024-10-16T14:30:00Z",
            "archive": false
        },
        {
            "id": 1,
            "patient": 4,
            "patient_username": "Seamus Moore",
            "doctor": 2,
            "doctor_username": "Dr. Ekta",
            "date_created": "2024-10-15T10:00:00Z",
            "date_modified": "2024-10-15T10:00:00Z",
            "archive": false
        }
    ]
}
```

| Field              | Type    | Description                          |
| -----------------  | ------- | ------------------------------------ |
| count              | integer | Total number of consultations       |
| next               | string  | URL for next page (null if none)    |
| previous           | string  | URL for previous page (null if none)|
| results            | array   | List of consultation objects        |
| results.id         | integer | Consultation ID                      |
| results.patient    | integer | Patient ID                           |
| results.patient_username | string | Patient name                    |
| results.doctor     | integer | Doctor ID                            |
| results.doctor_username | string | Doctor name                       |
| results.date_created | string | Timestamp of creation                |
| results.date_modified | string | Timestamp of last modification      |
| results.archive    | boolean | Indicates if the consultation is archived |

### Create Consultation

**Endpoint:** 127.0.0.1:8000/consultations/

**Description:**  
Create a new consultation by assigning a patient and a doctor.

**Request:**  
```json
{
    "patient": 4,
    "doctor": 1
}
```

**Response:**  
```json
{
    "id": 3,
    "patient_username": "Seamus Moore",
    "doctor_username": "Admin",
    "date_created": "2025-10-24T09:47:28.932901Z",
    "date_modified": "2025-10-24T09:47:28.932901Z",
    "archive": false,
    "patient": 4,
    "doctor": 1
}
```

| Field                  | Type    | Description                          |
| ---------------------- | ------- | ------------------------------------ |
| id                     | integer | Consultation ID                      |
| patient_username       | string  | Patient name                         |
| doctor_username        | string  | Doctor name                          |
| date_created           | string  | Timestamp of creation                |
| date_modified          | string  | Timestamp of last modification       |
| archive                | boolean | Indicates if the consultation is archived |
| patient                | integer | Patient ID                           |
| doctor                 | integer | Doctor ID                            |

### Update Consultation

**Endpoint:** 127.0.0.1:8000/consultations/id/

**Description:**  
Update a consultation’s patient or doctor using PATCH.

**Request (example):**  
```json
{
    "doctor": 3,
    "patient": 1
}
```

**Response:**  
```json
{
    "id": 2,
    "patient_username": "Admin",
    "doctor_username": "Dr. Seamus",
    "date_created": "2024-10-16T14:30:00Z",
    "date_modified": "2025-10-24T09:50:29.206587Z",
    "archive": false,
    "patient": 1,
    "doctor": 3
}
```

| Field                  | Type    | Description                          |
| ---------------------- | ------- | ------------------------------------ |
| id                     | integer | Consultation ID                      |
| patient_username       | string  | Patient name                         |
| doctor_username        | string  | Doctor name                          |
| date_created           | string  | Timestamp of creation                |
| date_modified          | string  | Timestamp of last modification       |
| archive                | boolean | Indicates if the consultation is archived |
| patient                | integer | Patient ID                           |
| doctor                 | integer | Doctor ID                            |


## Consultation Messages API

### Get All Messages

**Endpoint:** 127.0.0.1:8000/consultation-messages/all/

**Description:**  
Fetch all messages for consultations. You can filter messages using query parameters:  
- `consultation`: ID of the consultation  
- `role`: Role ID of the author (Doctor, Patient, etc.)

**Request:**  
No body is required for this GET request.  
Example query parameters: `?consultation=2&role=1`

**Response:**  
Returns a paginated list of consultation messages.

```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "consultation": 1,
            "author": 4,
            "author_username": "Seamus Moore",
            "author_role": 2,
            "author_role_title": "Patient",
            "content": "Hello Dr. Ekta, I have been experiencing headaches every afternoon.",
            "date_created": "2024-10-15T10:05:00Z"
        },
        {
            "id": 2,
            "consultation": 1,
            "author": 2,
            "author_username": "Dr. Ekta",
            "author_role": 1,
            "author_role_title": "Doctor",
            "content": "Hi Seamus, are the headaches sharp or dull? How often do they occur?",
            "date_created": "2024-10-15T10:08:00Z"
        },
        {
            "id": 3,
            "consultation": 1,
            "author": 4,
            "author_username": "Seamus Moore",
            "author_role": 2,
            "author_role_title": "Patient",
            "content": "Mostly dull, sometimes throbbing when working on the computer.",
            "date_created": "2024-10-15T10:10:00Z"
        },
        {
            "id": 4,
            "consultation": 2,
            "author": 5,
            "author_username": "Priya Sharma",
            "author_role": 2,
            "author_role_title": "Patient",
            "content": "Hello Dr. Ekta, I have trouble sleeping at night and wake up often.",
            "date_created": "2024-10-16T14:35:00Z"
        },
        {
            "id": 5,
            "consultation": 2,
            "author": 2,
            "author_username": "Dr. Ekta",
            "author_role": 1,
            "author_role_title": "Doctor",
            "content": "Hi Priya, try reducing caffeine after 2 PM and follow a calming bedtime routine.",
            "date_created": "2024-10-16T14:43:00Z"
        },
        {
            "id": 6,
            "consultation": 2,
            "author": 5,
            "author_username": "Priya Sharma",
            "author_role": 2,
            "author_role_title": "Patient",
            "content": "Thanks Dr. Ekta, I will follow your advice and update you next week.",
            "date_created": "2024-10-16T14:45:00Z"
        },
        {
            "id": 7,
            "consultation": 2,
            "author": 1,
            "author_username": "Admin",
            "author_role": 2,
            "author_role_title": "Patient",
            "content": "OK",
            "date_created": "2025-10-24T08:23:27.656002Z"
        },
        {
            "id": 8,
            "consultation": 2,
            "author": 5,
            "author_username": "Priya Sharma",
            "author_role": 2,
            "author_role_title": "Patient",
            "content": "OK",
            "date_created": "2025-10-24T08:33:20.263763Z"
        }
    ]
}
```

| Field               | Type    | Description                          |
| ------------------  | ------- | ------------------------------------ |
| count               | integer | Total number of messages            |
| next                | string  | URL for next page (null if none)    |
| previous            | string  | URL for previous page (null if none)|
| results             | array   | List of message objects              |
| results.id          | integer | Message ID                           |
| results.consultation| integer | Consultation ID                      |
| results.author      | integer | Author ID                            |
| results.author_username | string | Author name                        |
| results.author_role | integer | Role ID of author                    |
| results.author_role_title | string | Role title of author             |
| results.content     | string  | Message content                      |
| results.date_created | string | Timestamp of message creation       |

### Create Message

**Endpoint:** 127.0.0.1:8000/consultation-messages/

**Description:**  
Create a new message for a consultation.

**Request:**  
```json
{
    "author": 5,
    "consultation": 2,
    "author_role": 1,
    "content": "OK"
}
```

**Response:**  
```json
{
    "id": 9,
    "consultation": 2,
    "author": 1,
    "author_username": "Admin",
    "author_role": 2,
    "author_role_title": "Patient",
    "content": "OK",
    "date_created": "2025-10-24T09:53:11.908486Z",
    "last_modified": "2025-10-24T09:53:11.908486Z",
    "archive": false
}
```

| Field                  | Type    | Description                          |
| ---------------------- | ------- | ------------------------------------ |
| id                     | integer | Message ID                           |
| consultation           | integer | Consultation ID                      |
| author                  | integer | Author ID                            |
| author_username        | string  | Author name                          |
| author_role            | integer | Role ID of author                    |
| author_role_title      | string  | Role title of author                 |
| content                | string  | Message content                      |
| date_created           | string  | Timestamp of message creation        |
| last_modified          | string  | Timestamp of last modification       |
| archive                | boolean | Indicates if the message is archived |


#### **Architecture Decisions**

The backend of TELEMED is designed to be simple, modular, and easy to maintain while supporting the core telemedicine functionality. Key decisions include:

1. **Database Design**  
   - **Roles Table:** Stores role information (`Doctor`, `Patient`, `Admin`, etc.). This allows for role-based access and filtering of messages and consultations.  
   - **Consultations Table:** Stores consultations between patients and doctors. Each consultation references the `patient` and `doctor` (foreign keys from the `User` table).  
   - **Messages Table:** Stores messages sent within a consultation. Each message references the `consultation` and `author` (from the `User` table), along with the `author_role` to allow filtering by role.  
   - **User Table:** The existing `User` table is leveraged to store user details like name and unique IDs. Other tables reference this for relational integrity.  

2. **Relationships**  
   - One **User** can have multiple **Roles**, but each action (message, consultation) references a single role at the time of the operation.  
   - One **Consultation** links exactly one **patient** and one **doctor**, but each consultation can have multiple messages.  
   - Messages are always tied to a **consultation**, allowing easy retrieval of conversation history per consultation.  

3. **API Design**  
   - Endpoints are RESTful, with standard HTTP methods:
     - **GET** for retrieving data (all roles, all consultations, messages with optional filters).  
     - **POST** for creating new entries (roles, consultations, messages).  
     - **PUT/PATCH** for updating entries (roles, consultations).  
     - **DELETE** for soft-deleting or archiving data.  
   - Pagination is implemented for list endpoints to ensure scalability.  
   - Query parameters allow filtering messages by consultation ID and author role, improving performance for specific queries.  

4. **Data Integrity & Consistency**  
   - Foreign key relationships enforce consistency between users, roles, consultations, and messages.  
   - Soft-delete (`archive` boolean field) is used instead of hard deletes to preserve historical data.  
   - Timestamps (`date_created`, `date_modified`, `last_modified`) are maintained for auditing and version tracking.  

5. **Scalability Considerations**  
   - Modular design allows adding new roles or extending consultation types without schema changes.  
   - Indexing on foreign keys (user, consultation, role) ensures fast queries for message history and consultation lookups.  
   - API structure and filtering are designed to support large datasets and multiple concurrent users efficiently.  

This architecture ensures a **clean separation of concerns**, **scalable data structure**, and **easy maintainability**, while meeting the requirements for real-time telemedicine interactions between doctors and patients.


#### **Data Model**

The TELEMED backend is structured around three main tables (`Roles`, `Consultations`, `Messages`) along with the existing `User` table. The relationships and fields were designed to ensure data integrity, support real-time interactions, and make querying efficient.

1. **Roles Table**  
   - **Fields:**  
     - `id` (integer, primary key) – unique identifier for the role  
     - `title` (string) – role name (e.g., Doctor, Patient, Admin)  
     - `date_created` / `date_modified` – timestamps for auditing  
     - `archive` (boolean) – soft-delete flag  
   - **Purpose:** Stores user roles to enable role-based filtering, permissions, and message/consultation filtering.

2. **Consultations Table**  
   - **Fields:**  
     - `id` (integer, primary key) – unique consultation ID  
     - `patient` (foreign key → User) – identifies the patient in the consultation  
     - `doctor` (foreign key → User) – identifies the doctor  
     - `date_created` / `date_modified` – timestamps for auditing  
     - `archive` (boolean) – soft-delete flag  
   - **Purpose:** Tracks interactions between a patient and a doctor. Supports linking multiple messages to a single consultation.  

3. **Messages Table**  
   - **Fields:**  
     - `id` (integer, primary key) – unique message ID  
     - `consultation` (foreign key → Consultations) – links the message to a specific consultation  
     - `author` (foreign key → User) – user who sent the message  
     - `author_role` (foreign key → Roles) – role of the author at the time of sending  
     - `content` (string/text) – message text  
     - `date_created` / `last_modified` – timestamps for auditing and editing  
     - `archive` (boolean) – soft-delete flag  
   - **Purpose:** Stores all messages sent during a consultation. Supports filtering by consultation and author role.

4. **Relationship Between Consultations and Messages**  
   - One **Consultation** can have multiple **Messages** (1-to-many).  
   - Each **Message** belongs to exactly one **Consultation** and has one **Author** with a specific role.  
   - This design allows retrieval of all messages for a consultation efficiently, with optional filtering by author role.

5. **Indexes for a Real Database**  
   To ensure fast queries and scalability:  
   - **Messages Table:**  
     - Index on `consultation` – for fetching all messages in a consultation quickly  
     - Index on `author_role` – for filtering messages by role  
     - Index on `date_created` – for sorting messages chronologically  
   - **Consultations Table:**  
     - Index on `patient` and `doctor` – for fast lookups of consultations per user  
   - **Roles Table:**  
     - Index on `title` – for fast role-based queries  
   - Foreign key constraints inherently enforce referential integrity across all tables.

This data model balances **simplicity, query efficiency, and maintainability**, while supporting the core features of TELEMED: role-based messaging, consultations, and auditing.

#### **Technology Choices**

The TELEMED backend was built using Django REST Framework with **SQLite** as the storage database. The choices were guided by scalability, maintainability, and rapid development needs.

1. **Language and Framework**  
   - **Python + Django REST Framework (DRF)**  
     - DRF provides a clean, modular way to build RESTful APIs.  
     - Python allows rapid development and easy integration with data manipulation and filtering.  
     - Django’s ORM simplifies database operations, relationships, and migrations.  
   - **Trade-offs:**  
     - DRF may add some overhead compared to lightweight frameworks like Flask, but it accelerates development for complex relational models.

2. **Storage Approach**  
   - **SQLite**  
     - Chosen for development simplicity and zero-configuration setup.  
     - Relational structure fits the relationships between Users, Roles, Consultations, and Messages.  
     - Foreign key constraints enforce data integrity and support complex queries.  
   - **Trade-offs:**  
     - SQLite is not ideal for heavy concurrent write operations or very large datasets.  
     - For production, a switch to PostgreSQL or MySQL would be recommended for scalability.

3. **Other Choices**  
   - **Docker + Docker Compose** for environment consistency and easy deployment.  
   - **Soft-delete (`archive` field)** instead of hard delete to maintain historical data.  
   - **Pagination and filtering** for scalability on list endpoints.  

4. **Trade-offs Given Time Constraints**  
   - Focused on building a functional, maintainable backend rather than implementing full real-time messaging (WebSockets).  
   - Chose simplicity in database schema to prioritize correct relationships and API functionality.  
   - Deferred advanced optimizations (like caching or message queues) for future iterations.

This technology stack allows rapid development, ensures maintainable code, and supports the core functionality of TELEMED while keeping the system flexible for future enhancements.

### **3. Making This Production-Ready**

Before deploying TELEMED to a real production environment, several enhancements would be necessary to ensure **security, performance, reliability, scalability, and compliance**.

---

#### **Security**
- **Switch from SQLite to PostgreSQL** for production-grade data handling and user isolation.  
- **Implement authentication & authorization** using JWT or DRF’s token-based auth to secure API endpoints.  
- **Use HTTPS** for all communications to protect patient-doctor messages and consultation data.  
- **Enforce role-based access control (RBAC)** — ensure only doctors can initiate consultations and only participants can send messages.  
- **Add rate limiting & throttling** to prevent abuse or DDoS attacks.  
- **Store secrets securely** using environment variables or a secret manager (e.g., AWS Secrets Manager, Vault).  

---

#### **Performance**
- **Optimize database queries** using Django’s `select_related` / `prefetch_related` for related objects.  
- **Add caching** (Redis or Memcached) for frequently accessed endpoints like roles or consultations.  
- **Implement pagination everywhere** to handle large datasets efficiently.  
- **Enable GZIP compression** for API responses to reduce bandwidth usage.  

---

#### **Reliability**
- **Use PostgreSQL with automatic backups** and point-in-time recovery.  
- **Add health-check endpoints** for monitoring container and service health.  
- **Implement logging & monitoring** using tools like Sentry, ELK Stack, or Prometheus + Grafana.  
- **Dockerize with versioned builds** to ensure consistent deployments across environments.  

---

#### **Scalability**
- **Migrate from SQLite to PostgreSQL or MySQL** for handling concurrent reads/writes at scale.  
- **Use Gunicorn or uWSGI with Nginx** to serve the Django app efficiently.  
- **Implement horizontal scaling** with load balancing if deployed on cloud (AWS, GCP, Azure).  
- **Decouple message sending** via Celery and Redis queues if real-time or high message volume is expected.  

---

#### **Data Integrity**
- **Use database constraints and transactions** to maintain consistency between Users, Consultations, and Messages.  
- **Add audit logging** for changes to roles, consultations, and messages.  
- **Implement soft-delete consistently** (using the `archive` flag) to preserve historical data safely.  
- **Regularly validate foreign key references** to avoid orphaned records.  

---

#### **Compliance**
- **Ensure GDPR/HIPAA compliance** for sensitive health data:
  - Encrypt all personally identifiable information (PII) and medical data at rest and in transit.  
  - Allow users to delete or export their data upon request.  
  - Maintain detailed access logs for audit purposes.  
- **Conduct security and penetration testing** before go-live.  

---

These improvements would transform the TELEMED prototype into a **secure, stable, and production-ready telemedicine platform**, capable of handling real-world workloads and sensitive medical data responsibly.
