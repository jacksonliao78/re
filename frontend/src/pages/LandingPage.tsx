import { Link, useOutletContext } from "react-router";

type AppOutletContext = {
  showLogin: () => void;
};

export default function LandingPage() {
  const { showLogin } = useOutletContext<AppOutletContext>();

  return (
    <div className="landing">
      <section className="landing-hero">
        <h1 className="landing-title font-accent">get a job</h1>
        <p className="landing-subtitle">
          Upload your resume. Find jobs. Tailor with AI.
        </p>
        <Link to="/resume" className="landing-cta">
          Get Started
        </Link>
        <p className="landing-note">
          Accounts are optional but recommended for saving your resume across
          sessions.
        </p>
      </section>

      <section className="landing-features">
        <div className="landing-card">
          <div className="landing-card-icon">📄</div>
          <h3>Upload &amp; Parse</h3>
          <p>Drop a PDF and get a structured resume in seconds.</p>
        </div>
        <div className="landing-card">
          <div className="landing-card-icon">🔍</div>
          <h3>Scrape Jobs</h3>
          <p>Search for real job postings or paste your own description.</p>
        </div>
        <div className="landing-card">
          <div className="landing-card-icon">✨</div>
          <h3>AI Tailoring</h3>
          <p>
            Get targeted suggestions to align your resume with each job.
          </p>
        </div>
      </section>

      <section className="landing-steps" aria-labelledby="landing-steps-heading">
        <h2 id="landing-steps-heading" className="landing-steps-title font-accent">
          How it works
        </h2>

        <div className="landing-step-block">
          <div
            className="landing-step-media"
            aria-label="Screenshot placeholder: upload step"
          >
            <span className="landing-step-media-placeholder">Screenshot</span>
            {/* Replace placeholder with <img src="..." alt="..." /> when ready */}
          </div>
          <div className="landing-step-copy">
            <span className="landing-step-number" aria-hidden="true">
              1
            </span>
            <h3 className="landing-step-heading">Upload</h3>
            <p>
              Drop your PDF resume. Our parser extracts your experience,
              skills, and education into a structured format.
            </p>
          </div>
        </div>

        <div className="landing-step-block landing-step-block--reverse">
          <div
            className="landing-step-media"
            aria-label="Screenshot placeholder: find jobs step"
          >
            <span className="landing-step-media-placeholder">Screenshot</span>
            {/* Replace placeholder with <img src="..." alt="..." /> when ready */}
          </div>
          <div className="landing-step-copy">
            <span className="landing-step-number" aria-hidden="true">
              2
            </span>
            <h3 className="landing-step-heading">Find jobs</h3>
            <p>
              Search real job postings by role, or paste any job description
              directly.
            </p>
          </div>
        </div>

        <div className="landing-step-block">
          <div
            className="landing-step-media"
            aria-label="Screenshot placeholder: tailor step"
          >
            <span className="landing-step-media-placeholder">Screenshot</span>
            {/* Replace placeholder with <img src="..." alt="..." /> when ready */}
          </div>
          <div className="landing-step-copy">
            <span className="landing-step-number" aria-hidden="true">
              3
            </span>
            <h3 className="landing-step-heading">Tailor</h3>
            <p>
              AI compares your resume to the job and suggests targeted
              improvements you can apply in one click.
            </p>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <div className="landing-footer-cta">
          <Link to="/resume" className="landing-cta">
            Get Started
          </Link>
          <p className="landing-footer-login">
            Returning user?{" "}
            <button type="button" className="link-button" onClick={showLogin}>
              Log in
            </button>
          </p>
        </div>
        <div className="landing-footer-divider" />
        <div className="landing-site-footer">
          <a
            className="landing-site-footer-link"
            href="https://github.com/yourusername/your-repo"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>
        </div>
      </footer>
    </div>
  );
}
