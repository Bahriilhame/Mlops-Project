const field = (name, label, options = {}) => ({ name, label, min: 0, step: 'any', ...options });
const count = (name, label) => field(name, label, { step: 1 });
const ratio = (name, label) => field(name, label, { max: 1, hint: 'Proportion entre 0 et 1.' });
const score = (name, label) => field(name, label, { max: 100, hint: 'Note entre 0 et 100.' });
const delay = (name, label) => field(name, label, { min: undefined, hint: 'En jours. Une valeur négative indique une remise anticipée.' });

export const FEATURE_GROUPS = [
  { title: 'Engagement', description: 'La présence et les interactions sur la plateforme.', fields: [
    count('total_vle_interactions', 'Total VLE interactions'),
    count('total_clicks', 'Total clicks'),
    count('active_days', 'Active days'),
    count('active_weeks', 'Active weeks'),
    count('activity_span_days', 'Activity span (days)'),
    count('unique_resource_visits', 'Unique resource visits'),
  ] },
  { title: 'Daily Activity', description: 'Le rythme quotidien de consultation.', fields: [
    field('avg_daily_clicks', 'Average daily clicks'),
    field('median_daily_clicks', 'Median daily clicks'),
    field('max_daily_clicks', 'Maximum daily clicks'),
    field('clicks_std', 'Clicks standard deviation'),
    field('avg_clicks_per_event', 'Average clicks per event'),
  ] },
  { title: 'Resource Usage', description: 'Les ressources consultées et leur part dans l’activité.', fields: [
    count('clicks_content', 'Content clicks'), count('clicks_forum', 'Forum clicks'),
    count('clicks_quiz', 'Quiz clicks'), count('clicks_wiki', 'Wiki clicks'),
    count('clicks_other', 'Other clicks'), ratio('content_ratio', 'Content ratio'),
    ratio('forum_ratio', 'Forum ratio'), ratio('quiz_ratio', 'Quiz ratio'),
    ratio('wiki_ratio', 'Wiki ratio'), ratio('other_ratio', 'Other ratio'),
  ] },
  { title: 'Assessments', description: 'La participation aux évaluations et les notes obtenues.', fields: [
    count('assessment_count', 'Assessment count'),
    count('expected_assessment_count', 'Expected assessment count'),
    ratio('submission_rate', 'Submission rate'),
    score('avg_assessment_score', 'Average assessment score'),
    score('min_assessment_score', 'Minimum assessment score'),
    score('max_assessment_score', 'Maximum assessment score'),
    field('assessment_score_std', 'Assessment score standard deviation'),
  ] },
  { title: 'Submissions', description: 'La ponctualité et les délais de remise.', fields: [
    count('late_submission_count', 'Late submission count'),
    ratio('late_submission_rate', 'Late submission rate'),
    delay('avg_submission_delay', 'Average submission delay'),
    delay('median_submission_delay', 'Median submission delay'),
    delay('max_submission_delay', 'Maximum submission delay'),
    ratio('on_time_submission_rate', 'On-time submission rate'),
  ] },
];

export const FEATURES = FEATURE_GROUPS.flatMap(group => group.fields);
export const emptyValues = () => Object.fromEntries(FEATURES.map(({ name }) => [name, '']));

export function validateValues(values) {
  const errors = {};
  for (const field of FEATURES) {
    const raw = values[field.name];
    if (raw === undefined || raw === null || String(raw).trim() === '') {
      errors[field.name] = 'Ce champ est obligatoire.';
      continue;
    }
    const n = Number(raw);
    if (!Number.isFinite(n)) errors[field.name] = 'Saisissez un nombre valide.';
    else if (field.min !== undefined && n < field.min) errors[field.name] = `Minimum : ${field.min}.`;
    else if (field.max !== undefined && n > field.max) errors[field.name] = `Maximum : ${field.max}.`;
    else if (field.step === 1 && !Number.isInteger(n)) errors[field.name] = 'Saisissez un nombre entier.';
  }
  return errors;
}

export function toPayload(values) {
  const errors = validateValues(values);
  if (Object.keys(errors).length) throw new Error('Vérifiez les 34 caractéristiques avant la prédiction.');
  return Object.fromEntries(FEATURES.map(({ name }) => [name, Number(values[name])]));
}

