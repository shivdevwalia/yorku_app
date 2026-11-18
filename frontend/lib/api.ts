export type { Requirement, Course, Program, Graph, Meta } from './types';

export async function api<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch('/api/v1/' + path, { signal, cache: 'no-store' });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.error || 'Catalogue API unavailable (' + response.status + '). Start Python on port 8000.');
  }
  return response.json();
}
