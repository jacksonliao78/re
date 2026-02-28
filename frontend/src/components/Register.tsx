import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import '../App.css';

interface RegisterProps {
  onSwitchToLogin: () => void;
  onContinueWithoutAccount?: () => void;
}

export default function Register({ onSwitchToLogin, onContinueWithoutAccount }: RegisterProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const { register, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match. Please correct and try again.');
      return;
    }

    try {
      await register(email, password);
    } catch (err: any) {
      const msg = err?.message || '';
      if (msg.toLowerCase().includes('already registered') || msg.toLowerCase().includes('email already')) {
        setError('This email is already registered. Try logging in instead.');
      } else if (msg.includes('fetch') || msg.includes('network') || err?.name === 'TypeError') {
        setError('Cannot reach the server. Check your connection and try again.');
      } else {
        setError(msg || 'Registration failed. Please try again.');
      }
    }
  };

  return (
    <div className="auth-container">
      <h2>Register</h2>
      {error && (
        <div className="auth-alert" role="alert">
          <strong>Registration failed</strong>
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
        <div className="form-group">
          <label htmlFor="confirmPassword">Confirm Password:</label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            disabled={isLoading}
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p className="switch-auth">
        Already have an account?{' '}
        <button type="button" onClick={onSwitchToLogin} disabled={isLoading}>
          Login
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
