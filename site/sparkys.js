document.querySelectorAll('.enquiry').forEach(form=>form.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;const data=new FormData(form);const body=['Name: '+data.get('name'),'Email: '+data.get('email'),'City: '+data.get('city'),'Enquiry: '+data.get('message'),'Consent to reply: '+data.get('consent')].join('\n\n');form.querySelector('.form-status').textContent='Your email app will open. Please review and send the draft. If it does not open, email build@buildershaus.com directly.';location.href='mailto:build@buildershaus.com?subject='+encodeURIComponent(data.get('subject'))+'&body='+encodeURIComponent(body)}));
const results=document.querySelector('#search-results');if(results){const q=new URLSearchParams(location.search).get('s')||'';document.querySelector('#site-query').value=q;fetch('/search-index.json').then(r=>r.json()).then(pages=>{const terms=q.toLowerCase().trim().split(/\s+/).filter(Boolean);const matches=terms.length?pages.filter(p=>terms.every(t=>(p.title+' '+p.text).toLowerCase().includes(t))):[];results.textContent=matches.length?'':q?'No matches found.':'Enter a phrase to search.';for(const p of matches){const li=document.createElement('li'),a=document.createElement('a');a.href=p.url;a.textContent=p.title;li.append(a);results.append(li)}}).catch(()=>results.textContent='Search is unavailable. Please use the navigation.')}

// Site-branded enquiry card; no contractor assignment is implied.
const contactCard=document.querySelector('#sparkys-contact');
if(contactCard){let preference=null;try{preference=sessionStorage.getItem('sparkys-contact-open')}catch{}contactCard.open=preference===null?matchMedia('(min-width: 850px)').matches:preference==='true';contactCard.addEventListener('toggle',()=>{try{sessionStorage.setItem('sparkys-contact-open',String(contactCard.open))}catch{}});contactCard.querySelector('.contact-close').addEventListener('click',()=>{contactCard.open=false;contactCard.querySelector('summary').focus()});}

// A genuinely silent file; reduced-motion/data preferences start with the poster.
const headerVideo=document.querySelector('#sparkys-header-video');
if(headerVideo){
 const toggle=document.querySelector('.header-film-toggle');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const update=()=>{toggle.textContent=headerVideo.paused?'Play header video':'Pause header video';};
 const play=()=>{if(!headerVideo.getAttribute('src'))headerVideo.src=headerVideo.dataset.src;headerVideo.muted=true;headerVideo.play().catch(update);};
 headerVideo.muted=true;
 headerVideo.addEventListener('play',update);headerVideo.addEventListener('pause',update);headerVideo.addEventListener('error',()=>{toggle.hidden=true;});
 toggle.addEventListener('click',()=>headerVideo.paused?play():headerVideo.pause());
 reduced.addEventListener('change',event=>{if(event.matches)headerVideo.pause();});
 if(!reduced.matches&&!navigator.connection?.saveData){const observer=new IntersectionObserver(entries=>{if(entries[0].isIntersecting){play();observer.disconnect();}},{threshold:0.1});observer.observe(headerVideo);}
 update();
}

const journalTrack=document.querySelector('#journal-track');if(journalTrack){document.querySelectorAll('[data-journal-step]').forEach(button=>button.addEventListener('click',()=>journalTrack.scrollBy({left:Number(button.dataset.journalStep)*(journalTrack.querySelector('.journal-card').getBoundingClientRect().width+22),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})));}
const finder=document.querySelector('#contractor-finder');if(finder){finder.addEventListener('submit',event=>{event.preventDefault();const city=finder.elements.city.value.trim();if(!city)return;const trade=finder.elements.trade;const result=document.querySelector('#finder-results');result.replaceChildren();const heading=document.createElement('h2');heading.textContent=trade.options[trade.selectedIndex].text+' in '+city;const text=document.createElement('p');text.textContent='No contractor listings are published for this selection yet. The directory is being populated; this is not a booking or availability confirmation.';const link=document.createElement('a');link.href='/contact/';link.textContent='Tell us about your project →';result.append(heading,text,link);});}
