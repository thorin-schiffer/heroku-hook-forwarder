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
        sha1_head = request.form['head_long']
        review_url = request.form['url']
        url = f"https://circleci.com/api/v1.1/project/{VCS_TYPE}/{ORG}/{REPO}"
        response = requests.post(
            url,
            auth=HTTPBasicAuth(CIRCLE_API_KEY, ''),
            data={
                "build_parameters[CIRCLE_JOB]": CIRCLE_JOB_NAME,
                "build_parameters[CIRCLE_SHA1]": sha1_head,
                "build_parameters[CIRCLE_BRANCH]": "",
                "build_parameters[REVIEW_URL]": review_url,
            }
        )
        print(response.json(), request.form)
        context['response'] = response.json()
    return render_template('forward.html', **context)
