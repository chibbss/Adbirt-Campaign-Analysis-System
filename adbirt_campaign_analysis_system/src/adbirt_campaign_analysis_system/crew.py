# crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, output_json
from textwrap import dedent
import yaml
from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union


class FinalCampaignAnalysisReport(BaseModel):
    current_metrics: Optional[Dict[str, float]] = Field(
        default_factory=dict,
        description="Current campaign metrics based on campaign details - a conversion prediction probability score and a campaign success score representing an aggregation of all the reports available to the user."
    )

    strengths: Optional[List[Dict[str, str]]] = Field(
        default_factory=list,
        description="List of campaign strengths with id, title, and description."
    )

    original_campaign: Optional[Dict[str, Union[str, float, List[str]]]] = Field(
        default_factory=dict,
        description="The original campaign details as submitted by the user."
    )

    optimized_campaign: Optional[Dict[str, Union[str, float, List[str]]]] = Field(
        default_factory=dict,
        description="An optimized version of the campaign details generated using insights from all agents. This includes a better campaign name, tweaked start/end dates for better timing, possibly improved banner format, and refined budget suggestions based on predicted effectiveness. All fields reflect improved values while maintaining original intent."
    )

    optimization_summary: Optional[List[Dict[str, str]]] = Field(
        default_factory=list,
        description="A list of recommended changes and their expected improvements. Each entry should explain what was changed and why it’s beneficial."
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
            verbose=True,
        )

    @agent
    def conversion_prediction_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["conversion_prediction_agent"],
            tools=[],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def budget_allocation_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["budget_allocation_agent"],
            tools=[],
            allow_delegation=False,
            verbose=True,
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
            verbose=True,
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