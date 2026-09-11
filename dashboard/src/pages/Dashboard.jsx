import { useEffect, useState } from 'react';
import { Users, Activity, HeartHandshake, Layers, RefreshCw, ArrowUpRight, Info, GraduationCap, AlertCircle } from 'lucide-react';
import StatCard from '../components/StatCard';
import ClusterDistribution from '../components/ClusterDistribution';
import ClusterProfile from '../components/ClusterProfile';
import ModelMetrics from '../components/ModelMetrics';
import { getStatistics, getModelInfo } from '../services/api';
import { PROFILES, formatNumber } from '../data/profiles';

function DataError({ message, retry }) {
  return <div className="error-banner" role="alert"><AlertCircle size={18}/><span>{message}</span><button className="text-button" onClick={retry}>Réessayer</button></div>;
}
export default function Dashboard() {
  const [state, setState] = useState({ statistics: null, info: null, errors: {}, loading: true });
  const [revision, setRevision] = useState(0);
  const refresh = () => setRevision(r => r + 1);
  useEffect(() => {
    let active = true;
    setState(previous => ({ ...previous, loading: true, errors: {} }));
    Promise.allSettled([getStatistics(), getModelInfo()]).then(([statistics, info]) => {
      if (!active) return;
      setState({ statistics: statistics.status === 'fulfilled' ? statistics.value : null, info: info.status === 'fulfilled' ? info.value : null,
        errors: { statistics: statistics.status === 'rejected' ? statistics.reason.message : null, info: info.status === 'rejected' ? info.reason.message : null }, loading: false });
    });
    return () => { active = false; };
  }, [revision]);
  const { statistics, info, errors, loading } = state;
  const reference = statistics?.source === 'reference_results' || info?.source === 'reference_results';
  return <>
    <div className="page-heading"><div><p className="eyebrow">OBSERVATOIRE D’APPRENTISSAGE</p><h1>Analyse des parcours d’apprentissage</h1><p>Clustering des profils d’apprenants</p></div><button className="button secondary" onClick={refresh} disabled={loading}><RefreshCw size={16} className={loading ? 'loading-icon' : ''}/>Actualiser</button></div>
    <div className="source-note"><Info size={16}/><span>{loading ? 'Lecture des résultats depuis l’API…' : reference ? 'Résultats de référence du projet · utilisés lorsque les artefacts locaux correspondants sont absents.' : statistics || info ? 'Résultats issus des artefacts locaux du pipeline.' : 'Les résultats seront affichés lorsque l’API sera disponible.'}</span></div>
    {errors.statistics && <DataError message={errors.statistics} retry={refresh}/>}
    <section aria-label="Statistiques du clustering" className="stats-grid" aria-busy={loading}>
      <StatCard label="Total Students" value={loading ? '…' : formatNumber(statistics?.total_students)} caption="Inscriptions analysées · OULAD" icon={Users}/>
      <StatCard label="Engaged Learners" value={loading ? '…' : formatNumber(statistics?.clusters['0'].count)} caption="Cluster 0 · engagement soutenu" icon={Activity}/>
      <StatCard label="At-Risk Learners" value={loading ? '…' : formatNumber(statistics?.clusters['1'].count)} caption="Cluster 1 · attention potentielle" icon={HeartHandshake} tone="amber"/>
      <StatCard label="Clusters" value={loading ? '…' : formatNumber(info?.n_clusters)} caption="Segmentation non supervisée" icon={Layers}/>
    </section>
    <div className="analysis-grid">
      <section className="panel distribution-panel"><div className="panel-heading"><div><p className="eyebrow">01 / DISTRIBUTION</p><h2>Deux profils d’apprentissage</h2></div><span className="pill">KMeans</span></div>{loading ? <div className="empty-state" role="status">Chargement de la répartition…</div> : statistics ? <ClusterDistribution statistics={statistics}/> : <div className="empty-state">Répartition non disponible.</div>}<p className="muted-note">Une lecture des comportements, sans étiquette de réussite ou d’échec.</p></section>
      <section className="insight-panel"><span className="insight-icon"><GraduationCap size={25}/></span><p className="eyebrow">DE L’ANALYSE À L’ACCOMPAGNEMENT</p><h2>Mieux comprendre.<br/>Mieux accompagner.</h2><p>Identifiez le profil d’un apprenant à partir de son activité, de ses ressources et de ses évaluations.</p><a href="#/prediction" className="insight-link">Analyser un profil<ArrowUpRight size={18}/></a><div className="insight-footer"><span>34 caractéristiques</span><span>2 segments</span></div></section>
    </div>
    <section className="profiles-section"><div className="section-heading"><div><p className="eyebrow">02 / PROFILS</p><h2>Les comportements derrière les segments</h2></div></div><div className="profiles-grid">{PROFILES.map(profile => <ClusterProfile key={profile.id} profile={profile}/>)}</div><p className="risk-note"><Info size={15}/>« At-Risk » signale un profil de faible engagement, pas une prédiction certaine d’échec.</p></section>
    <section className="panel"><div className="panel-heading"><div><p className="eyebrow">03 / QUALITÉ DU MODÈLE</p><h2>Model Evaluation</h2></div><span className="pill">Clustering non supervisé</span></div>{loading ? <div className="empty-state compact" role="status">Chargement des métriques…</div> : errors.info ? <DataError message={errors.info} retry={refresh}/> : info && <ModelMetrics info={info}/>}</section>
    <section className="panel about-panel"><div><p className="eyebrow">LE PROJET</p><h2>About the Project</h2></div><dl><div><dt>Dataset</dt><dd>OULAD</dd></div><div><dt>Objective</dt><dd>Student profile clustering</dd></div><div><dt>Algorithm</dt><dd>KMeans · 2 clusters</dd></div><div><dt>Preprocessing</dt><dd>Log transformation + StandardScaler</dd></div><div><dt>Evaluation</dt><dd>Silhouette, Davies–Bouldin, Calinski–Harabasz</dd></div></dl></section>
  </>;
}

