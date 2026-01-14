interface ApiRequestOptions extends RequestInit {
  token?: string;
}

async function apiRequest<T>(url: string, options: ApiRequestOptions = {}): Promise<T> {
  const { token, body, headers, ...rest } = options;

  const config: RequestInit = {
    ...rest,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    body,
  };

  if (token) {
    config.headers = {
      ...config.headers,
      'Authorization': `Bearer ${token}`,
    } as HeadersInit;
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(errorData.detail || errorData.message || 'API request failed');
  }

  return response.json();
}

export default apiRequest;
