# app.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.services.gati_path.router import router as gati_router

app = FastAPI(title="Vitarai Enterprise Engine API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows connections from any origin (React, local files, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your core ML/IoT processing router
app.include_router(gati_router)


base_dir = os.path.dirname(os.path.abspath(__file__))
dist_path = os.path.join(base_dir, "backend", "dist")

if not os.path.exists(dist_path):
    dist_path = os.path.join(base_dir, "dist")

assets_path = os.path.join(dist_path, "assets")

# 🛑 SAFETY GUARD: Create directories if they do not exist to prevent boot crashes
if not os.path.exists(assets_path):
    print(f"⚠️ [STATIC MOUNT WARNING]: Build directory '{assets_path}' not found.")
    print("👉 Generating placeholder directory fallback to allow server startup.")
    os.makedirs(assets_path, exist_ok=True)
    # Put a dummy file inside so Starlette's indexer evaluates cleanly
    with open(os.path.join(dist_path, "index.html"), "w") as f:
        f.write("<h1>Gati-Path Standalone Pipeline Online</h1><p>Please run 'npm run build' and paste the contents into the dist folder.</p>")

# 1. Mount compiled production asset bundles safely
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
# 2. Main Entry Points
@app.get("/")
def home():
    return {"message": "Vitarai Engine is Live"}

@app.get("/gati-path/dashboard")
async def serve_dashboard():
    """
    Serves the production-compiled index.html entry point directly 
    at the standalone dashboard URL route.
    """
    index_file_path = os.path.join(dist_path, "index.html")
    if os.path.exists(index_file_path):
        return FileResponse(index_file_path)
    return {"error": "Frontend build files not found inside backend/dist. Please run 'npm run build' first."}