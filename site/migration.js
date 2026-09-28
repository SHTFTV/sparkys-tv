document.addEventListener('DOMContentLoaded',()=>{
 document.querySelectorAll('.sparkys-enquiry').forEach(form=>form.addEventListener('submit',event=>{
  event.preventDefault();
  if(!form.reportValidity())return;
  const fields=Array.from(form.querySelectorAll('input:not([type=hidden]),textarea,select')).filter(el=>el.name&&(!['checkbox','radio'].includes(el.type)||el.checked));
  const body=fields.map(el=>(el.getAttribute('aria-label')||el.placeholder||el.name)+': '+el.value).join('\n\n');
  window.location.href='mailto:build@buildershaus.com?subject='+encodeURIComponent('Sparkys.tv enquiry')+'&body='+encodeURIComponent(body);
 }));
 const results=document.getElementById('search-results');
 if(results){const query=new URLSearchParams(location.search).get('s')||'';document.getElementById('site-query').value=query;
 fetch('/search-index.json').then(r=>{if(!r.ok)throw Error();return r.json()}).then(pages=>{results.textContent='';const terms=query.toLowerCase().trim().split(/\s+/).filter(Boolean);const matches=terms.length?pages.filter(p=>terms.every(t=>(p.title+' '+p.text).toLowerCase().includes(t))):[];
 if(!matches.length){results.textContent=query?'No matching pages. Try a different search.':'Enter a phrase to search Sparkys.tv.';return;}
 matches.forEach(page=>{const li=document.createElement('li'),a=document.createElement('a');a.href=page.url;a.textContent=page.title;li.append(a);results.append(li);});}).catch(()=>{results.textContent='Search is unavailable. Please use the navigation or contact us.';});}
});
