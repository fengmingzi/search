from app import app


@app.route('/test')
def hello_world():
    return 'Hello World!'