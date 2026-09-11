export const PROFILES = [
  {
    id: 0, name: 'Active / Engaged Learner', shortName: 'Engaged Learners', color: '#16877d',
    description: 'Un engagement soutenu dans les activités d’apprentissage.',
    traits: ['Forte activité et interactions nombreuses', 'Présence régulière sur la plateforme', 'Utilisation importante des ressources', 'Implication plus importante dans les évaluations'],
  },
  {
    id: 1, name: 'Low-Engagement / At-Risk Learner', shortName: 'At-Risk Learners', color: '#c79546',
    description: 'Un profil qui peut nécessiter davantage d’attention.',
    traits: ['Faible activité et moins d’interactions', 'Participation limitée aux activités', 'Engagement irrégulier', 'Accompagnement potentiellement utile'],
  },
];
export const formatNumber = (n, digits = 0) => n === null || n === undefined ? '—' : new Intl.NumberFormat('en-US', { maximumFractionDigits: digits }).format(n);

