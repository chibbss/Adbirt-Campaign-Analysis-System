# crew.py

from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, output_json
from textwrap import dedent
import yaml
from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class FinalCampaignAnalysisReport(BaseModel):
    predicted_conversion_rate: Optional[float] = Field(
        None,
        description="Predicted conversion rate as a percentage (0-100%). Include only if the conversion_prediction_agent was used."
    )
    key_strengths: List[str] = Field(
        default_factory=list,
        description="Bulleted list of positive aspects synthesized from available agent reports."
    )
    key_recommendations: List[str] = Field(
        default_factory=list,
        description="Bulleted list of actionable recommendations synthesized from available agent reports."
    )
    suggested_new_campaign_details: Dict[str, str] = Field(
        default_factory=dict,
        description="Suggested changes based on available agent reports (e.g., budget, bidding, personalization)."
    )
    projected_conversion_if_optimized: Optional[str] = Field(
        None,
        description="A concise note estimating improved conversion rate if the user implements the key recommendations, with the final %"
    )

@CrewBase
class AdCampaignAnalysisCrew:
    """CrewAI Advertising Campaign Analysis Crew"""

    agents_config_path = "config/agents.yaml"
    tasks_config_path = "config/tasks.yaml"

    # === AGENTS ===

    @agent
    def tier_manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["tier_manager"],
            tools=[],
            allow_delegation=True,
            verbose=False,
        )

    @agent
    def conversion_prediction_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["conversion_prediction_agent"],
            tools=[],
            allow_delegation=False,
            verbose=False,
        )

    @agent
    def budget_allocation_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["budget_allocation_agent"],
            tools=[],
            allow_delegation=False,
            verbose=False,
        )

    @agent
    def bid_optimization_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["bid_optimization_agent"],
            tools=[],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def ad_personalization_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["ad_personalization_agent"],
            tools=[],
            allow_delegation=False,
            verbose=False,
        )

    @agent
    def chief_aggregator_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["chief_aggregator"],
            tools=[],
            allow_delegation=False,
            verbose=False,
        )

    # === TASKS ===

    @task
    def tier_manager_task(self) -> Task:
        return Task(
            config = self.tasks_config["tier_manager_task"],
            agent=self.tier_manager_agent(),
        )

    @task
    def conversion_prediction_task(self) -> Task:
        return Task(
            config = self.tasks_config["conversion_prediction_task"],
            agent=self.conversion_prediction_agent(),
        )

    @task
    def budget_allocation_task(self) -> Task:
        return Task(
            config = self.tasks_config["budget_allocation_task"],
            agent=self.budget_allocation_agent(),
        )

    @task
    def bid_optimization_task(self) -> Task:
        return Task(
            config = self.tasks_config["bid_optimization_task"],
            agent=self.bid_optimization_agent(),
        )

    @task
    def ad_personalization_task(self) -> Task:
        return Task(
            config = self.tasks_config["ad_personalization_task"],
            agent=self.ad_personalization_agent(),
        )

    @task
    def chief_aggregator_task(self) -> Task:
        return Task(
            config = self.tasks_config["chief_aggregator_task"],
            agent=self.chief_aggregator_agent(),
           output_json =FinalCampaignAnalysisReport,
        )

    # === CREW ===

    @crew
    def crew(self) -> Crew:
        """Creates the Advertising Campaign Analysis Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False,
        )