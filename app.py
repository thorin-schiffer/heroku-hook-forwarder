import os

from flask import Flask, render_template, request

app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv()
CIRCLE_API_URL = os.getenv("CIRCLE_API_URL")
CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY")
CIRCLE_JOB_NAME = os.getenv("CIRCLE_JOB_NAME")


@app.route('/', methods=['GET', 'POST'])
def forward():
    print(CIRCLE_JOB_NAME, CIRCLE_API_KEY, CIRCLE_API_URL)
    return render_template('forward.html')
