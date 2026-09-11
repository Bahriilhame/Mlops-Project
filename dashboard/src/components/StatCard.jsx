export default function StatCard({ label, value, caption, icon: Icon, tone = 'teal' }) {
  return <article className={'stat-card ' + tone}><div className="stat-top"><span>{label}</span><span className="stat-icon"><Icon size={19}/></span></div><strong className="stat-value">{value}</strong><p>{caption}</p></article>;
}

