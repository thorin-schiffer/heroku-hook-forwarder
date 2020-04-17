from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def forward():
    print(request.form)
    return render_template('forward.html')
