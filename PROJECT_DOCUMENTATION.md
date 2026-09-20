# Airline Resolution Agent

## 1. Project Overview

Airline Resolution Agent is a customer-support application for airline booking problems. It lets an agent or support operator:

- Select a customer booking scenario.
- View customer and booking information.
- Ask for help with cancellations, delays, refunds, rebooking, hotels, vouchers, or upgrades.
- Apply airline policy rules.
- Execute simulated support actions.
- Escalate requests that require a supervisor.
- See the result in a browser dashboard.

The project has two separately running applications:

1. A Next.js frontend. 
2. A FastAPI backend.

The frontend calls the backend over HTTP. The backend reads local data, evaluates the request through a LangGraph workflow, and returns a structured response.

---

## 2. Technology Stack

### Frontend

- **Next.js 16**: React framework used for the web application.
- **React 19**: Component and state-management layer.
- **TypeScript**: Static typing for frontend code.
- **Tailwind CSS 4**: Utility-first styling.
- **shadcn/ui patterns**: Reusable UI component structure.
- **Radix/Base UI dependencies**: Accessible UI primitives used by the component setup.
- **Lucide React**: Icons for customer, flight, chat, status, and activity elements.
- **React Markdown**: Renders agent responses that contain Markdown.
- **Framer Motion**: Installed for possible motion interactions; the current dashboard uses CSS motion for its card entrance effect.
- **Next Font**: Loads DM Sans for body text, Space Grotesk for headings, and Geist Mono for monospace text.


### Backend


- **Python**: Backend programming language.
- **FastAPI**: HTTP API framework.
- **Uvicorn**: ASGI development and production server.
- **Pydantic**: Request and response validation.
- **python-dotenv**: Loads environment variables from `.env`.
- **LangGraph**: Builds and runs the agent state graph.
- **LangChain**: Supporting framework for model and retrieval integrations.
- **langchain-mistralai**: Mistral chat-model and embedding integration.
- **FAISS**: Local vector index used for policy retrieval.
- **MarkdownHeaderTextSplitter**: Splits policy Markdown into retrievable sections.

### Data Layer

There is currently **no database** such as PostgreSQL, MySQL, MongoDB, or SQLite.

The project uses:

- `data/customers.json` for customer records.
- `data/bookings.json` for booking records.
- `data/policies.md` for airline policy text.
- Mistral embeddings plus an in-memory FAISS index for policy search when the API key is valid.
- A local Markdown fallback when Mistral embeddings cannot be created.

The action tools currently simulate operations by returning dictionaries. They do not persist refunds, rebookings, vouchers, or hotel reservations to a database.

---

## 3. Directory Structure

```text
airline-resolution-agent/
|-- .env                         Local secrets and model settings; do not commit
|-- .env.example                 Safe environment-variable template
|-- .gitignore                   Ignores local secrets and generated files
|-- PROJECT_DOCUMENTATION.md     This document
|-- data/
|   |-- bookings.json             Booking and flight data
|   |-- customers.json            Customer profile data
|   |-- policies.md               Airline policy rules
|-- backend/
|   |-- requirements.txt          Python dependencies
|   |-- app/
|   |   |-- main.py               FastAPI application and HTTP endpoints
|   |   |-- config.py             Environment configuration
|   |   |-- agent/
|   |   |   |-- graph.py          LangGraph workflow and agent decisions
|   |   |   |-- state.py           AgentState TypedDict
|   |   |-- models/
|   |   |   |-- schemas.py         Pydantic API request/response models
|   |   |-- rag/
|   |   |   |-- policy_rag.py      Policy splitting, embeddings, and search
|   |   |-- tools/
|   |       |-- actions.py         Simulated support actions and policy checks
|   |       |-- data_retrieval.py  JSON customer and booking lookups
|   |-- tests/
|       |-- test_booking.py       Booking lookup tests
|       |-- test_customer.py       Customer lookup tests
|       |-- test_policy.py         Agent scenario and tool tests
|       |-- test_priya.py          Cancellation scenario tests
|-- frontend/
    |-- package.json               Frontend dependencies and scripts
    |-- next.config.ts             Next.js configuration
    |-- tsconfig.json              TypeScript configuration
    |-- eslint.config.mjs          ESLint configuration
    |-- postcss.config.mjs         PostCSS/Tailwind configuration
    |-- components.json            UI component configuration
    |-- public/
    |   |-- airline_banner.jpg     Dashboard header image
    |   |-- file.svg, globe.svg,
    |       next.svg, vercel.svg,
    |       window.svg              Default/static assets
    |-- src/
        |-- app/
        |   |-- layout.tsx          Root layout, fonts, metadata
        |   |-- page.tsx             Home page entry point
        |   |-- globals.css          Theme tokens and global styles
        |-- components/
        |   |-- Dashboard.tsx        Main customer-support dashboard
        |   |-- ui/
        |       |-- badge.tsx        Status and tier badges
        |       |-- button.tsx       Shared button component
        |       |-- card.tsx         Card layout primitives
        |       |-- input.tsx         Chat input field
        |       |-- label.tsx         Shared label component
        |       |-- scroll-area.tsx   Scrollable chat/content area
        |       |-- separator.tsx     Divider component
        |-- lib/
            |-- utils.ts             Shared class-name utility
```

---

## 4. Frontend Files and Responsibilities

### `frontend/src/app/layout.tsx`

Defines the root HTML layout for the Next.js application.

Responsibilities:

- Loads the application fonts.
- Applies font variables to the document.
- Sets page metadata and browser title.
- Provides the root `<html>` and `<body>` elements.
- Imports global CSS.

### `frontend/src/app/page.tsx`

The home route entry point.

Responsibilities:

- Imports `Dashboard`.
- Renders the dashboard at `/`.

### `frontend/src/app/globals.css`

Defines the global visual system.

Responsibilities:

- Imports Tailwind and animation styles.
- Defines theme colors and border/radius tokens.
- Sets body font size and line height.
- Defines heading typography.
- Provides dashboard card entrance and hover motion.
- Disables motion when the user prefers reduced motion.

### `frontend/src/components/Dashboard.tsx`

The main client-side application screen.

Responsibilities:

- Stores the selected booking reference.
- Loads customer details from the backend.
- Loads booking details from the backend.
- Stores conversation messages.
- Sends chat requests to the backend.
- Displays customer profile and travel history.
- Displays flight status and disruption reason.
- Displays executed actions and escalation state.
- Displays policies returned by the backend.
- Provides scenario buttons for Priya, Arvind, and Meher.
- Renders agent responses with `ReactMarkdown`.
- Shows loading and connection-error states.
- Provides the responsive visual dashboard layout.

Current frontend API calls:

```text
GET  http://localhost:8000/api/customer/{booking_reference}
GET  http://localhost:8000/api/booking/{booking_reference}
POST http://localhost:8000/api/chat
```

For deployment, the hardcoded localhost URL should be replaced with an environment variable such as `NEXT_PUBLIC_API_URL`.

### `frontend/src/components/ui/*`

These are reusable presentation components:

- `button.tsx`: Button variants and sizes.
- `card.tsx`: Card, header, title, content, and footer primitives.
- `badge.tsx`: Status, loyalty-tier, and booking labels.
- `input.tsx`: Text input used by the chat form.
- `scroll-area.tsx`: Scrollable conversation region.
- `separator.tsx`: Visual divider.
- `label.tsx`: Accessible form labels.

### `frontend/src/lib/utils.ts`

Contains shared utility helpers, primarily for combining conditional CSS class names.

### `frontend/package.json`

Defines frontend dependencies and commands:

```text
npm run dev      Start the development server.
npm run build    Create a production build.
npm run start    Start the production build.
npm run lint     Run ESLint.
```

---

## 5. Backend Files and Responsibilities

### `backend/app/main.py`

Creates the FastAPI application and exposes the public API.

Responsibilities:

- Creates the FastAPI app titled `Airline Resolution Agent API`.
- Enables CORS for frontend requests.
- Defines customer lookup endpoint.
- Defines booking lookup endpoint.
- Defines the chat endpoint.
- Builds the initial `AgentState` for each chat request.
- Invokes `app_graph`.
- Converts graph output into `ChatResponse`.

Endpoints:

```text
GET /api/customer/{booking_reference}
GET /api/booking/{booking_reference}
POST /api/chat
```

FastAPI also provides interactive documentation at:

```text
http://localhost:8000/docs
```

### `backend/app/config.py`

Loads configuration from the project root.

Responsibilities:

- Finds the project root.
- Loads `.env` or `.env.example` if available.
- Reads `MISTRAL_API_KEY`.
- Reads `MISTRAL_MODEL`.
- Defaults the model to `mistral-large-latest`.

The API key must remain in `.env` and should never be committed or written into public documentation.

### `backend/app/agent/state.py`

Defines `AgentState`, the shared data structure passed through the LangGraph workflow.

State fields include:

- `messages`: User conversation messages.
- `customer`: Loaded customer profile.
- `booking`: Loaded booking record.
- `intent`: Reserved intent field.
- `relevant_policy`: Policy text returned by RAG.
- `proposed_action`: Action selected by the decision logic.
- `policy_check`: Reserved policy-check field.
- `tool_results`: Results from support action tools.
- `escalation_required`: Whether a human must review the request.
- `escalation_reason`: Explanation for escalation.
- `final_response`: Text returned to the frontend.

### `backend/app/agent/graph.py`

Contains the central agent workflow and decision logic.

Workflow nodes:

1. `identify_context`
   - Confirms that a message exists.
   - Keeps the current state available for later nodes.

2. `retrieve_policy`
   - Sends the user message to `search_policy`.
   - Stores relevant policy text in the state.

3. `determine_action`
   - Reads the user message, booking status, and delay duration.
   - Detects upgrades and fare differences.
   - Detects refund, rebooking, hotel, compensation, and delay requests.
   - Detects gratitude messages such as `thanks` and selects a conversational response.
   - Escalates free upgrades and fare differences above 1,500.

4. `validate_and_execute`
   - Applies the selected action against booking status and policy conditions.
   - Calls the relevant action tool.
   - Records action results.
   - Avoids executing booking actions for conversational responses.

5. `generate_response`
   - Converts tool results into customer-facing language.
   - Produces escalation messages when required.
   - Produces refund, rebooking, hotel, voucher, lounge, or general responses.
   - Returns a formal response for thank-you messages.

The graph runs in this order:

```text
START
  -> identify_context
  -> retrieve_policy
  -> determine_action
  -> validate_and_execute
  -> generate_response
  -> END
```

### `backend/app/models/schemas.py`

Defines API validation models:

- `ChatRequest`: Requires `message` and `booking_reference`.
- `ChatResponse`: Returns `response`, `escalated`, `actions_taken`, and `policies_applied`.

Pydantic validates incoming JSON and formats outgoing API data.

### `backend/app/tools/data_retrieval.py`

Reads local JSON data.

Functions:

- `get_customer_profile(booking_reference)` searches `customers.json`.
- `get_booking_details(booking_reference)` searches `bookings.json`.

Both functions return the matching dictionary or `None` when no record exists.

### `backend/app/tools/actions.py`

Contains policy-aware simulated support actions.

Functions:

- `calculate_delay_compensation(delay_hours)` determines meal, lounge, and hotel eligibility.
- `validate_fare_difference(fare_difference)` allows differences up to 1,500.
- `escalate_to_human(reason, booking_reference)` creates an escalation result.
- `initiate_refund(booking_reference, is_airline_caused)` simulates a full refund.
- `rebook_customer(booking_reference, is_airline_caused)` simulates free rebooking within 24 hours.
- `arrange_hotel(booking_reference, delay_hours)` allows hotel coverage only above 5 hours.
- `issue_meal_voucher(booking_reference)` simulates a 500 rupee meal voucher.
- `grant_lounge_access(booking_reference)` simulates lounge access.

These functions return dictionaries. They do not write to a database or external airline system.

### `backend/app/rag/policy_rag.py`

Handles policy retrieval.

Responsibilities:

- Reads `data/policies.md`.
- Splits Markdown by policy and condition headers.
- Creates Mistral embeddings when the configured key works.
- Builds a FAISS vector store.
- Retrieves the most relevant policy sections.
- Falls back to the complete local policy document when no valid key is available or embedding creation fails.

The fallback ensures that deterministic agent behavior can continue even when Mistral embeddings are unavailable.

### `backend/requirements.txt`

Lists Python packages needed by the backend, including FastAPI, Uvicorn, Pydantic, LangChain, LangGraph, Mistral integration, FAISS, and environment configuration support.

---

## 6. Data Files

### `data/customers.json`

Stores customer profiles associated with booking references.

The frontend uses this data for:

- Customer name.
- Loyalty tier.
- Email.
- Phone number.
- Travel history.
- Previous complaints and resolutions.

### `data/bookings.json`

Stores booking and flight information.

The frontend and agent use this data for:

- Flight number.
- Route.
- Travel date.
- Scheduled departure.
- Booking status.
- Delay details.
- Cancellation reason.
- New departure time when available.

### `data/policies.md`

The source of truth for airline rules:

- Cancellation rebooking or refund choices.
- Delay compensation thresholds.
- Refund processing details.
- Fare-difference escalation threshold.
- Loyalty-tier rules.
- Hotel coverage limitations.

---

## 7. Request and Response Flow

Example chat flow:

```text
1. User selects booking scenario in the Next.js dashboard.
2. Frontend requests customer and booking data from FastAPI.
3. User submits a message.
4. Frontend sends ChatRequest to POST /api/chat.
5. FastAPI validates the request with Pydantic.
6. Backend retrieves customer and booking JSON records.
7. LangGraph creates an AgentState.
8. Policy retrieval searches policies.md using Mistral/FAISS or fallback text.
9. Decision logic selects an action or conversational response.
10. Action tools simulate refund, rebooking, hotel, voucher, lounge, or escalation.
11. Response generation creates customer-facing text.
12. FastAPI returns ChatResponse.
13. Dashboard renders the response and activity results.
```

Example request:

```json
{
  "message": "I want a full refund for my cancelled flight",
  "booking_reference": "SK4821X"
}
```

Example response shape:

```json
{
  "response": "A full refund has been initiated...",
  "escalated": false,
  "actions_taken": ["refund_initiated"],
  "policies_applied": ["Cancellation Rule"]
}
```

---

## 8. Included Scenarios

### Priya: `SK4821X`

- Cancelled flight.
- Used to test full refund and rebooking decisions.
- Gold loyalty tier.

### Arvind: `TR1190B`

- Four-hour delay.
- Used to test meal voucher and lounge access.

### Meher: `WL7742`

- Six-hour delay.
- Used to test meal voucher, lounge access, and hotel eligibility.

---

## 9. Local Setup

### Backend

From the `backend` directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

If PowerShell blocks script activation for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Frontend

From the `frontend` directory:

```powershell
npm.cmd install
npm.cmd run dev
```

Open:

```text
http://localhost:3000
```

The backend API documentation is available at:

```text
http://localhost:8000/docs
```

### Environment Variables

The project root `.env` should contain:

```dotenv
MISTRAL_API_KEY=your_mistral_api_key
MISTRAL_MODEL=mistral-large-latest
```

Never commit the real API key. Because a key was previously shared during development, it should be rotated before deployment.

---

## 10. Testing

Backend tests are run from the `backend` directory:

```powershell
pytest
```

The tests cover:

- Customer lookup.
- Booking lookup.
- Invalid booking/customer behavior.
- Delay compensation thresholds.
- Fare-difference validation.
- Refund behavior.
- Cancellation scenario behavior.
- Delay and hotel scenario behavior.
- Escalation behavior.

Frontend validation commands:

```powershell
npm.cmd run lint
npm.cmd run build
```

---

## 11. Deployment Notes

The frontend and backend should be deployed as separate services.

### Frontend deployment

The complete application is configured as one Vercel project. Next.js serves the frontend and Vercel's Python runtime exposes the FastAPI application through `api/index.py`.

Import the repository into Vercel and keep the project Root Directory at the repository root. Do not set it to `frontend`.

The frontend reads the backend URL from `NEXT_PUBLIC_API_URL` and keeps `http://localhost:8000` as its local fallback:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";
```

Configure this environment variable in Vercel:

```text
NEXT_PUBLIC_API_URL=/api
```

The root `requirements.txt` contains the Python dependencies needed by the Vercel function. The root `vercel.json` rewrites `/api/*` requests to the FastAPI function.

### Backend deployment

The backend is deployed inside the same Vercel project. Vercel must include:

- `data/customers.json`.
- `data/bookings.json`.
- `data/policies.md`.
- `MISTRAL_API_KEY`.
- `MISTRAL_MODEL`.

Add `MISTRAL_API_KEY` and `MISTRAL_MODEL` as Vercel environment variables. The frontend and API share the same domain, so no separate backend URL is needed.

### Database migration for production

For a production system, replace JSON and simulated actions with:

- A relational database such as PostgreSQL.
- Database models and migrations.
- Persistent action records.
- Authentication and role-based authorization.
- Audit logs for refunds, rebookings, and escalations.
- A managed vector database or persisted FAISS index if policy volume grows.

---

## 12. Current Limitations

- Refunds, rebookings, hotels, vouchers, and lounge access are simulated.
- JSON data is read from local files and is not suitable for concurrent production writes.
- Chat responses currently use deterministic rule logic; the Mistral chat model is initialized but not used to generate the final response.
- Policy embeddings are rebuilt when policy search is called rather than persisted and reused.
- The frontend uses `NEXT_PUBLIC_API_URL=/api` on Vercel and falls back to `http://localhost:8000/api` during local development.
- CORS currently allows all origins and should be restricted before production.
- There is no authentication, authorization, user account system, or audit trail.
- The API key must be rotated if it has been exposed.
