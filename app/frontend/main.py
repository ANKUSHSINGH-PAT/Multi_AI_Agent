from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from common.custom_exception import CustomException
from common.logger import logging
from app.backend.xaml_parser import parse_xaml
from app.backend.rules import detect_errors
from app.backend.llm_explainer import explain
from app.backend.pdf_report import generate_pdf


app = FastAPI()

logging.info("Starting ICA Copilot application")

@app.post("/upload")
async def upload(file: UploadFile):

    try:
        content = await file.read()

        tree, activities = parse_xaml(content)
        errors, warnings = detect_errors(tree)

        try:
            llm_summary = explain(activities, errors, warnings)
        except Exception as llm_error:
            llm_summary = f"LLM failed: {llm_error}"

        return {
            "activities": activities,
            "errors": errors,
            "warnings": warnings,
            "explanation": llm_summary
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/download-report")
async def download_report(file: UploadFile):

    try:
        content = await file.read()

        tree, activities = parse_xaml(content)
        errors, warnings = detect_errors(tree)

        llm_summary = explain(activities, errors, warnings)

        pdf_buffer = generate_pdf(
            activities,
            errors,
            warnings,
            llm_summary
        )

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=ica_report.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))