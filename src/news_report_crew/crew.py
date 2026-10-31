from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool

# define the web search tool
web_search_tool = SerperDevTool()

 
class NewsReport(BaseModel):
    title: str = Field(..., description="Title of the news report")
    source: str = Field(..., description="Source of the news report")
    date: str = Field(..., description="Date of the news report")
    summary: str = Field(..., description="Summary of the news report")
    url: str = Field(..., description="URL of the news report")
    tags: List[str] = Field(..., description="Tags for the news report")
    additional_notes: dict = Field(..., description="Additional notes for the news report")
    author: str = Field(..., description="Author of the news report")

@CrewBase
class NewsReportCrew():
    """NewsReportCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # config paths 
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # define my agents and tasks
    @agent
    def news_reporter(self) -> Agent:
        """Creates the news_reporter agent"""
        return Agent(
            config=self.agents_config["news_reporter"],
            verbose=True,
            tools=[web_search_tool]
        )

    @task
    def research_task(self) -> Task:
        """Creates the research_task task"""
        return Task(
            config=self.tasks_config["research_task"],
            verbose=True,
            output_json=NewsReport
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsReportCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
