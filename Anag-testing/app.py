from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello_world():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8"/>
        </head>
        <body>
            Hello World
        </body>
    </html>
    """

if __name__ == "__main__":
    app.debug = True
    app.run()
