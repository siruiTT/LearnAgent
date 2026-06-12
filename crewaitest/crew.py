import os
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI


@CrewBase
class CrewtestprojectCrew():
    def __init__(self):
        # 加载 YAML 配置（确保文件存在）
        with open('config/agents.yaml', 'r', encoding='utf-8') as f:
            self.agents_config = yaml.safe_load(f)
        with open('config/tasks.yaml', 'r', encoding='utf-8') as f:
            self.tasks_config = yaml.safe_load(f)

        # 直接使用字符串，不要 SecretStr
        self.llm = ChatOpenAI(
            model="kimi-k2.6",
            api_key="sk-mQnOyBvhUF3BqfHv2IUogEGu3QS1oPr2tKmmeEsmDz3tWMnD",  # ← 纯字符串
            base_url="https://api.moonshot.cn/v1",
            temperature=1
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            llm=self.llm
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            llm=self.llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
        )

    @crew
    def crew(self) -> Crew:
        # 显式列出 agents 和 tasks，避免依赖自动收集
        return Crew(
            agents=[self.researcher(), self.reporting_analyst()],
            tasks=[self.research_task(), self.reporting_task()],
            process=Process.sequential,
            verbose=True,
            callbacks=[],  # 可选：抑制回调警告
        )