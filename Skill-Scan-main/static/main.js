// main.js

document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("analyzeForm");
  const btn = document.getElementById("submitBtn");
  const load = document.getElementById("loading");
  const err = document.getElementById("errorAlert");
  const resCard = document.getElementById("resultCard");
  const themeBtn = document.getElementById("themeToggle");
  const exampleBtn = document.getElementById("exampleBtn");

  // =========================
  // THEME TOGGLE
  // =========================

  const setTheme = (t) => {
    document.body.classList.remove("light", "dark");
    document.body.classList.add(t);

    themeBtn.textContent = (t === "dark") ? "☀️" : "🌙";

    localStorage.setItem("theme", t);
  };

  const saved = localStorage.getItem("theme") || "light";

  setTheme(saved);

  themeBtn.addEventListener("click", () => {
    setTheme(
      document.body.classList.contains("dark")
        ? "light"
        : "dark"
    );
  });

  // =========================
  // EXAMPLE JD
  // =========================

  exampleBtn.addEventListener("click", () => {

    document.getElementById("jd").value =
      "We are hiring a Software Engineer with experience in Python, Flask, Docker, REST APIs, SQL, Machine Learning, AWS, CI/CD, and cloud deployment.";

  });

  // =========================
  // FORM SUBMIT
  // =========================

  form.addEventListener("submit", async (e) => {

    e.preventDefault();

    err.classList.add("d-none");
    resCard.classList.add("d-none");

    btn.disabled = true;
    load.classList.remove("d-none");

    const fd = new FormData(form);

    try {

      const r = await fetch("/analyze", {
        method: "POST",
        body: fd
      });

      const j = await r.json();

      if (!j.success) {
        throw new Error(j.error || "Unknown error");
      }

      const out = j.result || {};

      // =========================
      // MATCH SCORE
      // =========================

      let score =
        out["JD Match"] ??
        out["match_score"] ??
        0;

      let pct = 0;

      if (typeof score === "string") {

        const m = score.match(/\d+/);

        pct = m ? Number(m[0]) : 0;

      } else if (typeof score === "number") {

        pct = Math.round(score);
      }

      pct = Math.max(0, Math.min(100, pct));

      document.getElementById("matchScoreBadge").innerHTML =
        `<span class="badge bg-info">${pct}%</span>`;

      document.getElementById("matchProgress").style.width =
        pct + "%";

      // =========================
      // MISSING KEYWORDS
      // =========================

      const missing =
        out["Missing Keywords"] ||
        out["MissingKeywords"] ||
        out["missing_keywords"] ||
        [];

      document.getElementById("missingKeywords").textContent =
        missing.length
          ? missing.join(", ")
          : "No critical keywords missing.";

      // =========================
      // EXTRA ANALYSIS
      // =========================

      const strengths =
        out["Strengths"] || [];

      const weaknesses =
        out["Weaknesses"] || [];

      const recommendations =
        out["ATS Recommendations"] || [];

      const improvements =
        out["Resume Improvements"] || [];

      const projects =
        out["Suggested Projects"] || [];

      const certs =
        out["Recommended Certifications"] || [];

      const summary =
        out["Profile Summary"] ||
        "No summary available.";

      const verdict =
        out["Final Verdict"] ||
        "No verdict available.";

      // =========================
      // BUILD RESULT HTML
      // =========================

      document.getElementById("profileSummary").innerHTML = `

        <div class="mb-4">
          <h5>📌 Profile Summary</h5>
          <p>${summary}</p>
        </div>

        <div class="mb-4">
          <h5>✅ Strengths</h5>
          <ul>
            ${strengths.map(s => `<li>${s}</li>`).join("")}
          </ul>
        </div>

        <div class="mb-4">
          <h5>⚠️ Weaknesses</h5>
          <ul>
            ${weaknesses.map(w => `<li>${w}</li>`).join("")}
          </ul>
        </div>

        <div class="mb-4">
          <h5>🚀 ATS Recommendations</h5>
          <ul>
            ${recommendations.map(r => `<li>${r}</li>`).join("")}
          </ul>
        </div>

        <div class="mb-4">
          <h5>🛠 Resume Improvements</h5>
          <ul>
            ${improvements.map(i => `<li>${i}</li>`).join("")}
          </ul>
        </div>

        <div class="mb-4">
          <h5>💡 Suggested Projects</h5>
          <ul>
            ${projects.map(p => `<li>${p}</li>`).join("")}
          </ul>
        </div>

        <div class="mb-4">
          <h5>🎓 Recommended Certifications</h5>
          <ul>
            ${certs.map(c => `<li>${c}</li>`).join("")}
          </ul>
        </div>

        <div class="mb-4">
          <h5>📋 Final Verdict</h5>
          <p><strong>${verdict}</strong></p>
        </div>

      `;

      // =========================
      // SHOW RESULT
      // =========================

      resCard.classList.remove("d-none");

    } catch (e2) {

      err.textContent =
        e2.message || "An error occurred";

      err.classList.remove("d-none");

    } finally {

      btn.disabled = false;

      load.classList.add("d-none");
    }

  });

});