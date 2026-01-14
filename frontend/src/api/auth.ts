import apiRequest from '../utils/apiClient';

interface UserCredentials {
  email: string;
  password: string;
}

interface UserResponse {
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
