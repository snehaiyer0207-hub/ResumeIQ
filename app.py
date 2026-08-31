from flask import Flask, render_template, request
from analyzer import analyze_resume, JOB_SKILLS

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", job_roles=JOB_SKILLS.keys())


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("resume")
    role = request.form.get("job_role", "Data Analyst")

    if not file:
        return "Please upload a resume."

    try:
        result = analyze_resume(file, role)
        return render_template("result.html", result=result, job_role=role)
    except Exception as error:
        return f"Error analyzing resume: {error}"


if __name__ == "__main__":
    app.run(debug=True)