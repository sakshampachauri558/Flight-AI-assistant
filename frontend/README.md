# Altitude Resolutions

Local frontend for the Airline Resolution Agent.

## Local Links

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)
- Backend API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Run Locally

Start the backend in one PowerShell terminal:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Start the frontend in a second PowerShell terminal:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Then open [http://localhost:3000](http://localhost:3000).

## Backend Setup

The first time you run the backend, create the virtual environment and install dependencies:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Environment Variables

Create `.env` in the project root:

```dotenv
MISTRAL_API_KEY=your_mistral_api_key
MISTRAL_MODEL=mistral-large-latest
```

Keep the real API key private. The local policy fallback allows the backend to continue when Mistral embeddings are unavailable.

## Frontend Commands

Run these commands from the `frontend` directory:

```powershell
npm.cmd run dev      # Start local development
npm.cmd run lint     # Check frontend code
npm.cmd run build    # Create a production build
npm.cmd run start    # Start the production build
```

## Backend Tests

Run from the `backend` directory:

```powershell
pytest
```

## Deploy Frontend To Vercel

The complete application can be deployed as one Vercel project. Next.js serves the frontend, while the existing FastAPI app is exposed as a Vercel Python function under `/api`.

1. Push this repository to GitHub.
2. In Vercel, select **Add New Project** and import the repository.
3. Keep the project root as the repository root. Do not set the Root Directory to `frontend`.
4. Keep the framework as **Next.js**.
5. Leave the build and install commands from `vercel.json` unchanged.
6. Add this Vercel environment variable:

```text
NEXT_PUBLIC_API_URL=/api
```

7. Deploy the project.

The root `vercel.json` routes API requests to `api/index.py`, which imports the FastAPI application from `backend/app/main.py`.

For the full architecture and file-by-file explanation, see [PROJECT_DOCUMENTATION.md](../PROJECT_DOCUMENTATION.md).
