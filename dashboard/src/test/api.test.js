import { describe, it, expect, vi } from 'vitest';
import { FEATURES, FEATURE_GROUPS, emptyValues, toPayload, validateValues } from '../data/features';
import { predictStudent, getStatistics, getModelInfo } from '../services/api';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const valid = () => Object.fromEntries(FEATURES.map(f => [f.name, 0]));
describe('FastAPI contract', () => {
  it('matches exactly the 34 backend features in order', () => {
    const backend = readFileSync(resolve(process.cwd(), '../api/main.py'), 'utf8');
    const names = [...backend.match(/FEATURES = \[([\s\S]*?)\]/)[1].matchAll(/"([^"]+)"/g)].map(m => m[1]);
    expect(FEATURES.map(f => f.name)).toEqual(names);
    expect(new Set(names).size).toBe(34);
    expect(FEATURE_GROUPS.map(g => g.fields.length)).toEqual([6, 5, 10, 7, 6]);
  });
  it('rejects missing, nonfinite, out-of-range and noninteger values', () => {
    expect(Object.keys(validateValues(emptyValues()))).toHaveLength(34);
    const values = { ...valid(), content_ratio: 1.1, total_clicks: 0.5, avg_assessment_score: 101, active_days: Infinity };
    expect(Object.keys(validateValues(values))).toHaveLength(4);
    expect(() => toPayload({ ...valid(), active_days: '' })).toThrow();
  });
  it('keeps negative submission delays and sends only numeric feature keys', async () => {
    const fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ cluster: 0, profile: 'Active / Engaged Learner' }) });
    vi.stubGlobal('fetch', fetch);
    await predictStudent({ ...valid(), avg_submission_delay: '-4', extra: 'discard' });
    const [url, options] = fetch.mock.calls[0];
    expect(url).toMatch(/\/predict$/);expect(options.method).toBe('POST');
    const body = JSON.parse(options.body);
    expect(Object.keys(body)).toEqual(FEATURES.map(f => f.name));
    expect(body.avg_submission_delay).toBe(-4);
    expect(Object.values(body).every(v => typeof v === 'number')).toBe(true);
  });
  it('handles inaccessible API', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
    await expect(predictStudent(valid())).rejects.toThrow('API inaccessible');
  });
  it('preserves FastAPI field validation errors', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 422, json: async () => ({ detail: [{ loc: ['body', 'active_days'], msg: 'Required' }] }) }));
    await expect(predictStudent(valid())).rejects.toMatchObject({ fieldErrors: { active_days: 'Required' } });
  });
  it('rejects unexpected prediction responses', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({ cluster: 8 }) }));
    await expect(predictStudent(valid())).rejects.toThrow('inattendue');
  });
  it('handles HTTP failures without valid JSON', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 502, json: async () => { throw new Error(); } }));
    await expect(predictStudent(valid())).rejects.toThrow('HTTP 502');
  });
  it('keeps HTTP status when the error body is JSON null', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 503, json: async () => null }));
    await expect(predictStudent(valid())).rejects.toThrow('HTTP 503');
  });
  it('handles a timed out request', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new DOMException('Aborted', 'AbortError')));
    await expect(predictStudent(valid())).rejects.toThrow('délai');
  });
  it('rejects inconsistent dashboard counts and metrics', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({ total_students: 2, clusters: { 0: { count: 1, percentage: 50 }, 1: { count: 2, percentage: 50 } } }) }));
    await expect(getStatistics()).rejects.toThrow('invalides');
    await expect(getModelInfo()).rejects.toThrow('invalides');
  });
});
