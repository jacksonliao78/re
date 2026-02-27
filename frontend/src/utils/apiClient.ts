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
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    const detail = errorData.detail;
    const message = typeof detail === 'string'
      ? detail
      : Array.isArray(detail)
        ? detail.map((x: { msg?: string }) => x.msg || String(x)).join('. ')
        : errorData.message || 'Request failed';
    throw new Error(message || 'Request failed');
  }

  return response.json();
}

export default apiRequest;
