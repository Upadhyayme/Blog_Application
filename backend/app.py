import os
from flask import Flask

app = Flask(__name__)

# Your application code here

if __name__ == "__main__":
    app.run(host='0.0.0.0')