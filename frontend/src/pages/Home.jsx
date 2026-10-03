import { useState } from "react";

import Hero from "../components/Hero";
import Loading from "../components/Loading";
import Navbar from "../components/Navbar";
import ScoreCard from "../components/ScoreCard";
import UploadBox from "../components/UploadBox";
import { analyzeResume } from "../services/api";


function SkillBadge({ children, type = "normal" }) {
  return (
    <span className={`skill-badge ${type}`}>
      {children}
    </span>
  );
}


function SectionTitle({
  eyebrow,
  title,
  description,
}) {
  return (
    <div className="section-title">
      <span>{eyebrow}</span>

      <h2>{title}</h2>

      {description && (
        <p>{description}</p>
      )}
    </div>
  );
}


export default function Home() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] =
    useState("");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleAnalyze(event) {
    event.preventDefault();

    setError("");

    if (!file) {
      setError("Please upload your resume PDF.");
      return;
    }

    if (!jobDescription.trim()) {
      setError(
        "Please paste the job description."
      );
      return;
    }

    if (jobDescription.trim().length < 30) {
      setError(
        "Please provide a more detailed job description."
      );
      return;
    }

    try {
      setLoading(true);

      const data = await analyzeResume(
        file,
        jobDescription.trim()
      );

      setResult(data);

      setTimeout(() => {
        document
          .getElementById("results")
          ?.scrollIntoView({
            behavior: "smooth",
          });
      }, 100);

    } catch (err) {
      setError(
        err.message ||
          "Unable to analyze the resume."
      );
    } finally {
      setLoading(false);
    }
  }


  function handleReset() {
    setFile(null);
    setJobDescription("");
    setResult(null);
    setError("");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }


  const atsScore =
    result?.ats?.score ?? 0;

  const jobMatch =
    result?.job_match?.score ?? 0;

  const readiness =
    result?.placement?.overall_readiness ?? 0;

  const matchedSkills =
    result?.job_match?.matched_skills ?? [];

  const missingSkills =
    result?.job_match?.missing_skills ?? [];

  const roadmap =
    result?.roadmap ?? [];

  const atsBreakdown =
    result?.ats?.report ?? {};

  const ai =
    result?.ai_feedback ?? null;


  return (
    <div className="app">
      <Navbar />

      <main>
        <Hero />

        {!result && (
          <section className="analysis-card">
            <SectionTitle
              eyebrow="01 — Your profile"
              title="Start your career analysis"
              description="Upload your resume and provide the job you want to target."
            />

            <form onSubmit={handleAnalyze}>
              <div className="form-grid">
                <UploadBox
                  file={file}
                  setFile={setFile}
                />

                <div className="job-box">
                  <label>
                    Target Job Description
                  </label>

                  <textarea
                    value={jobDescription}
                    onChange={(event) =>
                      setJobDescription(
                        event.target.value
                      )
                    }
                    placeholder="Paste the complete job description here..."
                  />

                  <div className="textarea-footer">
                    <span>
                      {jobDescription.length} characters
                    </span>

                    <span>
                      Include responsibilities and required skills
                    </span>
                  </div>
                </div>
              </div>

              {error && (
                <div className="error-box">
                  <span>!</span>
                  {error}
                </div>
              )}

              <button
                className="analyze-button"
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Analyzing..."
                  : "Analyze My Career →"}
              </button>
            </form>
          </section>
        )}

        {loading && (
          <Loading />
        )}

        {result && !loading && (
          <div
            id="results"
            className="results"
          >
            <section className="results-header">
              <div>
                <span className="result-eyebrow">
                  ANALYSIS COMPLETE
                </span>

                <h2>
                  Your CareerPilot Report
                </h2>

                <p>
                  {result.resume?.filename}
                  {" • "}
                  {result.resume?.pages} page(s)
                  {" • "}
                  {result.resume?.words} words
                </p>
              </div>

              <button
                className="secondary-button"
                onClick={handleReset}
              >
                Analyze Another Resume
              </button>
            </section>


            {/* SCORE CARDS */}
            <section className="score-grid">
              <ScoreCard
                label="ATS Score"
                score={atsScore}
                icon="◈"
                description="Resume structure and keyword readiness"
              />

              <ScoreCard
                label="Job Match"
                score={jobMatch}
                icon="◎"
                description="Recognized skills matching the target role"
              />

              <ScoreCard
                label="Placement Readiness"
                score={readiness}
                icon="✦"
                description="Combined career readiness indicator"
              />
            </section>


            {/* ATS */}
            <section className="dashboard-section">
              <SectionTitle
                eyebrow="02 — Resume intelligence"
                title="ATS Resume Analysis"
                description="A transparent rule-based score showing how your resume performs across important resume sections."
              />

              <div className="ats-layout">
                <div className="ats-main-card">
                  <div className="ats-score-circle">
                    <strong>{atsScore}</strong>
                    <span>/100</span>
                  </div>

                  <div>
                    <h3>
                      {atsScore >= 85
                        ? "Strong resume foundation"
                        : atsScore >= 70
                        ? "Good resume foundation"
                        : atsScore >= 55
                        ? "Room for improvement"
                        : "Needs improvement"}
                    </h3>

                    <p>
                      CareerPilot evaluates your resume
                      using consistent structural and
                      keyword-based criteria.
                    </p>
                  </div>
                </div>

                <div className="breakdown-card">
                  {Object.entries(
                    atsBreakdown
                  ).map(([label, value]) => (
                    <div
                      className="breakdown-row"
                      key={label}
                    >
                      <div>
                        <span>{label}</span>

                        <div className="progress-track">
                          <div
                            className="progress-fill"
                            style={{
                              width: `${Math.min(
                                100,
                                value * 5
                              )}%`,
                            }}
                          />
                        </div>
                      </div>

                      <strong>
                        {value}
                      </strong>
                    </div>
                  ))}
                </div>
              </div>

              {result.ats?.suggestions?.length > 0 && (
                <div className="suggestions-card">
                  <h3>
                    Resume improvement suggestions
                  </h3>

                  <div className="suggestion-list">
                    {result.ats.suggestions
                      .slice(0, 8)
                      .map((suggestion, index) => (
                        <div
                          key={index}
                          className="suggestion-item"
                        >
                          <span>→</span>
                          <p>{suggestion}</p>
                        </div>
                      ))}
                  </div>
                </div>
              )}
            </section>


            {/* JOB MATCH */}
            <section className="dashboard-section">
              <SectionTitle
                eyebrow="03 — Target role"
                title="Job Match Analysis"
                description={result.job_match?.message}
              />

              <div className="match-layout">
                <div className="match-score-card">
                  <span>JOB MATCH</span>

                  <strong>
                    {jobMatch}%
                  </strong>

                  <div className="large-progress">
                    <div
                      style={{
                        width: `${jobMatch}%`,
                      }}
                    />
                  </div>

                  <p>
                    {matchedSkills.length} of{" "}
                    {result.job_match
                      ?.total_required_skills ?? 0}{" "}
                    recognized required skills matched.
                  </p>
                </div>

                <div className="skill-panel">
                  <div>
                    <h3>
                      ✓ Matched Skills
                    </h3>

                    <div className="skill-list">
                      {matchedSkills.length ? (
                        matchedSkills.map(
                          (skill) => (
                            <SkillBadge
                              key={skill}
                              type="matched"
                            >
                              {skill}
                            </SkillBadge>
                          )
                        )
                      ) : (
                        <span className="empty-text">
                          No recognized matching skills.
                        </span>
                      )}
                    </div>
                  </div>

                  <div>
                    <h3>
                      + Missing Skills
                    </h3>

                    <div className="skill-list">
                      {missingSkills.length ? (
                        missingSkills.map(
                          (skill) => (
                            <SkillBadge
                              key={skill}
                              type="missing"
                            >
                              {skill}
                            </SkillBadge>
                          )
                        )
                      ) : (
                        <span className="empty-text">
                          No recognized missing skills.
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </section>


            {/* PLACEMENT */}
            <section className="dashboard-section">
              <SectionTitle
                eyebrow="04 — Career readiness"
                title="Placement Readiness"
                description="A combined indicator based on ATS quality, job match and recognized skill coverage."
              />

              <div className="readiness-card">
                <div className="readiness-score">
                  <strong>
                    {readiness}
                  </strong>

                  <span>/100</span>

                  <div className="stars">
                    {result.placement?.rating}
                  </div>

                  <h3>
                    {result.placement?.status}
                  </h3>
                </div>

                <div className="readiness-details">
                  <div>
                    <span>ATS Score</span>
                    <strong>
                      {result.placement?.ats_score}
                    </strong>
                  </div>

                  <div>
                    <span>Job Match</span>
                    <strong>
                      {result.placement?.job_match}%
                    </strong>
                  </div>

                  <div>
                    <span>Skill Coverage</span>
                    <strong>
                      {result.placement?.skill_coverage}%
                    </strong>
                  </div>
                </div>
              </div>
            </section>


            {/* ROADMAP */}
            <section className="dashboard-section">
              <SectionTitle
                eyebrow="05 — Growth plan"
                title="Personalized Career Roadmap"
                description="Your missing job skills are converted into practical learning steps."
              />

              {roadmap.length ? (
                <div className="roadmap-grid">
                  {roadmap.map((item) => (
                    <div
                      className="roadmap-card"
                      key={item.skill}
                    >
                      <div className="roadmap-top">
                        <div className="roadmap-icon">
                          ↗
                        </div>

                        <span
                          className={`priority ${item.priority.toLowerCase()}`}
                        >
                          {item.priority}
                        </span>
                      </div>

                      <h3>
                        {item.skill}
                      </h3>

                      <p>
                        {item.learn}
                      </p>

                      <div className="roadmap-meta">
                        <span>
                          Difficulty:{" "}
                          <strong>
                            {item.difficulty}
                          </strong>
                        </span>

                        <span>
                          Time:{" "}
                          <strong>
                            {item.estimated_time}
                          </strong>
                        </span>
                      </div>

                      <div className="project-box">
                        <small>
                          PRACTICAL PROJECT
                        </small>

                        <p>
                          {item.project}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="success-card">
                  <span>✓</span>
                  <div>
                    <h3>
                      No recognized skill gaps
                    </h3>

                    <p>
                      Your resume contains all the
                      technical skills recognized in
                      the target job description.
                    </p>
                  </div>
                </div>
              )}
            </section>


            {/* AI */}
            <section className="dashboard-section ai-section">
              <SectionTitle
                eyebrow="06 — AI career coach"
                title="CareerPilot AI Feedback"
                description="Personalized feedback based on your resume, target role and detected skill gaps."
              />

              {ai && (
                <>
                  <div className="ai-score">
                    <div>
                      <span>
                        AI Career Score
                      </span>

                      <strong>
                        {ai.score}/100
                      </strong>
                    </div>

                    <span className="ai-source">
                      {ai.source}
                    </span>
                  </div>

                  <div className="feedback-grid">
                    <div className="feedback-card">
                      <h3>
                        Strengths
                      </h3>

                      <ul>
                        {ai.strengths?.map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="feedback-card">
                      <h3>
                        Weaknesses
                      </h3>

                      <ul>
                        {ai.weaknesses?.map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}
                      </ul>
                    </div>

                    <div className="feedback-card wide">
                      <h3>
                        Recommended Actions
                      </h3>

                      <ul>
                        {ai.suggestions?.map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  </div>


                  <div className="interview-card">
                    <div>
                      <span className="result-eyebrow">
                        INTERVIEW PREP
                      </span>

                      <h3>
                        Questions you should prepare for
                      </h3>
                    </div>

                    <div className="question-list">
                      {ai.interview_questions?.map(
                        (question, index) => (
                          <div
                            key={index}
                            className="question"
                          >
                            <span>
                              {String(
                                index + 1
                              ).padStart(2, "0")}
                            </span>

                            <p>
                              {question}
                            </p>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                </>
              )}
            </section>


            <section className="final-cta">
              <div>
                <span>CAREERPILOT AI</span>

                <h2>
                  Your next career move starts here.
                </h2>

                <p>
                  Use this report as a roadmap,
                  not just a score.
                </p>
              </div>

              <button
                className="analyze-button compact"
                onClick={handleReset}
              >
                Analyze Again →
              </button>
            </section>
          </div>
        )}
      </main>

      <footer>
        <strong>
          CareerPilot AI
        </strong>

        <span>
          Resume Intelligence • Job Matching • Career Guidance
        </span>
      </footer>
    </div>
  );
}