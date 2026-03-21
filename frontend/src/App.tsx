import { useState, useEffect } from "react";
import { Outlet, NavLink, Link } from "react-router";
import "./App.css";
import Login from "./components/Login";
import Register from "./components/Register";
import { useAuth } from "./contexts/AuthContext";

function App() {
  const { isAuthenticated, isLoading, logout } = useAuth();
  const [showAuthScreen, setShowAuthScreen] = useState(false);
  const [authMode, setAuthMode] = useState<"login" | "register">("login");

  useEffect(() => {
    if (isAuthenticated) setShowAuthScreen(false);
  }, [isAuthenticated]);

  if (isLoading) {
    return (
      <div className="app-root" style={{ justifyContent: "center", alignItems: "center" }}>
        <p>Loading…</p>
      </div>
    );
  }

  if (showAuthScreen && !isAuthenticated) {
    return (
      <div className="app-root">
        {authMode === "login" ? (
          <Login
            onSwitchToRegister={() => setAuthMode("register")}
            onContinueWithoutAccount={() => setShowAuthScreen(false)}
          />
        ) : (
          <Register
            onSwitchToLogin={() => setAuthMode("login")}
            onContinueWithoutAccount={() => setShowAuthScreen(false)}
          />
        )}
      </div>
    );
  }

  return (
    <div className="app-root">
      <header className="app-nav">
        <Link to="/" style={{ textDecoration: "none" }}>
          <h1>get a job</h1>
        </Link>
        <nav className="nav-links">
          <NavLink to="/resume">Resume</NavLink>
          <NavLink to="/tailor">Tailor</NavLink>
        </nav>
        <div className="nav-auth">
          {isAuthenticated ? (
            <button
              type="button"
              onClick={() => {
                logout();
                setShowAuthScreen(true);
              }}
              className="clear-btn"
            >
              Log out
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setShowAuthScreen(true)}
              className="clear-btn"
            >
              Log in
            </button>
          )}
        </div>
      </header>

      <main className="app-main">
        <Outlet context={{ showLogin: () => setShowAuthScreen(true) }} />
      </main>
    </div>
  );
}

export default App;
