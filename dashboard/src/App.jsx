import { lazy, Suspense, useEffect, useState } from 'react';
import Navbar from './components/Navbar';
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Prediction = lazy(() => import('./pages/Prediction'));
const currentPage = () => window.location.hash === '#/prediction' ? 'prediction' : 'dashboard';
export default function App() {
  const [page, setPage] = useState(currentPage);
  useEffect(() => { const listener = () => { setPage(currentPage()); window.scrollTo(0, 0); }; window.addEventListener('hashchange', listener); return () => window.removeEventListener('hashchange', listener); }, []);
  useEffect(() => { document.title = page === 'prediction' ? 'Prediction · EduCluster' : 'Analyse des parcours d’apprentissage · EduCluster'; }, [page]);
  return <><a href="#main-content" className="skip-link" onClick={event => {event.preventDefault(); document.getElementById('main-content')?.focus();}}>Aller au contenu</a><Navbar page={page}/><div className="main-shell"><header className="topbar"><div>Workspace <span>/</span> EduCluster <span>/</span> <strong>{page === 'dashboard' ? 'Dashboard' : 'Prediction'}</strong></div><span className="topbar-label"><span/>OULAD · Learning analytics</span></header><main id="main-content" tabIndex="-1"><Suspense fallback={<div className="empty-state" role="status">Chargement…</div>}>{page === 'dashboard' ? <Dashboard/> : <Prediction/>}</Suspense></main><footer><span>EduCluster · Analyse des parcours d’apprentissage</span><span>Master IA / MLOps</span></footer></div></>;
}
