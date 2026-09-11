import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { formatNumber } from '../data/profiles';
const metrics = [
  ['silhouette_score', 'Silhouette Score', 'Higher is better', 4, ArrowUpRight],
  ['davies_bouldin_score', 'Davies–Bouldin Score', 'Lower is better', 4, ArrowDownRight],
  ['calinski_harabasz_score', 'Calinski–Harabasz Score', 'Higher is generally better', 2, ArrowUpRight],
];
export default function ModelMetrics({ info }) {
  return <div className="metric-grid">{metrics.map(([key, label, hint, digits, Icon]) => <div className="metric-item" key={key}><span>{label}</span><strong>{formatNumber(info[key], digits)}</strong><small><Icon size={15}/>{info[key] === null ? 'Métrique non disponible' : hint}</small></div>)}</div>;
}

