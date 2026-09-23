from flask import Flask
import socket

app = Flask(__name__)


@app.route("/")
def index():
    return (
        "<h1>SWE40006 Task 4.2</h1>"
        f"<p>Flask container running on host {socket.gethostname()}</p>"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
