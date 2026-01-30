---

layout: col-sidebar
title: OWASP Zombies on Fire
tags: example-tag
level: 2
type: code
pitch: AI-powered framework for generating advanced cybersecurity tabletop exercises

---

This OWASP project proposes the development of an open-source, AI assisted framework for generating advanced tabletop cybersecurity exercises. These exercises are built to enhance organizational readiness through dynamic, threat-realistic scenarios that align with OWASP's mission to improve the security of software and systems.

The project addresses the lack of accessible, scalable, and high-fidelity tabletop exercises. Traditional tabletops often fall short limited in scope, unrealistic, or resource-intensive to develop. By using AI to assist in the creation and customization of exercises, this project democratizes access to world-class training tools and aligns with OWASP's broader goals around secure system development and awareness.

### Tabletop Exercise Portal

The portal is an AI-powered web application for creating and managing tabletop exercises. It features a guided 4-question creation flow, multiple LLM provider support (OpenAI, Anthropic), and professional PDF document generation.

#### Platform Support

| Platform | Installation |
|----------|--------------|
| macOS | `./scripts/install-mac.sh` |
| Ubuntu/Debian | `./scripts/install-ubuntu.sh` |
| Windows | `scripts\install-windows.ps1` |
| Docker | `docker-compose up -d` |

**Requirements:** Python 3.11+, 2GB RAM minimum

#### Quick Start

```bash
# Clone the repository
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal

# Run platform-specific installer (or use Docker)
./scripts/install-mac.sh      # macOS
./scripts/install-ubuntu.sh   # Ubuntu/Debian
docker-compose up -d          # Docker

# Open http://localhost:8000
```

For detailed deployment instructions, see [portal/DEPLOYMENT.md](portal/DEPLOYMENT.md).

### Road Map

|Phase|Deliverable|Timeframe|
|-------|------------------------------------|----------|
|Phase 1|AI Prompt Framework + 2 Scenarios|2 months|
|Phase 2|Open-source Toolkit + Ethics Guide|4 months|
|Phase 3|Community Engagement + Feedback Loop|6 months|
|Phase 4|Launch and OWASP Distribution|8–9 months|
