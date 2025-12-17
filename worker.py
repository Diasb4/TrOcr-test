from pdf_extractor import extract_target_page_paddle

JOBS = {}

def process_pdf_job(job_id: str, pdf_path: str, phrase: str):
    try:
        result = extract_target_page_paddle(pdf_path, phrase)
        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["result"] = result
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["result"] = str(e)
