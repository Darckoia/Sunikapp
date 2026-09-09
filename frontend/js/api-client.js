export async function api(path, options = {}) {
  const response = await fetch(`/api/v1${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}
