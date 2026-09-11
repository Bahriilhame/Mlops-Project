import { Activity, HeartHandshake, Check } from 'lucide-react';
export default function ClusterProfile({ profile }) {
  const Icon = profile.id === 0 ? Activity : HeartHandshake;
  return <article className={'profile-card ' + (profile.id === 0 ? 'engaged' : 'attention')}>
    <div className="flex items-center justify-between"><span className="cluster-badge">Cluster {profile.id}</span><Icon size={23}/></div>
    <h3>{profile.name}</h3><p>{profile.description}</p><ul>{profile.traits.map(trait => <li key={trait}><Check size={15}/><span>{trait}</span></li>)}</ul>
  </article>;
}

