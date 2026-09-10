'use strict';
let data = null, page = 0;
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number = value => value === null || value === undefined || value === '' || !Number.isFinite(Number(value)) ? '—' : Number(value).toLocaleString('fr-FR', {maximumFractionDigits:3});
function table(headers, rows) { return '<div class="table-wrap"><table><thead><tr>' + headers.map(h=>'<th scope="col">'+esc(h)+'</th>').join('') + '</tr></thead><tbody>' + rows.map(r=>'<tr>'+r.map(c=>'<td>'+esc(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>'; }
function filtered(){return data.students.filter(r=>(!$('module').value||r.code_module===$('module').value)&&(!$('session').value||r.code_presentation===$('session').value));}
function renderSegments(){
 const rows=filtered(), counts={}; rows.forEach(r=>{const k=r.cluster||'Non renseigné';counts[k]=(counts[k]||0)+1;});
 $('total').textContent=data.files.find(f=>f.key==='students').exists?number(rows.length):'—';
 $('unique').textContent=rows.length?`${number(new Set(rows.map(r=>r.id_student).filter(Boolean)).size)} étudiants distincts · sélection actuelle`:'Aucune inscription disponible';
 $('clusters').textContent=rows.length?number(Object.keys(counts).length):'—';
 const entries=Object.entries(counts).sort((a,b)=>a[0].localeCompare(b[0]));
 $('distribution').className=rows.length?'':'empty'; $('outcomes').className=rows.length?'':'empty';
 $('distribution').innerHTML=rows.length?entries.map(([k,n])=>`<div class="bar-row"><div class="bar-label"><span>Segment ${esc(k)}</span><strong>${number(n)} · ${number(n/rows.length*100)} %</strong></div><div class="track"><div class="fill" style="width:${n/rows.length*100}%"></div></div></div>`).join(''):'Aucune donnée de segmentation pour cette sélection. Fichier attendu : clustered_students.csv.';
 $('outcomes').innerHTML=rows.length?entries.map(([k,n])=>{const results={};rows.filter(r=>(r.cluster||'Non renseigné')===k).forEach(r=>{let v=r.final_result||'Non renseigné';results[v]=(results[v]||0)+1;});return `<div class="outcome"><strong>Segment ${esc(k)}</strong>${Object.entries(results).map(([name,count])=>`<span>${esc(name)} · ${number(count/n*100)} %</span>`).join('')}</div>`;}).join(''):'Les résultats seront affichés dès que les inscriptions segmentées seront disponibles.';
 const pages=Math.max(1,Math.ceil(rows.length/15)); page=Math.max(0,Math.min(page,pages-1));
 $('students').innerHTML=table(['Étudiant','Module','Session','Segment','Résultat'],rows.slice(page*15,(page+1)*15).map(r=>[r.id_student,r.code_module,r.code_presentation,r.cluster,r.final_result]));
 $('page').textContent=`${page+1} / ${pages}`;$('previous').disabled=page===0;$('next').disabled=page>=pages-1;$('row-count').textContent=`· ${number(rows.length)}`;
}
function render(){
 const available=data.files.filter(f=>f.exists).length;
 $('artifacts').textContent=`${available} / ${data.files.length}`;$('artifact-caption').textContent=`${data.files.length-available} fichiers absents`;
 const metric=(...keys)=>keys.map(k=>data.metrics[k]).find(v=>v!==undefined&&v!==null);
 $('silhouette').textContent=number(metric('silhouette_score','silhouette'));$('db').textContent=number(metric('davies_bouldin_score','davies_bouldin'));$('ch').textContent=number(metric('calinski_harabasz_score','calinski_harabasz'));$('inertia').textContent=number(metric('inertia'));
 for(const [id,key,label] of [['module','code_module','Tous les modules'],['session','code_presentation','Toutes les sessions']]){const selected=$(id).value;$(id).innerHTML=`<option value="">${label}</option>`+[...new Set(data.students.map(r=>r[key]).filter(Boolean))].sort().map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join('');if([...$(id).options].some(o=>o.value===selected))$(id).value=selected;}
 const missing=data.files.filter(f=>!f.exists);
 $('notice').className=missing.length||data.errors.length?'notice':'notice ready';
 $('notice').textContent=data.errors.length?'Erreur de lecture : '+data.errors.join(' · '):missing.length?'Données locales incomplètes. Les fichiers disponibles sont affichés ; les indicateurs manquants restent en attente. Restaurez les artefacts DVC ou exécutez le pipeline pour compléter cette vue.':'Les artefacts attendus sont présents. Les indicateurs proviennent des fichiers locaux.';
 $('inventory').innerHTML='<div class="table-wrap"><table><thead><tr><th scope="col">Artefact</th><th scope="col">Disponibilité</th><th scope="col">Dernière modification</th></tr></thead><tbody>'+data.files.map(f=>`<tr><td>${esc(f.path)}</td><td><span class="badge ${f.exists?'':'missing'}">${f.exists?'Présent':'Absent'}</span></td><td>${f.modified?esc(new Date(f.modified).toLocaleString('fr-FR')):'—'}</td></tr>`).join('')+'</tbody></table></div>';
 if(data.comparison.length){$('comparison').className='';$('comparison').innerHTML=table(['Algorithme','Clusters','Silhouette','Davies–Bouldin','Calinski–Harabasz','Durée (s)'],data.comparison.map(r=>[r.model,number(r.n_clusters),number(r.silhouette),number(r.davies_bouldin),number(r.calinski_harabasz),number(r.time_seconds)]));}else{$('comparison').className='empty compact';$('comparison').textContent='Aucune comparaison disponible. Fichier attendu : clustering_comparison.csv.';}
 $('updated').textContent='Lecture du '+new Date(data.updated).toLocaleString('fr-FR');renderSegments();
}
async function refresh(){ $('refresh').disabled=true;try{const response=await fetch('/api/dashboard');if(!response.ok)throw new Error('HTTP '+response.status);data=await response.json();render();}catch(error){$('notice').className='notice';$('notice').textContent='Lecture impossible. Vérifiez le serveur local puis actualisez. '+(data?'Les valeurs affichées correspondent à la dernière lecture réussie. ':'')+error.message;}finally{$('refresh').disabled=false;}}
$('refresh').addEventListener('click',refresh);['module','session'].forEach(id=>$(id).addEventListener('change',()=>{page=0;renderSegments();}));$('previous').addEventListener('click',()=>{page--;renderSegments();});$('next').addEventListener('click',()=>{page++;renderSegments();});document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>{document.querySelectorAll('nav a').forEach(x=>x.classList.remove('active'));a.classList.add('active');}));refresh();
