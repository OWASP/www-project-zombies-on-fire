# OWASP Zombies on Fire - Tabletop Exercise Portal

An AI-powered platform for creating and managing tabletop cybersecurity exercises.

## Features

### 1. Administrator Authentication
- Secure login system with JWT tokens
- User registration and management
- Role-based access control

### 2. Tabletop Exercise Creation
- Guided 4-question creation flow
- Story-based scenario building
- Progress tracking

### 3. Four-Question Framework
Each tabletop exercise is built through four key questions:

1. **Overview** - The game's scenario, setting, and narrative context
2. **Challenges** - Issues and problems players must solve
3. **Twists** - Unexpected events and information thrown at players
4. **Conclusion** - Expected resolution and learning outcomes

### 4. AI-Powered Document Generation
Each document type has its own specialized agent:

| Document Type | Agent Purpose |
|--------------|---------------|
| Scenario Brief | Creates the main scenario narrative |
| Facilitator Guide | Instructions for exercise leaders |
| Participant Handbook | Materials for players |
| Inject Cards | Unexpected events/twists cards |
| Assessment Rubric | Evaluation criteria |
| After Action Template | Post-exercise review format |

### 5. PDF Export
All generated documents can be exported as professional PDF files.

## Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the application:
```bash
python run.py
```

6. Open http://localhost:8000 in your browser

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key | Required |
| `DATABASE_URL` | Database connection URL | `sqlite:///./tabletop.db` |
| `LLM_PROVIDER` | AI provider (openai, anthropic, mock) | `mock` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `LLM_MODEL` | Model to use | `gpt-4` |

### LLM Providers

The portal supports multiple LLM providers:

- **OpenAI** (`LLM_PROVIDER=openai`): Uses GPT-4 or other OpenAI models
- **Anthropic** (`LLM_PROVIDER=anthropic`): Uses Claude models
- **Mock** (`LLM_PROVIDER=mock`): For testing without API calls

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Key Endpoints

```
POST /api/auth/register     - Register new admin
POST /api/auth/login        - Login and get token
GET  /api/auth/me           - Get current user

POST /api/tabletops/        - Create tabletop
GET  /api/tabletops/        - List tabletops
GET  /api/tabletops/{id}    - Get tabletop details
PUT  /api/tabletops/{id}/questions/{type}  - Answer question

POST /api/documents/tabletop/{id}/generate  - Generate documents
GET  /api/documents/{id}/download           - Download PDF
```

## Project Structure

```
portal/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── security.py          # Authentication utilities
│   ├── api/                  # API routes
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── tabletops.py
│   │   └── documents.py
│   ├── models/               # Database models
│   │   ├── user.py
│   │   ├── tabletop.py
│   │   └── document.py
│   ├── schemas/              # Pydantic schemas
│   ├── agents/               # Document generation agents
│   │   ├── base.py
│   │   ├── scenario_brief.py
│   │   ├── facilitator_guide.py
│   │   └── ...
│   ├── services/             # Business logic
│   │   ├── llm_service.py
│   │   ├── pdf_service.py
│   │   └── document_service.py
│   └── frontend/             # Web interface
│       └── templates/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Example Scenarios

### Healthcare Crisis
> A hospital operating without a steam plant faces a critical power shortage.
> Players must manage resources and make decisions as backup batteries deplete.

### Infrastructure Failure
> A region's critical infrastructure begins failing. Players must coordinate
> response efforts and manage cascading effects across systems.

### Cyber Attack Response
> An organization detects a sophisticated intrusion. Players must contain
> the threat while maintaining business operations.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Security

For security issues, see [SECURITY.md](../SECURITY.md).

## License

This project is part of OWASP and follows OWASP licensing.

## Project Leaders

- Nathan Case (nathan.case@owasp.org)
- Jon McCoy (jon.mccoy@owasp.org)
