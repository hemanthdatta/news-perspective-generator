from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    print("Starting test application...")
    app.run(debug=True, port=8000, host='0.0.0.0')
