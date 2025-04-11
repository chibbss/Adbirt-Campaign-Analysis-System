from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict
from crew import AdCampaignAnalysisCrew, FinalCampaignAnalysisReport
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Optional: Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


# Function to generate pretty JSON output
def generate_json_output(data):
    """
    Converts the input data into a pretty-printed JSON format.
    """
    return json.dumps(data, indent=4)


@app.post("/analyze", response_model=FinalCampaignAnalysisReport)
async def analyze_campaign(campaign_data: CampaignInput):
    try:
        # Step 1: Prepare input for the crew
        raw_input = campaign_data.dict()

        # Step 2: Initialize and run crew
        campaign_crew = AdCampaignAnalysisCrew()
        raw_output = campaign_crew.crew().kickoff(inputs=raw_input)

        # Step 3: Handle output if it's a string
        if isinstance(raw_output, str):
            try:
                raw_output = json.loads(raw_output)
            except Exception:
                raise HTTPException(status_code=500, detail="Crew output was not valid JSON.")

        # Step 4: Convert dict to response model
        if isinstance(raw_output, dict):
            try:
                # Generate JSON output
                json_output = generate_json_output(raw_output)
                # Return the formatted JSON in the response
                return {"formatted_json": json_output}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Output format mismatch: {str(e)}")

        raise HTTPException(status_code=500, detail="Crew did not return a valid JSON object.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)