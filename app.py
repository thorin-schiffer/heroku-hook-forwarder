import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

load_dotenv()
VCS_TYPE = os.getenv("VCS_TYPE")
ORG = os.getenv("ORG")
REPO = os.getenv("REPO")
CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY")
CIRCLE_JOB_NAME = os.getenv("CIRCLE_JOB_NAME")


@app.route('/', methods=['GET', 'POST'])
def forward():
    context = {}
    if request.method == 'POST':
        branch = request.form['head']
        url = f"https://circleci.com/api/v1.1/project/{VCS_TYPE}/{ORG}/{REPO}/tree/{branch}"
        response = requests.post(
            url,
            auth=HTTPBasicAuth(CIRCLE_API_KEY, ''),
            data={
                "build_parameters[CIRCLE_JOB]": CIRCLE_JOB_NAME
            }
        )
        context['response'] = response.json()
    return render_template('forward.html', **context)
