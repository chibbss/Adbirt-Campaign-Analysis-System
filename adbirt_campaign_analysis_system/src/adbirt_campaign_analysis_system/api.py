from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import json
from crew import AdCampaignAnalysisCrew
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === INPUT MODEL ===
class CampaignInput(BaseModel):
    user_tier: str
    campaign_name: str
    campaign_objective: str
    campaign_description: str
    campaign_destination: str  # must be str not HttpUrl for CrewAI inputs
    banner_size: str
    banner_type: str
    daily_ad_budget: float
    start_date: str
    end_date: str
    target_country: List[str]
    media_url: str  # same here, keep as str for now


@app.post("/analyze")
async def analyze_campaign(campaign_data: CampaignInput):
    try:
        raw_input = campaign_data.dict()
        campaign_crew = AdCampaignAnalysisCrew()
        raw_output = campaign_crew.crew().kickoff(inputs=raw_input)

        # Convert CrewOutput-like object to dict if needed
        if hasattr(raw_output, "dict"):
            raw_output = raw_output.dict()
        elif hasattr(raw_output, "to_dict"):
            raw_output = raw_output.to_dict()

        # If it’s now a dict, check for json_dict or raw
        if isinstance(raw_output, dict):
            if 'json_dict' in raw_output:
                return JSONResponse(content=raw_output['json_dict'], status_code=200)
            elif 'raw' in raw_output:
                try:
                    parsed = json.loads(raw_output['raw'])
                    return JSONResponse(content=parsed, status_code=200)
                except json.JSONDecodeError:
                    # fallback — send the entire thing
                    return JSONResponse(content=raw_output, status_code=200)

        # Fallback: try to return raw_output anyway (last resort)
        return JSONResponse(content=raw_output, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Capture the app start time
start_time = datetime.utcnow()

@app.get("/health", tags=["Health Check"])
def health_check():
    uptime: timedelta = datetime.utcnow() - start_time
    return JSONResponse(
        content={
            "status": "ok",
            "uptime": str(uptime)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)