# AdBirt AI Campaign Analysis API

A FastAPI-based backend service that leverages CrewAI and various AI agents to analyze and optimize advertising campaigns.

## Overview

This API provides AI-powered insights for digital advertising campaigns, offering various analysis features based on user subscription tier:

- **Conversion Prediction**: Analyzes campaign metrics to predict conversion probabilities
- **Budget Allocation**: Optimizes ad spend distribution for maximum ROI
- **Bid Optimization**: Determines optimal bid prices for real-time bidding (RTB) auctions
- **Ad Personalization**: Tailors ad creatives based on audience targeting

## Subscription Tiers

The API supports different feature sets based on the user's subscription plan:

- **Basic Plan ($5/month)**: Conversion Prediction, Budget Allocation
- **Pro Plan ($9/month)**: Conversion Prediction, Budget Allocation, priority support
- **Advanced Plan ($10.99/month)**: Conversion Prediction, Bid Optimization, Budget Allocation
- **Enterprise Plan ($12.99/month)**: Ad Personalization, Conversion Prediction, AI-Driven Recommendation, Account Management, Budget Allocation

## API Endpoints

### Health Check
```
GET /health
```
Returns the status of the API.

### Campaign Analysis
```
POST /campaign/analyze/
```
Analyzes campaign data based on the selected agent and user tier.

#### Request Format
```json
{
  "user_tier": "basic",
  "agent_selected": "conversion_prediction",
  "campaign_name": "Summer Sales Boost",
  "campaign_objective": "Increase conversions",
  "campaign_description": "A campaign to promote summer deals",
  "campaign_destination": "https://example.com/summer-sale",
  "banner_size": "300x250",
  "banner_type": "static",
  "daily_ad_budget": 500.0,
  "start_date": "2025-04-01",
  "end_date": "2025-04-30",
  "target_country": ["US", "UK", "Canada"],
  "media_url": "https://example.com/banner.jpg"
}
```

#### Response Format
The API returns responses in the following format:

```json
{
  "status": "success",
  "data": "Detailed analysis content based on the agent selected"
}
```

**Example Response (Ad Personalization)**:
```json
{
  "status": "success",
  "data": "**Ad Personalization Report for the \"Summer Sales Boost\" Campaign**\n\n**1. Recommended Creative Variations:**\n- **Dynamic Imagery:** Incorporate dynamic elements in the static banner, such as rotating images of various summer products, to capture different interests within the audience.\n- **Localized Content:** Create variations of the ad that include localized images or references to cultural symbols relevant to the US, UK, and Canada. For instance, featuring iconic summer locations or events from each country.\n- **Personalized Messaging:** Use personalized text overlays that address the specific audience segment, such as \"Enjoy Summer in [Country] with Our Exclusive Deals!\"\n\n**2. Expected Engagement Improvements:**\n- By integrating dynamic imagery and localized content, we anticipate an increase in engagement by approximately 15-20%, as these elements resonate more effectively with the audience's cultural and personal preferences.\n- Personalized messaging is expected to enhance the click-through rate (CTR) from 1.5% to potentially 2.0%, improving the overall interaction with the ad.\n\n**3. AI-Driven Insights for Content Tailoring:**\n- **User Behavior Analysis:** Utilize AI tools to analyze user interaction data, identifying patterns that can inform future creative adjustments. For instance, if a particular product image receives higher engagement, prioritize it in future ads.\n- **Sentiment Analysis:** Implement AI-driven sentiment analysis on feedback or comments related to the campaign to gauge audience reactions and adapt the messaging accordingly.\n- **Predictive Engagement Models:** Deploy AI models to predict which creative elements are likely to perform best based on historical data and current trends, allowing for proactive adjustments.\n\n**4. Creative Insights for Better Engagement:**\n- **Color Psychology:** Use bright, summer-themed colors that evoke a sense of excitement and urgency, encouraging users to engage with the ad.\n- **Call-to-Action (CTA) Optimization:** Test different CTAs, such as \"Shop Now,\" \"Discover Deals,\" or \"Uncover Savings,\" to determine which generates the highest response rate.\n- **Visual Hierarchy:** Ensure that the most critical information, such as discounts or limited-time offers, is prominently displayed to capture attention immediately.\n\nBy implementing these personalized ad variations and leveraging AI-driven insights, the \"Summer Sales Boost\" campaign is poised to significantly enhance its engagement and conversion rates. This approach not only aligns with the campaign's objective to increase conversions but also maximizes the effectiveness of the allocated budget, ensuring a robust return on investment."
}
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key
- Git

### Installation Guide

#### 1. Clone the Repository
```bash
git clone https://github.com/adbirt/Adbirt-Campaign-Optimizer.git
cd Adbirt-Campaign-Optimizer
```

#### 2. Set Up a Virtual Environment
```bash
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

#### 3. Upgrade Package Management Tools
```bash
pip install --upgrade pip setuptools wheel
```

#### 4. Install Core Dependencies
```bash
pip install crewai fastapi uvicorn openai langchain langchain-openai
```

#### 5. Install Additional Dependencies
```bash
pip install pydantic python-dotenv tiktoken requests
```

#### 6. Install Search Tool
```bash
pip install -U duckduckgo-search
```

#### 7. Set Up Environment Variables
Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_ORGANIZATION_ID=your_organization_id
```

#### 8. Run the Server
```bash
uvicorn api:app --reload
```

## Example Usage

### cURL

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_tier": "enterprise",
    "campaign_name": "Q2 Marketing Blitz",
    "campaign_objective": "Increase brand awareness and sales",
    "campaign_description": "This campaign focuses on boosting our visibility and driving conversions through targeted digital marketing strategies.",
    "campaign_destination": "https://www.brandsite.com",
    "banner_size": "300x250",
    "banner_type": "static",
    "daily_ad_budget": 5000.00,
    "start_date": "2025-05-01",
    "end_date": "2025-06-30",
    "target_country": ["Nigeria"],
    "media_url": "https://www.brandsite.com/assets/media/creative-banner.jpg"
  }'
```

### Python

```python
import requests
import json

url = "http://localhost:8000/campaign/analyze/"
headers = {"Content-Type": "application/json"}
payload = {
    "user_tier": "premium",
    "campaign_name": "Summer Sales Boost",
    "campaign_objective": "Increase conversions",
    "campaign_description": "A campaign to promote summer deals",
    "campaign_destination": "https://example.com/summer-sale",
    "banner_size": "300x250",
    "banner_type": "static",
    "daily_ad_budget": 500.0,
    "start_date": "2025-04-01",
    "end_date": "2025-04-30",
    "target_country": ["US", "UK", "Canada"],
    "media_url": "https://example.com/banner.jpg"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json())
```

## Architecture

The system is built on these core components:
- **FastAPI**: Handles HTTP requests and responses
- **CrewAI**: Orchestrates the AI agents working together
- **OpenAI Models**: Powers the AI capabilities
  - GPT-3.5-Turbo: Used for basic tier management
  - GPT-4o-Mini: Powers conversion prediction, budget allocation, and bid optimization
  - GPT-4o: Powers advanced ad personalization features

## Troubleshooting

Common issues and solutions:

1. **API Key Authentication Errors**:
   - Ensure your `.env` file has the correct OpenAI API key
   - Check that the environment variables are properly loaded

2. **Dependency Conflicts**:
   - Use a dedicated virtual environment
   - Follow the installation steps in the correct order

3. **Server Won't Start**:
   - Check for port conflicts (default is 8000)
   - Ensure all dependencies are correctly installed
