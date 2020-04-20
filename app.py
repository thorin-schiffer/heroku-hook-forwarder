import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from requests.auth import HTTPBasicAuth
from github import Github

app = Flask(__name__)

load_dotenv()
VCS_TYPE = os.getenv("VCS_TYPE")
ORG = os.getenv("ORG")
REPO = os.getenv("REPO")
CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY")
CIRCLE_JOB_NAME = os.getenv("CIRCLE_JOB_NAME")
CIRCLE_WORKFLOW_ID = os.getenv("CIRCLE_WORKFLOW_ID")


def resolve_branch_name(sha1):
    if VCS_TYPE != 'github':
        print("Don't know how to resolve sha1 to branch for non github repos")
    g = Github()
    repo = g.get_repo(f"{ORG}/{REPO}")
    branches = repo.get_branches()
    for branch in branches:
        if branch.commit.sha == sha1:
            return branch.name


@app.route('/', methods=['GET', 'POST'])
def forward():
    context = {}
    if request.method == 'POST':
        sha1_head = request.form['head_long']
        review_url = request.form['url']
        branch = resolve_branch_name(sha1_head)
        if branch:
            url = f"https://circleci.com/api/v1.1/project/{VCS_TYPE}/{ORG}/{REPO}/tree/{branch}"
        else:
            url = f"https://circleci.com/api/v1.1/project/{VCS_TYPE}/{ORG}/{REPO}"
        print(f"Redirecting hook to {url}")
        response = requests.post(
            url,
            auth=HTTPBasicAuth(CIRCLE_API_KEY, ''),
            data={
                "build_parameters[CIRCLE_JOB]": CIRCLE_JOB_NAME,
                "build_parameters[REVIEW_URL]": review_url,
                "build_parameters[CIRCLE_WORKFLOW_ID]": CIRCLE_WORKFLOW_ID,
                "revision": sha1_head
            }
        )
        print(response.json(), request.form)
        context['response'] = response.json()
    return render_template('forward.html', **context)


if __name__ == '__main__':
    print(resolve_branch_name("ed08fd17ef1e5199e9d34f48f1358416ba30fe54"))
