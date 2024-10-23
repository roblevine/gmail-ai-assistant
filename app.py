# create a web based chatbot using flask that uses chatgpt to generate responses

from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

app = Flask(__name__)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)


    @app.route('/')
    def home():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)