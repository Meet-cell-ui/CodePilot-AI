import { useState } from "react";
import "./App.css";

function App() {
  const [apiKey, setApiKey] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeProject = async () => {
    if (!apiKey.trim()) {
      setError("Please enter your CodePilot API key.");
      return;
    }

    if (!file) {
      setError("Please select a ZIP project.");
      return;
    }

    if (!file.name.toLowerCase().endsWith(".zip")) {
      setError("Please upload a ZIP file.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        headers: {
          "X-API-Key": apiKey,
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Project analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to CodePilot AI backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      setFile(null);
      return;
    }

    setError("");

    if (!selectedFile.name.toLowerCase().endsWith(".zip")) {
      setFile(null);
      setError("Please select a ZIP file.");
      return;
    }

    setFile(selectedFile);
  };

  const qualityScore =
    result?.analysis?.quality_score?.overall_score ?? 0;

  const securityIssues =
    result?.analysis?.security?.total_issues ?? 0;

  const totalFiles =
    result?.analysis?.project_structure?.total_files ?? 0;

  const functions =
    result?.analysis?.code_analysis?.functions ?? 0;

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="brand">
          <div className="brand-icon">CP</div>

          <div>
            <h1>CodePilot AI</h1>
            <p>AI-Powered Software Engineering Platform</p>
          </div>
        </div>

        <div className="status">
          <span></span>
          Backend Online
        </div>
      </header>

      <main className="container">
        {/* Hero */}
        <section className="hero">
          <div className="hero-badge">AI CODE INTELLIGENCE</div>

          <h2>Analyze Your Software Project</h2>

          <p>
            Upload your project and let CodePilot AI analyze
            code quality, security, architecture, and
            engineering improvements.
          </p>
        </section>

        {/* Upload */}
        <section className="upload-box">
          <div className="input-group">
            <label htmlFor="apiKey">CodePilot API Key</label>

            <input
              id="apiKey"
              className="api-input"
              type="password"
              placeholder="Enter your cpai_ API key"
              value={apiKey}
              onChange={(event) =>
                setApiKey(event.target.value)
              }
            />
          </div>

          <label className="file-label">
            <input
              type="file"
              accept=".zip"
              onChange={handleFileChange}
            />

            <div className="upload-icon">↑</div>

            <strong>
              {file
                ? file.name
                : "Upload your ZIP project"}
            </strong>

            <small>
              {file
                ? `${(file.size / 1024 / 1024).toFixed(2)} MB`
                : "ZIP files only"}
            </small>
          </label>

          <button
            className="analyze-button"
            onClick={analyzeProject}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing Project...
              </>
            ) : (
              "Analyze Project"
            )}
          </button>

          {loading && (
            <div className="loading-message">
              CodePilot AI is analyzing your project...
              <br />
              <small>
                Scanning structure, code quality, security
                and AI insights.
              </small>
            </div>
          )}

          {error && <div className="error">{error}</div>}
        </section>

        {/* Results */}
        {result && (
          <section className="results">
            <div className="project-title">
              <div>
                <span className="eyebrow">
                  ANALYSIS COMPLETE
                </span>

                <h2>{result.project_name}</h2>

                <p>
                  CodePilot AI has completed the analysis of
                  your software project.
                </p>
              </div>

              <div className="grade">
                <span>Quality Score</span>
                <strong>{qualityScore}</strong>
                <small>/100</small>
              </div>
            </div>

            {/* Statistics */}
            <div className="cards">
              <div className="stat-card">
                <span>Quality Score</span>
                <strong>{qualityScore}/100</strong>
                <small>Overall project quality</small>
              </div>

              <div className="stat-card">
                <span>Security Issues</span>
                <strong>{securityIssues}</strong>
                <small>Detected vulnerabilities</small>
              </div>

              <div className="stat-card">
                <span>Total Files</span>
                <strong>{totalFiles}</strong>
                <small>Project files detected</small>
              </div>

              <div className="stat-card">
                <span>Functions</span>
                <strong>{functions}</strong>
                <small>Functions analyzed</small>
              </div>
            </div>

            {/* Project Structure */}
            <div className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    PROJECT OVERVIEW
                  </span>
                  <h3>Project Structure</h3>
                </div>
              </div>

              <div className="details">
                <div>
                  <span>Project Type</span>
                  <strong>
                    {
                      result.analysis.project_structure
                        .project_type
                    }
                  </strong>
                </div>

                <div>
                  <span>Database</span>
                  <strong>
                    {
                      result.analysis.project_structure
                        .database
                    }
                  </strong>
                </div>

                <div>
                  <span>Health Score</span>
                  <strong>
                    {
                      result.analysis.project_structure
                        .health_score
                    }
                    /100
                  </strong>
                </div>

                <div>
                  <span>Grade</span>
                  <strong>
                    {
                      result.analysis.project_structure
                        .grade
                    }
                  </strong>
                </div>
              </div>

              <div className="subsection">
                <span>Languages</span>

                <div className="tags">
                  {result.analysis.project_structure.languages.map(
                    (language, index) => (
                      <span key={index}>{language}</span>
                    )
                  )}
                </div>
              </div>

              <div className="subsection">
                <span>Frameworks</span>

                <div className="tags">
                  {result.analysis.project_structure.frameworks
                    .length > 0 ? (
                    result.analysis.project_structure.frameworks.map(
                      (framework, index) => (
                        <span key={index}>
                          {framework}
                        </span>
                      )
                    )
                  ) : (
                    <span>No frameworks detected</span>
                  )}
                </div>
              </div>
            </div>

            {/* Code Analysis */}
            <div className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    STATIC ANALYSIS
                  </span>
                  <h3>Code Analysis</h3>
                </div>
              </div>

              <div className="analysis-grid">
                <div>
                  <strong>
                    {
                      result.analysis.code_analysis
                        .files_analyzed
                    }
                  </strong>
                  <span>Files Analyzed</span>
                </div>

                <div>
                  <strong>
                    {
                      result.analysis.code_analysis
                        .functions
                    }
                  </strong>
                  <span>Functions</span>
                </div>

                <div>
                  <strong>
                    {
                      result.analysis.code_analysis.classes
                    }
                  </strong>
                  <span>Classes</span>
                </div>

                <div>
                  <strong>{totalFiles}</strong>
                  <span>Total Files</span>
                </div>
              </div>
            </div>

            {/* Security */}
            <div className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow security-label">
                    SECURITY SCAN
                  </span>
                  <h3>Security Findings</h3>
                </div>

                <div
                  className={
                    securityIssues === 0
                      ? "security-count safe"
                      : "security-count danger"
                  }
                >
                  {securityIssues} Issue
                  {securityIssues !== 1 ? "s" : ""}
                </div>
              </div>

              {result.analysis.security.issues.length ===
              0 ? (
                <div className="success">
                  No security vulnerabilities detected.
                </div>
              ) : (
                <div className="security-list">
                  {result.analysis.security.issues.map(
                    (issue, index) => (
                      <div
                        className="security-issue"
                        key={index}
                      >
                        <div>
                          <div className="issue-top">
                            <span className="severity">
                              {issue.severity}
                            </span>

                            <strong>
                              {issue.issue}
                            </strong>
                          </div>

                          <p>
                            Sensitive or potentially
                            dangerous information was
                            detected in the project.
                          </p>

                          <small>
                            {issue.file} — Line{" "}
                            {issue.line}
                          </small>
                        </div>
                      </div>
                    )
                  )}
                </div>
              )}
            </div>

            {/* Recommendations */}
            <div className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    ENGINEERING GUIDANCE
                  </span>
                  <h3>Recommendations</h3>
                </div>
              </div>

              <ul className="recommendations">
                {result.analysis.recommendations.map(
                  (recommendation, index) => (
                    <li key={index}>
                      <span className="recommendation-number">
                        {index + 1}
                      </span>

                      <span>{recommendation}</span>
                    </li>
                  )
                )}
              </ul>
            </div>

            {/* Gemini AI */}
            <div className="panel ai-panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow ai-label">
                    GEMINI AI
                  </span>
                  <h3>Technical Assessment</h3>
                </div>

                <span className="ai-badge">
                  AI POWERED
                </span>
              </div>

              <div className="ai-analysis">
                {result.analysis.ai_analysis}
              </div>
            </div>

            {/* Report */}
            <div className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    GENERATED OUTPUT
                  </span>
                  <h3>CodePilot AI Report</h3>
                </div>
              </div>

              <pre className="report">
                {result.report}
              </pre>
            </div>
          </section>
        )}
      </main>

      <footer>
        <p>
          CodePilot AI • AI-Powered Software Engineering
          Platform
        </p>
      </footer>
    </div>
  );
}

export default App;
