import { useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Check, LoaderCircle, RotateCcw, ScanLine, AlertCircle } from 'lucide-react';
import { FEATURE_GROUPS, FEATURES, emptyValues, validateValues, toPayload } from '../data/features';
import { PROFILES } from '../data/profiles';
import { predictStudent } from '../services/api';

export default function PredictionForm() {
  const [values, setValues] = useState(emptyValues);
  const [step, setStep] = useState(0);
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const locked = useRef(false);
  const group = FEATURE_GROUPS[step];
  const completed = FEATURES.filter(f => String(values[f.name]).trim() !== '' && !validateValues(values)[f.name]).length;

  function focusError(nextErrors, groupIndex) {
    setStep(groupIndex);
    setErrors(nextErrors);
    const name = FEATURE_GROUPS[groupIndex].fields.find(f => nextErrors[f.name])?.name;
    requestAnimationFrame(() => document.getElementById(name)?.focus());
  }
  function advance() {
    const allErrors = validateValues(values);
    const currentErrors = Object.fromEntries(group.fields.filter(f => allErrors[f.name]).map(f => [f.name, allErrors[f.name]]));
    if (Object.keys(currentErrors).length) return focusError(currentErrors, step);
    setErrors({}); setStep(step + 1);
  }
  async function submit(event) {
    event.preventDefault();
    if (locked.current) return;
    if (step < FEATURE_GROUPS.length - 1) return advance();
    const validation = validateValues(values);
    if (Object.keys(validation).length) {
      setMessage('Complétez les champs signalés avant d’envoyer les données.');
      focusError(validation, FEATURE_GROUPS.findIndex(g => g.fields.some(f => validation[f.name])));
      return;
    }
    locked.current = true; setLoading(true); setMessage(''); setErrors({}); setResult(null);
    try { setResult(await predictStudent(toPayload(values))); }
    catch (error) {
      setMessage(error.message);
      const fieldErrors = error.fieldErrors || {};
      const index = FEATURE_GROUPS.findIndex(g => g.fields.some(f => fieldErrors[f.name]));
      if (index >= 0) focusError(fieldErrors, index);
    } finally { locked.current = false; setLoading(false); }
  }
  function reset() {
    setValues(emptyValues()); setErrors({}); setMessage(''); setResult(null); setStep(0);
  }
  const profile = result ? PROFILES.find(p => p.id === result.cluster) : null;
  return <div className="prediction-layout">
    <form className="panel prediction-form" noValidate onSubmit={submit}>
      <div className="form-top"><div><span className="eyebrow">LEARNING BEHAVIOR</span><h2>Caractéristiques de l’étudiant</h2></div><span className="pill">{completed} / 34 renseignés</span></div>
      <div className="stepper" aria-label="Sections du formulaire">{FEATURE_GROUPS.map((item, i) => <button type="button" key={item.title} disabled={loading} className={i === step ? 'step active' : 'step'} aria-current={i === step ? 'step' : undefined} onClick={() => setStep(i)}><span>{item.fields.every(f => values[f.name] !== '' && !validateValues(values)[f.name]) ? <Check size={14}/> : i + 1}</span>{item.title}</button>)}</div>
      <div className="form-section-title"><h3>{group.title}</h3><p>{group.description}</p></div>
      {message && <div className="error-banner" role="alert"><AlertCircle size={18}/><span>{message}</span></div>}
      <fieldset disabled={loading} className="fields-grid"><legend className="sr-only">{group.title}</legend>{group.fields.map(field => <div className="field" key={field.name}>
        <label htmlFor={field.name}>{field.label} <span aria-hidden="true">*</span></label>
        <input id={field.name} name={field.name} type="number" inputMode="decimal" min={field.min} max={field.max} step={field.step} required value={values[field.name]}
          placeholder={field.max === 1 ? '0 à 1' : 'Saisir une valeur'}
          aria-invalid={Boolean(errors[field.name])} aria-describedby={errors[field.name] ? field.name + '-error' : field.name + '-hint'}
          onChange={event => {setValues(v => ({ ...v, [field.name]: event.target.value })); setErrors(e => ({ ...e, [field.name]: undefined })); setResult(null);}}/>
        <small id={field.name + '-hint'}>{field.hint || field.name}</small>
        {errors[field.name] && <span className="field-error" id={field.name + '-error'}>{errors[field.name]}</span>}
      </div>)}</fieldset>
      <div className="form-actions"><button className="button secondary" type="button" disabled={loading || step === 0} onClick={() => setStep(step - 1)}><ArrowLeft size={16}/>Précédent</button>
        <span>{step + 1} / 5</span>
        {step < 4 ? <button key="continue" className="button primary" type="button" disabled={loading} onClick={advance}>Continuer<ArrowRight size={16}/></button> : <button key="predict" className="button primary" type="submit" disabled={loading}>{loading ? <LoaderCircle className="loading-icon" size={17}/> : <ScanLine size={17}/>} {loading ? 'Analyse en cours…' : 'Predict Student Cluster'}</button>}
      </div>
    </form>
    <aside className="prediction-aside">
      <section className="panel result-panel" aria-live="polite" aria-busy={loading}><div className="section-label"><ScanLine size={18}/><span>Prediction Result</span></div>
        {loading ? <div className="result-empty"><LoaderCircle className="loading-icon" size={30}/><h3>Analyse du profil…</h3><p>Le modèle traite les caractéristiques saisies.</p></div> : result ? <div className={'prediction-result ' + (result.cluster === 0 ? 'engaged' : 'attention')}><span className="cluster-badge">Cluster {result.cluster}</span><h3>{result.profile}</h3><p>{profile.description}</p><div className="result-success"><Check size={16}/>Profil identifié par KMeans</div></div> : <div className="result-empty"><span className="result-symbol"><ScanLine size={30}/></span><h3>Un profil à découvrir</h3><p>Renseignez les cinq sections pour identifier le segment de cet étudiant.</p></div>}
        <p className="risk-note">« At-Risk » décrit un groupe de comportements. Ce résultat n’est pas une prédiction certaine d’échec.</p>
      </section>
      <section className="panel input-guide"><h3>Avant de commencer</h3><p>Saisissez les valeurs brutes observées. Les 34 champs sont obligatoires ; utilisez 0 uniquement si l’absence d’activité est confirmée.</p><p>Les proportions sont comprises entre 0 et 1. Les notes sont sur 100.</p><button type="button" className="text-button" disabled={loading} onClick={reset}><RotateCcw size={15}/>Réinitialiser le formulaire</button></section>
    </aside>
  </div>;
}

