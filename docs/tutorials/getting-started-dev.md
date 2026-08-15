# Tutorial: Getting Started with Local Development

This step-by-step tutorial guides you through setting up a complete local development environment for **barincairo.com**, including the PostgreSQL + PostGIS database, FastAPI Python backend, and Next.js frontend.

---

## Prerequisites

Before starting, ensure you have installed:
- **Node.js**: v20.x or higher
- **Python**: v3.11+
- **Docker & Docker Compose**: For local PostGIS containerization
- **Git**: For version control

---

## Step 1: Clone the Repository & Environment Setup

```bash
# Clone the repository
git clone git@github.com:alexseif/barincairo.com.git
cd barincairo.com

# Copy the environment configuration
cp .env.example .env
```

Review `.env` parameters to verify default database credentials and local ports.

---

## Step 2: Launch PostGIS Data Tier

Start the PostgreSQL / PostGIS container using Docker Compose:

```bash
docker compose up -d db
```

Verify that the PostGIS database container is running cleanly:

```bash
docker compose ps
```

---

## Step 3: Set Up Python Backend (FastAPI)

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Run local database migrations / table creation script:
   ```bash
   python -m backend.app.db_init
   ```

4. Start the FastAPI development server:
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```

Verify backend health by navigating to `http://localhost:8000/docs` in your browser.

---

## Step 4: Set Up Frontend (Next.js)

1. Open a new terminal window and navigate to the project root.
2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Next.js dev server:
   ```bash
   npm run dev
   ```

4. Open `http://localhost:3000` to view the interactive spatial map of Downtown Cairo.

---

## Next Steps

- Learn how venue data is processed in the **[Ingestion Pipeline Guide](../how-to/ingestion-pipeline.md)**.
- Review the database structure in the **[PostGIS Database Schema Reference](../reference/database-schema.md)**.
- Explore the **[System Architecture Overview](../explanation/architecture-overview.md)**.
