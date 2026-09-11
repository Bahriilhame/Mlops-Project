import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { PROFILES, formatNumber } from '../data/profiles';

export default function ClusterDistribution({ statistics }) {
  const slices = PROFILES.map(profile => ({ ...profile, value: statistics.clusters[profile.id].count, percentage: statistics.clusters[profile.id].percentage }));
  if (!statistics.total_students) return <div className="empty-state">Aucune inscription segmentée disponible.</div>;
  return <div className="distribution-layout">
    <div className="donut-wrap" role="img" aria-label={slices.map(s => `Cluster ${s.id} : ${s.percentage} %`).join('. ')}>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart><Pie data={slices} dataKey="value" nameKey="shortName" innerRadius={78} outerRadius={103} paddingAngle={3} stroke="none" startAngle={90} endAngle={-270} isAnimationActive={false}>
          {slices.map(slice => <Cell key={slice.id} fill={slice.color}/>)}
        </Pie><Tooltip formatter={(value) => formatNumber(value)} contentStyle={{ borderRadius: 12, border: '1px solid #e2e8ed' }}/></PieChart>
      </ResponsiveContainer>
      <div className="donut-center"><strong>{formatNumber(statistics.total_students)}</strong><span>students</span></div>
    </div>
    <div className="legend">{slices.map(slice => <div className="legend-row" key={slice.id}><div className="legend-title"><span className="color-dot" style={{ background: slice.color }}/><span>Cluster {slice.id}</span><strong>{slice.percentage.toFixed(2)}%</strong></div><p>{slice.shortName}</p><span className="legend-count">{formatNumber(slice.value)} étudiants</span></div>)}</div>
  </div>;
}

