from flask import render_template
from flask_login import login_required
from .. import app 

@app.get('/')
@login_required
def main():
    return render_template('main.html')