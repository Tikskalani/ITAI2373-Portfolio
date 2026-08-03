async function post(url, body){
  const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
  return r.json();
}
async function analyze(){
  const text = document.getElementById('article').value;
  const out = document.getElementById('analyzeOut'); out.textContent = 'Analyzing...';
  const r = await post('/analyze', {text});
  if(r.error){ out.textContent = r.error; return; }
  const c = r.classification;
  const ents = (r.entities||[]).map(e=>e[0]+' ('+e[1]+')').join(', ') || 'none';
  out.innerHTML = '<b>Category:</b> '+c.category+' (confidence '+c.confidence+')'+(c.note?' &mdash; <i>'+c.note+'</i>':'')+'<br>'+
    '<b>Sentiment:</b> '+r.sentiment.label+' ('+r.sentiment.compound+'), emotion '+r.sentiment.emotion+'<br>'+
    '<b>Entities:</b> '+ents+'<br>'+
    '<b>Key terms:</b> '+((c.key_terms||[]).join(', ')||'-')+'<br>'+
    '<b>Summary:</b> '+r.summary;
}
async function ask(){
  const query = document.getElementById('query').value;
  const article = document.getElementById('article').value;
  const out = document.getElementById('queryOut'); out.textContent = 'Thinking...';
  const r = await post('/query', {query, article});
  out.innerHTML = '<b>Intent:</b> '+r.intent+'<br>'+String(r.response||'').replace(/\n/g,'<br>');
}
async function similar(){
  const query = document.getElementById('simq').value;
  const out = document.getElementById('simOut'); out.textContent = 'Searching...';
  const r = await post('/similar', {query});
  out.innerHTML = (r.results||[]).map(h=>'<b>['+h.category+']</b> (score '+h.score+') '+h.snippet+'...').join('<br>');
}
