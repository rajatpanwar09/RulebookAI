# RulebookAI

RulebookAI is a rule-grounded university policy question-answering system.

Instead of behaving like a generic chatbot, RulebookAI retrieves relevant rules from a university rulebook corpus and uses those rules to construct grounded answers.

The system also displays the sources and rules used to generate an answer and identifies potential contradictions or exceptions between university regulations.

## Key Features

- Question answering over university regulations
- Rule-based retrieval from the university rulebook corpus
- Source citation for retrieved rules
- Relevance/similarity scores
- Displays the rules used to generate an answer
- Detects potential contradictions and exceptions
- Handles unknown questions without blindly inventing rules
- FastAPI backend
- Simple HTML frontend

## Architecture

```text
User Question
      |
      v
Frontend
      |
      v
FastAPI /ask Endpoint
      |
      v
Rule Retrieval
      |
      v
Relevant Rules
      |
      +----------> Answer Generation
      |
      +----------> Source Information
      |
      +----------> Rules Used
      |
      +----------> Contradiction Detection
      |
      v
Frontend Response
```

## How It Works

### 1. User Question

The user enters a question related to university policies, regulations, examinations, attendance, fees, hostel rules, student welfare, or other rulebook topics.

### 2. Frontend

The HTML frontend collects the user's question and sends it to the backend through the `/ask` API endpoint.

### 3. FastAPI Backend

The FastAPI backend receives the question and passes it to the question-answering system.

### 4. Rule Retrieval

The system searches the university rulebook corpus and retrieves rules that are relevant to the user's question.

### 5. Answer Generation

The retrieved rules are used to construct a grounded answer rather than relying on unsupported information.

### 6. Source Information

The response identifies the source document from which the relevant rules were retrieved.

### 7. Rules Used

The application displays the specific rules used to construct the answer along with their relevance scores.

### 8. Contradiction Detection

The system identifies potential contradictions, exceptions, or different requirements between relevant rules.

For example, one rule may require 75% attendance for examination eligibility while another officially approved medical exception may allow eligibility with attendance as low as 60%.

### 9. Unknown Questions

If the rulebook does not contain sufficient information to answer a question, the system avoids blindly inventing a university policy.

## Example

### Question

> What is the minimum attendance required for an examination?

### RulebookAI Response

The system can identify:

- Normal attendance requirement: **75%**
- Approved medical exception: **60%**

It also displays the relevant rules and identifies the attendance threshold exception as a potential contradiction or exception.

## Project Structure

```text
RulebookAI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── qa.py
│   ├── retrieval.py
│   └── static/
│
├── corpus/
│   ├── academic_regulations.md
│   ├── examination_policy.md
│   ├── fee_deadlines.csv
│   ├── financial_regulations.md
│   ├── financial_regulations.pdf
│   ├── hostel_handbook.md
│   └── student_welfare.md
│
├── frontend/
│   └── index.html
│
├── scripts/
│   └── create_finance_pdf.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Technologies Used

- **Python**
- **FastAPI**
- **Pydantic**
- **HTML**
- **CSS**
- **JavaScript**
- **Rule-based information retrieval**
- **University policy documents**

## API

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Ask a Question

```http
POST /ask
```

Request:

```json
{
  "question": "What is the minimum attendance required for an examination?"
}
```

The API returns the generated answer together with the relevant sources, retrieved rules, relevance scores, and detected contradictions when applicable.

## Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/rajatpanwar09/RulebookAI.git
cd RulebookAI
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start the Backend

From the project root:

```powershell
uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### 5. Start the Frontend

Open a second terminal and run:

```powershell
cd frontend
python -m http.server 5500
```

Open the application in your browser:

```text
http://127.0.0.1:5500
```

## API Documentation

Once the backend is running, FastAPI provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The `/docs` page can be used to test the API directly.

## Design Philosophy

RulebookAI is designed around the principle of **grounded answers**.

A university policy assistant should not simply generate a confident response. It should identify the rules supporting the response and make exceptions or conflicting clauses visible.

The core workflow is:

```text
Question
   ↓
Retrieve Rules
   ↓
Rank Relevant Rules
   ↓
Generate Grounded Answer
   ↓
Show Sources
   ↓
Show Rules Used
   ↓
Detect Exceptions / Contradictions
```

## Why RulebookAI?

University regulations can contain exceptions, amendments, and clauses that interact with one another.

A simple chatbot may provide an answer without showing where that answer came from.

RulebookAI focuses on:

- **Traceability** — showing the rules behind an answer
- **Grounding** — answering from the rulebook corpus
- **Transparency** — displaying sources and relevance scores
- **Exception Detection** — highlighting special cases
- **Contradiction Detection** — identifying potentially conflicting requirements
- **Reliability** — avoiding unsupported answers when information is unavailable

## Future Improvements

Possible future improvements include:

- More advanced semantic search
- Better ranking of retrieved rules
- Automatic cross-document contradiction analysis
- Authentication for university users
- Admin interface for updating regulations
- Database-backed rule management
- Version tracking for university policies
- Improved natural-language explanations
- Support for additional document formats

## Mocked / Simplified Components

This project is a working prototype. The university rulebook documents in the `corpus/` directory are used as the source of truth for retrieval.

The current system does not connect to a live university database or university authentication system. User authentication, live policy updates, and database-backed rule management are not implemented.

The answer generation and contradiction/exception detection are implemented using the project's rule retrieval and processing logic rather than an external production university system.

## Project Status

**Working prototype**

The current version demonstrates rule retrieval, grounded question answering, source display, rule transparency, and contradiction/exception detection through a FastAPI backend and HTML frontend.