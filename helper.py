from groq import Groq
import PyPDF2 as pdf
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# GROQ CLIENT
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# AI RESPONSE FUNCTION
# =========================

def get_groq_response(prompt):

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a world-class ATS resume analyzer and senior technical recruiter. "
                        "You MUST return only valid JSON with no markdown, no explanations, "
                        "and no extra text."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1200,
            top_p=0.9
        )

        response_text = completion.choices[0].message.content.strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", response_text, re.DOTALL)

        if not match:
            raise Exception("No valid JSON found in AI response.")

        json_text = match.group()

        parsed_json = json.loads(json_text)

        return parsed_json

    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")


# =========================
# PDF TEXT EXTRACTION
# =========================

def extract_pdf_text(uploaded_file):

    try:

        reader = pdf.PdfReader(uploaded_file)

        if len(reader.pages) == 0:
            raise Exception("PDF is empty.")

        text_content = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                cleaned = text.replace("\n", " ").strip()
                text_content.append(cleaned)

        final_text = " ".join(text_content)

        if len(final_text.strip()) < 50:
            raise Exception("Resume text could not be extracted properly.")

        return final_text

    except Exception as e:
        raise Exception(f"PDF Extraction Error: {str(e)}")



# =========================
# ADVANCED ATS PROMPT
# =========================

def prepare_prompt(resume_text, job_description):

    prompt = f"""

You are a world-class ATS Resume Analyzer,
Senior Technical Recruiter,
Career Coach,
and Resume Optimization Expert.

Your task is to deeply analyze the candidate's resume
against the provided job description.

==================================================
JOB DESCRIPTION
==================================================

{job_description}

==================================================
RESUME
==================================================

{resume_text}

==================================================
ANALYSIS OBJECTIVES
==================================================

Perform detailed ATS and recruiter-level analysis.

Evaluate:

1. Technical skill match
2. Experience relevance
3. ATS keyword optimization
4. Resume formatting quality
5. Project relevance
6. Domain relevance
7. Industry alignment
8. Resume strengths
9. Resume weaknesses
10. Hiring potential
11. Missing technologies
12. Missing certifications
13. Missing impact metrics
14. Resume clarity and readability

==================================================
SCORING RULES
==================================================

- Be realistic and strict.
- Avoid inflated scores.
- Score 90+ only for highly optimized resumes.
- Penalize missing important skills.
- Penalize weak projects.
- Penalize lack of measurable achievements.
- Penalize irrelevant content.

==================================================
RESUME IMPROVEMENT TASK
==================================================

Provide highly actionable improvement suggestions.

Suggestions should include:

- Missing technical skills
- Better ATS keywords
- Better project descriptions
- Better resume wording
- Quantifiable achievement suggestions
- Better certifications to add
- Better formatting suggestions
- Better profile summary suggestions
- Stronger action verbs
- Important tools/frameworks to learn

==================================================
RETURN FORMAT
==================================================

Return ONLY valid JSON.

DO NOT return markdown.
DO NOT return explanations.
DO NOT return code blocks.

Use this EXACT JSON structure:

{{
    "JD Match": 78,

    "Matching Skills": [
        "Python",
        "Machine Learning",
        "Flask"
    ],

    "Missing Keywords": [
        "Docker",
        "AWS",
        "CI/CD"
    ],

    "Strengths": [
        "Strong machine learning projects",
        "Good Python foundation",
        "Relevant academic background"
    ],

    "Weaknesses": [
        "Missing deployment experience",
        "No cloud technologies mentioned",
        "Projects lack measurable outcomes"
    ],

    "Profile Summary": "Detailed ATS-friendly recruiter evaluation summary.",

    "ATS Recommendations": [
        "Add cloud technologies like AWS or Azure",
        "Improve project descriptions with measurable impact",
        "Use stronger ATS keywords from the job description"
    ],

    "Resume Improvements": [
        "Add GitHub links for all projects",
        "Include Docker and deployment experience",
        "Use action verbs like developed, optimized, engineered",
        "Add quantified achievements",
        "Improve technical skills section formatting"
    ],

    "Suggested Projects": [
        "End-to-end MLOps deployment project",
        "Cloud-based Flask AI application",
        "Real-time AI analytics dashboard"
    ],

    "Recommended Certifications": [
        "AWS Certified Cloud Practitioner",
        "Google Data Analytics",
        "Deep Learning Specialization"
    ],

    "Final Verdict": "Moderately suitable candidate with strong potential after resume optimization."
}}

"""

    return prompt