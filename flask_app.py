# flask_app.py

import os
from io import BytesIO
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from helper import (
    get_groq_response,
    extract_pdf_text,
    prepare_prompt
)

# =========================
# FLASK APP CONFIG
# =========================

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

load_dotenv()

# =========================
# HOME ROUTE
# =========================

@app.route("/")
def index():
    return render_template("index.html")

# =========================
# ANALYZE ROUTE
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        # Get form data
        jd = request.form.get("jd", "").strip()
        uploaded_file = request.files.get("resume")

        # Validation
        if not jd:
            return jsonify({
                "success": False,
                "error": "Job description is required."
            }), 400

        if uploaded_file is None or uploaded_file.filename == "":
            return jsonify({
                "success": False,
                "error": "Please upload a PDF resume."
            }), 400

        # Extract PDF text
        file_stream = BytesIO(uploaded_file.read())
        resume_text = extract_pdf_text(file_stream)

        # Prepare ATS prompt
        input_prompt = prepare_prompt(
            resume_text=resume_text,
            job_description=jd
        )

        # AI analysis
        result_json = get_groq_response(input_prompt)

        # Final response
        return jsonify({
            "success": True,
            "result": result_json
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8501,
        debug=True
    )