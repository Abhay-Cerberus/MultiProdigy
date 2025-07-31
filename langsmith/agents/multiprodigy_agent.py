from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langsmith_integration import trace_with_langsmith
from langsmith import Client

# Initialize LangSmith client
client = Client()

@trace_with_langsmith(project_name="multiprodigy")
def create_multiprodigy_agent(tools):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )
    return agent
