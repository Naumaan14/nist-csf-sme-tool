# ============================================================
# app.py  —  Flask Web Application
# NIST CSF 2.0 Risk Assessment Tool
# Nauman Salimbhai Shaikh | MSc Cybersecurity | CO7047
# ============================================================
from flask import (Flask, render_template, request,
                   send_file, session, redirect, url_for)
from engine import QUESTIONS, calculate_results
from export import generate_excel
import io, json

app = Flask(__name__)
app.secret_key = "nist-csf-tool-2024"
app.jinja_env.globals.update(enumerate=enumerate)

FUNCTIONS = list(QUESTIONS.keys())   # ordered list


@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/assess", methods=["GET", "POST"])
def assess():
    """One page per NIST function, stepped."""
    step = int(request.args.get("step", 0))

    if request.method == "POST":
        # Save responses for current step
        fn = FUNCTIONS[step]
        answers = []
        for i in range(5):
            val = request.form.get(f"q{i}", "3")
            answers.append(int(val))
        if "responses" not in session:
            session["responses"] = {}
        session["responses"][fn] = answers
        session.modified = True

        next_step = step + 1
        if next_step >= len(FUNCTIONS):
            return redirect(url_for("results"))
        return redirect(url_for("assess", step=next_step))

    fn       = FUNCTIONS[step]
    progress = int((step / len(FUNCTIONS)) * 100)
    return render_template(
        "assess.html",
        fn=fn,
        questions=QUESTIONS[fn],
        step=step,
        total=len(FUNCTIONS),
        progress=progress,
        prev_step=step - 1,
    )


@app.route("/results")
def results():
    if "responses" not in session:
        return redirect(url_for("index"))
    responses = session["responses"]
    if len(responses) < len(FUNCTIONS):
        return redirect(url_for("assess", step=len(responses)))

    data = calculate_results(responses)
    session["results"] = json.dumps(data)   # cache for export
    return render_template("results.html", data=data)


@app.route("/export")
def export():
    if "results" not in session:
        return redirect(url_for("index"))
    data     = json.loads(session["results"])
    org_name = request.args.get("org", "Organisation")
    xlsx     = generate_excel(data, org_name)
    return send_file(
        io.BytesIO(xlsx),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=f"NIST_Risk_Assessment_{org_name.replace(' ','_')}.xlsx",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
