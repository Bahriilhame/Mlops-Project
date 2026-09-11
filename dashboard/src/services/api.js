import { toPayload } from '../data/features';

export const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8002').replace(/\/+$/, '');
const configuredMlflow = import.meta.env.VITE_MLFLOW_URL || 'http://localhost:5001';
export const MLFLOW_URL = /^https?:\/\//i.test(configuredMlflow) ? configuredMlflow : 'http://localhost:5001';

export class ApiError extends Error {
  constructor(message, fieldErrors = {}) {
    super(message);
    this.name = 'ApiError';
    this.fieldErrors = fieldErrors;
  }
}

async function request(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);
  try {
    const response = await fetch(`${API_URL}${path}`, { ...options, signal: controller.signal });
    let body;
    try { body = await response.json(); }
    catch { throw new ApiError(response.ok ? 'Réponse inattendue : un résultat JSON était attendu.' : `Erreur HTTP ${response.status}. Réessayez plus tard.`); }
    if (!response.ok) {
      if (response.status === 422 && Array.isArray(body?.detail)) {
        const fieldErrors = Object.fromEntries(body.detail.map(error => [error.loc?.at(-1), error.msg]));
        throw new ApiError('Les données ont été refusées par l’API. Vérifiez les champs indiqués.', fieldErrors);
      }
      throw new ApiError(typeof body?.detail === 'string' ? `Erreur HTTP ${response.status} : ${body.detail}` : `Erreur HTTP ${response.status}. Réessayez plus tard.`);
    }
    return body;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    if (error.name === 'AbortError') throw new ApiError('Le délai de réponse a été dépassé. Réessayez.');
    throw new ApiError('API inaccessible. Vérifiez qu’elle est démarrée et que VITE_API_URL est configurée.');
  } finally { clearTimeout(timeout); }
}

export async function predictStudent(data) {
  const payload = toPayload(data);
  const result = await request('/predict', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (!result || ![0, 1].includes(result.cluster) || typeof result.profile !== 'string' || !result.profile.trim()) {
    throw new ApiError('Réponse de prédiction inattendue : cluster ou profil manquant.');
  }
  return result;
}

export async function getStatistics() {
  const result = await request('/statistics');
  const clusters = result?.clusters;
  if (!Number.isInteger(result?.total_students) || result.total_students < 0 ||
      !clusters || ![0, 1].every(id => Number.isInteger(clusters[id]?.count) && clusters[id].count >= 0 &&
        Number.isFinite(clusters[id]?.percentage) && clusters[id].percentage >= 0 && clusters[id].percentage <= 100) ||
      clusters[0].count + clusters[1].count !== result.total_students) {
    throw new ApiError('Les statistiques reçues sont incomplètes ou invalides.');
  }
  return result;
}

export async function getModelInfo() {
  const result = await request('/model-info');
  const metrics = ['silhouette_score', 'davies_bouldin_score', 'calinski_harabasz_score'];
  if (!result || result.algorithm !== 'KMeans' || result.n_clusters !== 2 || result.features !== 34 ||
      metrics.some(key => result[key] !== null && !Number.isFinite(result[key]))) {
    throw new ApiError('Les informations du modèle sont incomplètes ou invalides.');
  }
  return result;
}

