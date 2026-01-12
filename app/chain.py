import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from app.weather import get_weather

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0.7,
    api_key=api_key
)

# Define tools for the agent
tools = [
    Tool(
        name="get_weather",
        func=get_weather,
        description="""Get the current weather for a location. Use this tool when the user asks about weather, temperature, or outdoor conditions.
        Input should be a city name or location (e.g., 'Madrid', 'New York', 'London').
        The tool returns weather data that you should integrate naturally into a conversational response."""
    )
]

# Create agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly and conversational assistant with access to weather information.
    
When users ask about the weather:
1. Use the get_weather tool to fetch current weather data
2. Integrate the weather information naturally into your response, like you're having a conversation
3. Be warm and personable - don't just list facts
4. Add context or helpful suggestions based on the weather (e.g., "It's quite chilly, you might want to bring a jacket")
5. Use natural language instead of bullet points

Remember: You're chatting with someone, not writing a weather report!"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Create memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Create agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=False,
    handle_parsing_errors=True
)

def chat(message: str) -> str:
    """
    Send a message to the chatbot and get a response.
    The chatbot can access weather information and maintain conversation history.
    """
    response = agent_executor.invoke({"input": message})
    return response["output"]
