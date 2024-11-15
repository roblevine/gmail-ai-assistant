from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.text_splitter import RecursiveCharacterTextSplitter
import subprocess
import os

# Function to initialize the LLM based on user choice
def get_llm(model_name: str):
    if model_name == "openai":
        return ChatOpenAI(model_name="gpt-3.5-turbo")
    elif model_name == "anthropic":
        return ChatAnthropic(model="claude-3")
    else:
        raise ValueError("Unsupported model name. Choose 'openai' or 'anthropic'.")

llm = get_llm("openai")

search = DuckDuckGoSearchRun()

@tool
def news_search(query: str) -> str:
    """Searches for latest news on a topic"""
    try:
        results = search.run(f"latest news {query}")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = text_splitter.split_text(results)
        return chunks[0] if chunks else "No results found"
    except Exception as e:
        return f"Error searching news: {str(e)}"

@tool
def general_search(query: str) -> str:
    """Searches for general information online"""
    try:
        results = search.run(query)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = text_splitter.split_text(results)
        return chunks[0] if chunks else "No results found"
    except Exception as e:
        return f"Error searching: {str(e)}"

@tool
def search_workspace(query: str) -> str:
    """Searches files in workspace"""
    try:
        result = subprocess.run(['grep', '-r', query, '.'], 
                              capture_output=True, text=True)
        return result.stdout or "No results found"
    except Exception as e:
        return f"Error searching workspace: {str(e)}"

@tool
def run_command(command: str) -> str:
    """Executes terminal command"""
    try:
        result = subprocess.run(command.split(), 
                              capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error executing command: {str(e)}"

tools = [
    Tool(name="NewsSearch", 
         func=news_search,
         description="Search for latest news on a topic"),
    Tool(name="WebSearch", 
         func=general_search,
         description="Search for general information online"),
    Tool(name="WorkspaceSearch", 
         func=search_workspace,
         description="Search files in workspace"),
    Tool(name="TerminalCommand", 
         func=run_command,
         description="Execute terminal commands")
]

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    max_iterations=3,
    early_stopping_method="generate"
)

def chat():
    print("News Assistant Ready! (type 'quit' to exit)")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'quit':
            break
        try:
            response = agent.run(user_input)
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    chat()