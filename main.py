from http.client import HTTPException

from fastapi import FastAPI
import httpx
from shared_models import Article, SynthesisRequest, AnalysisResult, ReportRequest, AcademicResearch

#Endpoints des services
ACADEMIC_SERVICE_URL = "http://academic-service:8001"
AI_SYNTHESIS_SERVICE_URL = "http://ai-synthesis-service:8002"

app = FastAPI(title="Gateway Service", description="Service de communication avec les autres services", version="0.1.0")

@app.get("/health")
async def health():
    return {"message": "healthy", "service": "gateway-service"}

@app.post("/api/v1/generate-report", response_model=AnalysisResult)
async def generate_report(request: ReportRequest):
    try:
        #1. Construction de la requête pour Academic Service
        academic_request = AcademicResearch(
            keywords=request.keywords,
            authors=request.authors,
            year_from=request.year_from,
            year_to=request.year_to,
            max_results=request.max_results
        )
        async with httpx.AsyncClient() as client:
            academic_response = await client.post(f"{ACADEMIC_SERVICE_URL}/search",
                                                  json=academic_request.model_dump(),
                                                  timeout=10)
            academic_response.raise_for_status()
            academic_data = academic_response.json()
        #Vérification qu'on a bien des articles
        if not academic_data.get("articles"):
            raise HTTPException("Aucun articles trouvé")

        #3. Construction de la requête pour AI service
        synthesis_query = SynthesisRequest(
            articles=academic_data["articles"],
            synthesis_type=request.synthesis_type,
            language=request.language,
            focus_areas=request.focus_areas
        )

        #4. Appel au service AI
        async with httpx.AsyncClient() as client:
            ai_response = await client.post(f"{AI_SYNTHESIS_SERVICE_URL}/synthesize",
                                            json=synthesis_query.model_dump(),
                                            timeout=60.0
                                            )
            ai_response.raise_for_status()
            return ai_response.json()
    except httpx.HTTPError as e:
        print(e)
        raise HTTPException(e)
    except Exception as e:
        print(e)
        raise HTTPException(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)