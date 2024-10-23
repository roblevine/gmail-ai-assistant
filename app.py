import os
import logging

from dotenv import load_dotenv, find_dotenv

from flask import Flask, request, jsonify, render_template

import openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

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
                "You are a helpful assistant that can answer questions about anything. You will keep answers relatively short, without being so terse as to be rude. You will also provide a source for your information. If you don't know the answer, you will say so.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    model = ChatOpenAI(model="gpt-3.5-turbo")

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
      
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)