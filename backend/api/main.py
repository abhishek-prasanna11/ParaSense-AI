import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inference.predict import initialize_models, predict_similarity
from logging_config import setup_logging

# Initialize structured JSON logger
logger = setup_logging()

app = FastAPI(
    title="Paraphrase & Semantic Similarity API",
    description="API for checking if two sentences are paraphrases and retrieving their similarity score.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Middleware: log every request with latency ───
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000

    # Skip logging health-check noise to keep the index lean
    if request.url.path != "/":
        logger.info(
            "request_completed",
            extra={
                "event": "request_completed",
                "method": request.method,
                "endpoint": str(request.url.path),
                "status_code": response.status_code,
                "response_time_ms": round(duration_ms, 2),
                "client_ip": request.client.host if request.client else "unknown",
            },
        )
    return response

# Load machine learning model during startup
@app.on_event("startup")
def startup_event():
    logger.info("model_loading_started", extra={"event": "startup", "phase": "model_init"})
    initialize_models()
    logger.info("model_loading_complete", extra={"event": "startup", "phase": "model_ready"})

class AnalyzeRequest(BaseModel):
    text1: str
    text2: str

class AnalyzeResponse(BaseModel):
    similarity: float
    paraphrase: bool

@app.get("/")
def health_check():
    return {"status": "Backend running"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    if not payload.text1.strip() or not payload.text2.strip():
        logger.warning(
            "empty_input_rejected",
            extra={"event": "validation_error", "detail": "Missing input text"},
        )
        raise HTTPException(status_code=400, detail="Missing input text")
    
    start = time.time()
    similarity, is_paraphrase = predict_similarity(payload.text1, payload.text2)
    inference_ms = (time.time() - start) * 1000

    logger.info(
        "inference_completed",
        extra={
            "event": "inference",
            "similarity_score": round(float(similarity), 4),
            "is_paraphrase": bool(is_paraphrase),
            "inference_time_ms": round(inference_ms, 2),
            "text1_length": len(payload.text1),
            "text2_length": len(payload.text2),
        },
    )
    
    return AnalyzeResponse(
        similarity=round(float(similarity), 4),
        paraphrase=bool(is_paraphrase)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
