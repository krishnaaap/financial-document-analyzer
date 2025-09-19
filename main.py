from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import datetime
from helpers import save_result
from db import collection
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

app = FastAPI(title="Financial Document Analyzer")

# -----------------------------
# Async Crew Runner
# -----------------------------
async def run_crew(query: str, file_path: str):
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True,
        memory=False
    )
    result = await financial_crew.kickoff(inputs={"query": query, "file_path": file_path})
    return result

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

# -----------------------------
# Fetch all MongoDB results
# -----------------------------
@app.get("/results")
async def get_results():
    cursor = collection.find({})
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        results.append(doc)
    return {"results": results}

# -----------------------------
# Analyze PDF Endpoint
# -----------------------------
@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded PDF
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"

        # -----------------------------
        # Run Crew pipeline
        # -----------------------------
        try:
            crew_result = await run_crew(query=query.strip(), file_path=file_path)

            # Combine all agent outputs into one string
            combined_output = ""
            for agent_name, task_output in crew_result.items():
                combined_output += f"{agent_name}: {task_output}\n"

            combined_output = combined_output.strip()

            # Save combined result to MongoDB
            await save_result(file.filename, query.strip(), combined_output)
            response = combined_output

        except Exception as e:
            # Crew failed → save fallback
            fallback = f"Crew failed: {str(e)}"
            await save_result(file.filename, query.strip(), fallback)
            response = fallback

        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

# -----------------------------
# Run Uvicorn Server
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
