from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
from datetime import datetime
from shared-models import Article, SynthesisRequest, AnalysisResult

#Endpoints des services
ACADEMIC_SERVICE_URL = "http://academic-data-service:8000"
AI_SYNTHESIS_SERVICE_URL = "http://ai-synthesis-service:8000"

app = FastAPI(title="Gateway Service", description="Service de communication avec les autres services", version="0.1.0")