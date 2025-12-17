from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from uuid import uuid4
import shutil
import os

from worker import process_pdf_job, JOBS

app = FastAPI(title="PDF Phrase Finder")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    phrase: str
):
    job_id = str(uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{job_id}.pdf")

    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    JOBS[job_id] = {
        "status": "processing",
        "result": None
    }

    background_tasks.add_task(
        process_pdf_job,
        job_id,
        pdf_path,
        phrase
    )

    return {"job_id": job_id}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"error": "job not found"})

    return {
        "status": job["status"],
        "result": job["result"]
    }
