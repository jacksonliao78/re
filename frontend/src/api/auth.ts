import apiRequest from '../utils/apiClient';
import type { Resume } from '../types';

interface UserCredentials {
  email: string;
  password: string;
}

export interface UserResponse {
  id: string;
  email: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function register(credentials: UserCredentials): Promise<UserResponse> {
  return apiRequest<UserResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
}

export async function login(credentials: UserCredentials): Promise<TokenResponse> {
  return apiRequest<TokenResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
}

export async function getCurrentUser(token: string): Promise<UserResponse> {
  return apiRequest<UserResponse>('/auth/me', {
    method: 'GET',
    token,
  });
}

export function logout(): void {
  localStorage.removeItem('authToken');
}

// default resume (stored per user; used as "original" when rechoosing a job)
export async function getDefaultResume(token: string): Promise<Resume | null> {
  const res = await fetch('/auth/me/default-resume', {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (res.status === 404) return null;
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to get default resume');
  }
  return res.json();
}

export async function saveDefaultResume(resume: Resume, token: string): Promise<void> {
  await apiRequest('/auth/me/default-resume', {
    method: 'PUT',
    body: JSON.stringify(resume),
    token,
  });
}

// ignored jobs (filtered out of scrape for this user)
export async function getIgnoredJobs(token: string): Promise<string[]> {
  return apiRequest<string[]>('/auth/me/ignored-jobs', { method: 'GET', token });
}

export async function addIgnoredJob(jobId: string, token: string): Promise<void> {
  await apiRequest('/auth/me/ignored-jobs', {
    method: 'POST',
    body: JSON.stringify({ job_id: jobId }),
    token,
  });
}
