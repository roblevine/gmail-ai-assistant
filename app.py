import os
import logging
import json
import time

from dotenv import load_dotenv, find_dotenv

from flask import Flask, request, jsonify, render_template, Response

import openai
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama.llms import OllamaLLM

logger = logging.getLogger('.')
logger.setLevel('DEBUG')

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    _ = load_dotenv(find_dotenv())
    openai.api_key  = os.getenv('OPENAI_API_KEY')

    # Define a new graph
    workflow = StateGraph(state_schema=MessagesState)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that can answer questions about anything. "
                + "You will keep answers relatively short, without being so terse as to be rude. "
                + "You will also provide a source for your information. "
                + "If you don't know the answer, you will say so. "
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    #model = ChatOpenAI(model="gpt-3.5-turbo")
    #model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    ollama_url = os.getenv("OLLAMA_URL")
    model = OllamaLLM(model="llama3", base_url=ollama_url)

    # Define the function that calls the model
    def call_model(state: MessagesState):
        chain = prompt | model
        response = chain.invoke(state)
        return {"messages": response}

    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    chat_app = workflow.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "abc345"}}
    language = "English"

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        user_input = request.form['user_input']
        input_messages = [HumanMessage(user_input)]
        output = chat_app.invoke({"messages": input_messages}, config)
        answer = output["messages"][-1].content
        
        return jsonify({'response': answer})

    def generate_response(user_input):
        messages = [HumanMessage(user_input)]    
        for chunk in chat_app.stream(
            {"messages": messages},
            config,
        ):
            #if isinstance(chunk, AIMessage):  # Filter to just model responses
             #   yield f"data: {json.dumps({'response': chunk.content})}\n\n"
        #        yield f"data: {json.dumps({'response': chunk.messages[-1]})}\n\n"
              #  print(chunk['model']['message'][-1])
                yield f"data: {json.dumps({'response': chunk['model']['messages']})}\n\n"
                time.sleep(0.1)

    @app.route('/stream', methods=['POST'])
    def stream():
        user_input = request.form['user_input']
        return Response(
            generate_response(user_input),
            mimetype='text/event-stream'
        )
      
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)