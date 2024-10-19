from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os, yaml, sys
from crewai_tools import DirectoryReadTool, FileReadTool,CodeInterpreterTool, DOCXSearchTool



llm1 ='groq/llama-3.1-70b-versatile'
llm2 = 'mistral/codestral-latest'

docs_tool = DirectoryReadTool()
code = CodeInterpreterTool()
tools = [docs_tool, code]



@CrewBase
class WebportcrewCrew():
	"""Webportcrew crew"""

	def __init__(self):
		self.original_agents_config_path = r'config/agents.yaml'
		self.original_tasks_config_path = r'config/tasks.yaml'
		
		with open(r'config/agents.yaml', 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open(r'config/tasks.yaml', 'r') as f:
			self.tasks_config = yaml.safe_load(f)
   
	@agent
	def ui_ux_designer(self) -> Agent:
		return Agent(
			config=self.agents_config['ui_ux_designer'],
			tools=tools, 
			verbose=True,
			llm=llm1,
			allow_code_execution=True
		)

	@agent
	def software_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['software_developer'],
			verbose=True,
			llm=llm1,
			tools=tools,
			allow_code_execution=True
		)


	@task
	def ui_ux_task(self) -> Task:
		return Task(
			config=self.tasks_config['ui_ux_task'],
			agent=self.ui_ux_designer(),
			output_file='ui_ux_design.md'
		)
	@task
	def html_task(self) -> Task:
		return Task(
			config=self.tasks_config['html_task'],
			agent=self.software_developer(),
			output_file='index.html'
		)
	@task
	def css_task(self) -> Task:
		return Task(
			config=self.tasks_config['css_task'],
			agent=self.software_developer(),
			output_file='styles/styles.css'
		)
	@task
	def js_task(self) -> Task:
		return Task(
			config=self.tasks_config['js_task'],
			agent=self.software_developer(),
			output_file='scripts/script.js'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SimplePort crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)