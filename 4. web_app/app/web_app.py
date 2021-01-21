__author__ = 'xead'
from codecs import open
from flask import Flask, render_template, request

from app.filmsearch import predict

app = Flask(__name__)
@app.route("/", methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    if request.method == "POST":
        text = request.form.get("text")
        logfile = open("ydf_demo_logs.txt", "a", "utf-8")
        prediction_message = predict(text)
        print("<response>", file=logfile)
        print(text, file=logfile)
        print(prediction_message, file=logfile)
        print("</response>", file=logfile)
        logfile.close()
    return render_template('filmsearch.html', text=text, prediction_message=prediction_message)


if __name__ == "__main__":
    app.run()

