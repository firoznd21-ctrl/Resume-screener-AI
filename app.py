from flask import Flask, render_template, request
import os
from model import extract_text_from_pdf, match_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    score = None

    if request.method == "POST":
        job_desc = request.form["job_desc"]
        file = request.files["resume"]

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)
            score = match_resume(job_desc, resume_text)

    return render_template("index.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)