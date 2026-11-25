"""Your first Flask app. Run it with the green Red button, or: python practice/hello.py
Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Student Management System</h1><p>Hello from Flask!</p>"


@app.route("/about")
def about():
    return "This app keeps track of the students at our school."


@app.route("/contact")
def contact():
    return "school@email.com"


if __name__ == "__main__":
    app.run(debug=True, port=5001)