# OWASP Zombies on Fire

An open-source, AI-powered framework for generating advanced cybersecurity tabletop exercises.

## Overview

This OWASP project provides an AI-assisted framework for generating advanced tabletop cybersecurity exercises. These exercises enhance organizational readiness through dynamic, threat-realistic scenarios that align with OWASP's mission to improve the security of software and systems.

The project addresses the lack of accessible, scalable, and high-fidelity tabletop exercises. Traditional tabletops often fall short—limited in scope, unrealistic, or resource-intensive to develop. By using AI to assist in the creation and customization of exercises, this project democratizes access to world-class training tools.

## Tabletop Exercise Portal

The portal is an AI-powered web application for creating and managing tabletop exercises. It features a guided 4-question creation flow, multiple LLM provider support (OpenAI, Anthropic), and professional PDF document generation.

### Platform Support

| Platform | Status | Installation |
|----------|--------|--------------|
| macOS | Supported | `./scripts/install-mac.sh` |
| Ubuntu/Debian | Supported | `./scripts/install-ubuntu.sh` |
| Windows | Supported | `scripts\install-windows.ps1` |
| Docker | Supported | `docker-compose up -d` |

**Requirements:** Python 3.11+, 2GB RAM minimum

### Quick Start

**macOS:**
```bash
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal && chmod +x scripts/install-mac.sh && ./scripts/install-mac.sh
```

**Ubuntu/Debian:**
```bash
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal && chmod +x scripts/install-ubuntu.sh && ./scripts/install-ubuntu.sh
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire\portal
powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
```

**Docker:**
```bash
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal
cp .env.example .env
docker-compose up -d
```

For detailed deployment instructions, see [portal/DEPLOYMENT.md](portal/DEPLOYMENT.md).

### Features

- **Guided Creation Flow** - 4-question framework for building exercises
- **AI-Powered Generation** - Support for OpenAI (GPT-4) and Anthropic (Claude)
- **Document Types** - Scenario briefs, facilitator guides, participant handbooks, inject cards, assessment rubrics, after-action templates
- **PDF Export** - Professional document generation
- **Web Interface** - Easy-to-use browser-based portal

## Road Map

| Phase | Deliverable | Timeframe |
|-------|-------------|-----------|
| Phase 1 | AI Prompt Framework + 2 Scenarios | 2 months |
| Phase 2 | Open-source Toolkit + Ethics Guide | 4 months |
| Phase 3 | Community Engagement + Feedback Loop | 6 months |
| Phase 4 | Launch and OWASP Distribution | 8-9 months |

## Project Structure

```
www-project-zombies-on-fire/
├── portal/                 # Tabletop Exercise Portal (FastAPI application)
│   ├── app/               # Application code
│   ├── scripts/           # Platform installation scripts
│   ├── Dockerfile         # Docker configuration
│   ├── docker-compose.yml # Development Docker Compose
│   ├── docker-compose.prod.yml  # Production Docker Compose
│   ├── DEPLOYMENT.md      # Detailed deployment guide
│   └── README.md          # Portal documentation
├── index.md               # OWASP project page
├── CONTRIBUTING.md        # Contribution guidelines
├── SECURITY.md            # Security policy
└── LICENSE.md             # License information
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Security

For security issues, see [SECURITY.md](SECURITY.md).

## License

This project is part of OWASP and follows OWASP licensing.

## Project Leaders

- Nathan Case (nathan.case@owasp.org)
- Jon McCoy (jon.mccoy@owasp.org)
