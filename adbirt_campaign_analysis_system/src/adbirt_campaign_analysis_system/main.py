#!/usr/bin/env python
import sys

from crew import AdCampaignAnalysisCrew



def run():
    inputs = {
        "user_tier": "enterprise",
        "campaign_name": "Summer Sale Campaign",
        "campaign_objective": "Increase sales by 20%",
        "campaign_description": "A campaign to boost summer sales with discounts.",
        "campaign_destination": "https://www.yourwebsite.com/summer-sale",
        "banner_size": "728x90",
        "banner_type": "gif",
        "daily_ad_budget": "1000",
        "start_date": "2025-06-01",
        "end_date": "2025-06-30",
        "target_country": "USA",
        "media_url": "https://www.yourwebsite.com/images/summer-banner.gif",
    }
    AdCampaignAnalysisCrew().crew().kickoff(inputs=inputs)




if __name__ == "__main__":
    run()