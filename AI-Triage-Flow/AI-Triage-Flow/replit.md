# NeuralForge PS3.23

## Overview

NeuralForge PS3.23 is an AI-powered emergency triage system that analyzes emergency situations, categorizes them by severity and priority, and routes them to appropriate authorities (police, ambulance, fire brigade, disaster response, rescue team). The system features multi-language support, voice-to-text input, and automatic location detection.

The project uses a hybrid architecture with a Python FastAPI backend for AI processing and a React/TypeScript frontend built with Vite. The Python backend integrates with Google's Gemini AI for emergency analysis.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite with hot module replacement
- **Routing**: Wouter for client-side routing
- **State Management**: TanStack React Query for server state
- **UI Components**: shadcn/ui component library built on Radix UI primitives
- **Styling**: Tailwind CSS with CSS variables for theming

The frontend has two implementations:
1. A React SPA in `client/` using modern component patterns
2. A vanilla JS interface in `frontend/` with cyberpunk styling for the emergency triage interface

### Backend Architecture
- **Primary Server**: Python FastAPI (`backend/main.py`) handles emergency analysis
- **Node.js Wrapper**: Express server (`server/index.ts`) spawns the Python process
- **AI Integration**: Google Gemini AI (`gemini-flash-latest` model) for emergency triage analysis
- **Routing Engine**: Deterministic routing logic (`backend/routing_engine.py`) maps emergency categories to response units

The Python backend provides:
- `POST /api/emergency` - Accepts emergency reports and returns AI analysis
- `GET /healthz` - Health check endpoint

### Data Storage
- **Database**: PostgreSQL with Drizzle ORM
- **Schema Location**: `shared/schema.ts`
- **Migrations**: Managed via `drizzle-kit push`
- **Current Schema**: Basic users table with id, username, password fields
- **In-Memory Fallback**: `MemStorage` class for development without database

### Key Features
- **Multi-language Support**: English, Hindi, Marathi, Tamil, Telugu with translation maps
- **Voice Input**: Web Speech API integration for voice-to-text
- **Location Detection**: Geolocation API with OpenStreetMap reverse geocoding
- **Offline Mode**: Status banner for network connectivity awareness

## External Dependencies

### AI Services
- **Google Gemini AI**: Primary AI engine for emergency analysis (requires `GEMINI_API_KEY` environment variable)

### Database
- **PostgreSQL**: Primary data store (requires `DATABASE_URL` environment variable)
- **Drizzle ORM**: Type-safe database queries and schema management

### External APIs
- **OpenStreetMap Nominatim**: Reverse geocoding for location detection (no API key required)

### Browser APIs Used
- **Web Speech API**: Voice recognition (`SpeechRecognition`/`webkitSpeechRecognition`)
- **Geolocation API**: GPS-based location detection
- **Fetch API**: Network requests with offline detection