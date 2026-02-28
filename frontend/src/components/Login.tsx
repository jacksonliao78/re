import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import '../App.css';

interface LoginProps {
  onSwitchToRegister: () => void;
  onContinueWithoutAccount?: () => void;
}

export default function Login({ onSwitchToRegister, onContinueWithoutAccount }: LoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const { login, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await login(email, password);
    } catch (err: any) {
      const msg = err?.message || '';
      if (msg.toLowerCase().includes('incorrect') || msg.toLowerCase().includes('email or password')) {
        setError('No account found with this email, or the password is incorrect. Try again or register below.');
      } else if (msg.includes('fetch') || msg.includes('network') || err?.name === 'TypeError') {
        setError('Cannot reach the server. Check your connection and try again.');
      } else {
        setError(msg || 'Login failed. Please try again.');
      }
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      {error && (
        <div className="auth-alert" role="alert">
          <strong>Login failed</strong>
          <p>{error}</p>
        </div>
      )}
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={isLoading}
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={isLoading}
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p className="switch-auth">
        Don't have an account?{' '}
        <button type="button" onClick={onSwitchToRegister} disabled={isLoading}>
          Register
        </button>
      </p>
      {onContinueWithoutAccount && (
        <p className="switch-auth" style={{ marginTop: "0.75rem" }}>
          <button type="button" onClick={onContinueWithoutAccount} disabled={isLoading} className="link-button">
            Continue without account
          </button>
        </p>
      )}
    </div>
  );
}
