import { BarChart3, LayoutDashboard, ScanLine, ExternalLink, GraduationCap, Workflow } from 'lucide-react';
import { DAGSTER_URL, MLFLOW_URL } from '../services/api';

export default function Navbar({ page }) {
  return <aside className="sidebar">
    <a className="brand" href="#/"><span className="brand-icon"><BarChart3 size={24}/></span>EduCluster<span className="brand-dot"/></a>
    <div className="workspace-label"><span>ESPACE DE TRAVAIL</span><strong>Learning analytics</strong><small>Master IA · MLOps</small></div>
    <nav aria-label="Navigation principale">
      <a href="#/" className={page === 'dashboard' ? 'nav-link active' : 'nav-link'} aria-current={page === 'dashboard' ? 'page' : undefined}><LayoutDashboard size={19}/>Dashboard</a>
      <a href="#/prediction" className={page === 'prediction' ? 'nav-link active' : 'nav-link'} aria-current={page === 'prediction' ? 'page' : undefined}><ScanLine size={19}/>Prediction</a>
      <a href={MLFLOW_URL} target="_blank" rel="noopener noreferrer" className="nav-link"><BarChart3 size={19}/>MLflow<ExternalLink size={14} className="ml-auto"/></a>
      <a href={DAGSTER_URL} target="_blank" rel="noopener noreferrer" className="nav-link"><Workflow size={19}/>Dagster<ExternalLink size={14} className="ml-auto"/></a>
    </nav>
    <div className="sidebar-bottom"><GraduationCap size={24}/><div><strong>OULAD</strong><span>Profils d’apprenants</span></div></div>
  </aside>;
}

