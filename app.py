# create a web based chatbot using flask that uses chatgpt to generate responses

from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():

    user_input = request.form['user_input']

    
    _ = load_dotenv(find_dotenv())

    openai.api_key  = os.getenv('OPENAI_API_KEY')
    client = openai.OpenAI(
    # This is the default and can be omitted
    #api_key=os.environ.get("OPENAI_API_KEY"),
)
    user_input = request.form['user_input']
    completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_input,
        }
    ],
    model="gpt-3.5-turbo",
)
    answer = completion.choices[0].message.content
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(debug=True)
