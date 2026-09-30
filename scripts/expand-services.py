"""One-time editorial expansion, preserving the current shared shell and enquiry behavior."""
from pathlib import Path
import re,json,html,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]/'site'
base=(R/'services/residential/index.html').read_text()
header=base.split('<main id="main">')[0]
footer=base.split('</main>',1)[1]
E=html.escape
specs={
'residential':('Residential electrical projects','residential-lighting','Plan renovations, new rooms, outlets and home electrical improvements with a clear room-by-room brief.',[
('Start with how you use the home','Describe the rooms involved and the changes you want: additional outlets, a renovated kitchen, a home office, exterior power or new lighting. Separate current problems from future upgrades. Photographs and an existing floor plan help explain the layout without guessing what is hidden behind finishes.'),
('Coordinate the renovation','Tell the electrician about cabinetry, appliances, heating equipment and planned wall or ceiling work. Record which products have already been selected and which remain undecided. Share the wider renovation sequence so electrical work can be coordinated with framing, drywall and finishing.'),
('Prepare for the assessment','Include the property type, city, occupancy and access arrangements. Any assessment of supply capacity, circuits or equipment suitability belongs with a qualified electrical contractor. Do not remove covers or handle wiring to prepare an enquiry; provide existing records and safely accessible photographs instead.'),
('Compare the complete scope','Ask the quote to identify labour, materials, fixtures, controls, making-good work and the approval or inspection responsibilities for the project. Agree how changes will be recorded. For room-by-room fixture decisions, continue to the residential lighting page.')]),
'commercial':('Commercial electrical projects','commercial-lighting','Organize electrical work for offices, retail units, tenant improvements and managed properties.',[
('Describe the business and building','Explain how the space operates, who occupies it and what is changing. A retail fit-out, office reconfiguration and common-area upgrade have different access and scheduling needs. Include the current plans, landlord requirements and the person responsible for coordinating the work.'),
('Make the equipment scope visible','List proposed equipment and attach available manufacturer information to your eventual contractor enquiry. Identify workstations, displays, lighting zones and other planned electrical loads. Have the project team confirm electrical capacity and design requirements; a floor plan alone cannot establish them.'),
('Plan access and interruptions','Record operating hours, loading arrangements, ceiling access and any restrictions on noise or shutdowns. Identify activities that must continue during the work. Discuss temporary arrangements, notice periods and a practical handover sequence with the responsible contractor and property team.'),
('Compare proposals by responsibility','Separate supply, installation, testing, commissioning, documentation and repairs to finishes. Establish who coordinates other trades and who handles project approvals. Use our commercial lighting page for fixture layouts, controls and occupied-space lighting upgrades.')]),
'solar':('Solar specialist project planning','solar-roof','Prepare a useful brief for rooftop solar, energy goals and a specialist assessment of your property.',[
('Begin with the goal','Explain whether you are exploring solar for a home, business or managed building. Describe your energy goals, future EV charging or equipment plans, and whether storage is part of the discussion. Collect recent energy-use records for the specialist instead of choosing a system size from roof area alone.'),
('Document the property','Provide the address, building type, available roof drawings, roof age if known and photographs taken from a safe location. Note planned roof repairs, neighbouring trees and any ownership or strata considerations. A specialist must assess the roof, shading, electrical connection and site conditions before proposing an installation.'),
('Ask for a complete proposal','Request a clear description of panels, inverter equipment, mounting, monitoring, installation and any proposed storage. Ask who coordinates roofing work, design review and connection approvals. Expected output, assumptions, warranties and exclusions should be written down so competing proposals can be compared on the same basis.'),
('Keep pricing assumptions explicit','Do not treat estimated savings, incentives or export arrangements as guaranteed. Ask the specialist to identify the current programme terms and the assumptions used for your specific property. Sparkys provides planning information and accepts general enquiries; it does not currently offer a booked solar installer or a guaranteed installation date.')]),
'residential-lighting':('Residential lighting planning','residential-lighting','Bring room layouts, daily routines and fixture preferences together before selecting a home lighting package.',[
('Plan by activity','Walk through the rooms and record where you cook, read, work, relax and move between spaces. Identify dark areas, glare or a need for more flexible control. Discuss general room lighting, lighting for specific tasks and accents as separate goals rather than simply adding more fixtures.'),
('Connect fixtures to the room','Share furniture and cabinetry layouts, ceiling heights, finish preferences and any selected fixture information. A pendant over an island, a wall light and a recessed ceiling fixture have different placement considerations. Ask the designer or electrician to review the complete room and product compatibility.'),
('Describe the controls you want','Record which lights should operate together and where convenient controls are needed. Mention dimming, schedules or connected-home preferences early. Have the contractor confirm fixture, driver and control compatibility; a product marked dimmable does not establish compatibility with every control.'),
('Include installation and finishing','Identify existing finished ceilings, access limitations and areas being renovated. Compare quotations for fixture supply, installation, controls, adjustments and repairs to finishes. Agree how the lighting will be demonstrated at handover and how changes to fixture selections affect the scope.')]),
'commercial-lighting':('Commercial lighting planning','commercial-lighting','Prepare office, retail, warehouse and common-area lighting projects around the people and work in the space.',[
('Map the operating zones','Identify desks, meeting rooms, displays, circulation, storage and service areas. Explain where existing lighting is uncomfortable, difficult to maintain or no longer suits the layout. Include hours of operation, daylight conditions and photographs alongside the current plans.'),
('Define the upgrade','State whether the project is a fixture replacement, a redesigned layout or a wider tenant improvement. List existing fixture information where available and mark what you expect to retain. Ask the project designer to establish the required lighting performance and the contractor to confirm equipment and control compatibility.'),
('Coordinate controls and maintenance','Discuss occupancy patterns, scheduling, dimming and the people who will operate the system. Include ceiling access, cleaning and replacement access in the design conversation. Keep emergency or other life-safety lighting requirements in the responsible project team’s review rather than assuming a general fixture upgrade covers them.'),
('Plan the installation sequence','Describe occupied areas, trading hours and restrictions on interruption. Ask proposals to separate fixtures, controls, installation, commissioning and documentation. Any energy or maintenance savings should identify their calculation assumptions. Agree on the operating demonstration and the documentation needed for the property team.')]),
'ev-charging':('EV charging project planning','electrical-projects','Prepare parking, ownership, vehicle and usage details before requesting an electrical assessment.',[
('Describe the parking arrangement','Identify whether the charging point is for a detached home, shared residential parking, staff parking or customers. Include stall locations, ownership, access and expected users. Tell the specialist about future vehicles or additional charging points you may want to plan for.'),
('Collect existing information','Provide available electrical drawings, equipment records and photographs from safely accessible areas. Do not open electrical enclosures. A qualified contractor needs to assess capacity, routing and the proposed equipment before specifying the work or determining whether upgrades are needed.'),
('Discuss use and management','Explain when vehicles are usually parked, how charging access should be managed and whether billing or shared use is part of the project. Include network connectivity and the property manager’s operating needs. Compare equipment, installation and ongoing platform responsibilities separately.'),
('Define the handover','Ask who supplies and installs equipment, coordinates approvals and demonstrates operation. Record maintenance contacts and available documentation. Use the electrical project brief to keep the parking plan, site questions and proposed timing together.')])}
alt={'electrical-projects':'Concept of a home and workspace with rooftop solar, room lighting and driveway EV charging','solar-roof':'Concept of rooftop solar panels on a contemporary house','residential-lighting':'Concept living room and kitchen with pendant, recessed and accent lighting','commercial-lighting':'Concept office with linear lighting, meeting rooms and reception'}
def figure(asset,caption):
 return '<figure class="service-visual"><img src="/images/'+asset+'.jpg" width="1536" height="1024" alt="'+E(alt[asset])+'" fetchpriority="high"><figcaption>'+E(caption)+' <span>AI-generated concept illustration for Sparkys.tv; not a completed project.</span></figcaption></figure>'
def card(slug):
 title,asset,desc,_=specs[slug]
 return '<a class="card visual-card" href="/services/'+slug+'/"><img class="service-thumb" src="/images/'+asset+'.jpg" width="1536" height="1024" alt="'+E(alt[asset])+'" loading="lazy"><div class="card-copy"><h3>'+E(title)+'</h3><p>'+E(desc)+'</p><span>Explore project planning →</span><small>Concept illustration</small></div></a>'
def page(route,title,desc,body,asset):
 url='https://sparkys.tv/'+route+'/'
 h=re.sub(r'<title>.*?</title>','<title>'+E(title)+' | Sparkys.tv</title>',header)
 h=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+E(desc)+'">',h)
 h=re.sub(r'<link rel="canonical" href="[^"]*">','<link rel="canonical" href="'+url+'">',h)
 h=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':url})+'</script>',h,count=1)
 p=R/route/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(h+'<main id="main"><section class="wrap section content"><a class="crumb" href="/services/">Electrical projects /</a><h1>'+E(title)+'</h1>'+figure(asset,desc)+'<p class="lead">'+E(desc)+'</p>'+body+'<div class="notice">Sparkys is preparing its electrical network. General enquiries are welcome; contractor matching and bookings are not yet available.</div><a class="button" href="/contact/">Prepare your project enquiry →</a></section></main>'+footer)
for slug,(title,asset,desc,sections) in specs.items():
 body=''.join('<h2>'+E(h)+'</h2><p>'+E(p)+'</p>' for h,p in sections)
 body+='<h2>Continue planning</h2><p><a href="/guides/electrical-project-brief/">Prepare an electrical project brief</a> · <a href="/guides/compare-electrical-quotes/">Compare electrical quotations</a> · <a href="/services/lighting/">Explore lighting projects</a></p>'
 page('services/'+slug,title,desc,body,asset)
page('services/lighting','Lighting for homes and commercial spaces','Explore residential and commercial lighting, from room-by-room updates to occupied business spaces.','<div class="cards">'+card('residential-lighting')+card('commercial-lighting')+'</div><h2>Start with the space, then the fixtures</h2><p>Describe the activities, existing layout, daylight and controls you want. Bring fixture preferences and access constraints together so the project team can assess the whole lighting scheme.</p>','commercial-lighting')
# Expand service directory and homepage service grid, retaining all other content.
for route in ['services','']:
 p=R/route/'index.html';s=p.read_text();start=s.index('<div class="cards">');end=s.index('</div>',s.index('</a>',start)) if False else 0
 # The cards contain nested identity divs, so match through the last old service card.
 s=re.sub(r'<div class="cards">(?:(?!</section>).)*?href="/services/ev-charging/".*?</a></div>','<div class="cards">'+''.join(card(k) for k in specs)+'</div>',s,count=1,flags=re.S)
 if route=='':s=re.sub(r'<figure>.*?</figure>',figure('electrical-projects','Solar, home lighting, commercial spaces and EV charging are different scopes that benefit from one coordinated project brief.'),s,count=1,flags=re.S)
 else:s=s.replace('</h1>','</h1>'+figure('electrical-projects','Choose a project category to prepare the property details, equipment information and questions for the specialist.'),1)
 p.write_text(s)
# Every current supporting page gets a subject-specific explanatory caption near its heading.
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
root=ET.fromstring((R/'sitemap.xml').read_text());urls=[x.text for x in root.findall('s:url/s:loc',ns)]
for u in urls:
 route=u.removeprefix('https://sparkys.tv/');p=R/route/'index.html';s=p.read_text()
 if '<figure' not in s:
  title=html.unescape(re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1));title=re.sub('<.*?>','',title)
  caption=title+': use the home, workspace, solar and charging examples to identify the scope and information relevant to your enquiry.'
  s=s.replace('</h1>','</h1>'+figure('electrical-projects',caption),1);p.write_text(s)
for slug in ['solar','lighting','residential-lighting','commercial-lighting']:
 u='https://sparkys.tv/services/'+slug+'/'
 if u not in urls:urls.append(u)
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="'+ns['s']+'">'+''.join('<url><loc>'+u+'</loc><lastmod>2026-09-29</lastmod></url>' for u in urls)+'</urlset>')
# Use page imagery in social sharing while retaining the mascot as the Organization logo.
for u in urls:
 p=R/u.removeprefix('https://sparkys.tv/')/'index.html';s=p.read_text();m=re.search(r'<figure.*?<img src="([^"]+)"[^>]*alt="([^"]+)"',s,re.S)
 if m:
  for key in ['og:image','twitter:image']:
   s=re.sub(r'(<meta (?:property|name)="'+key+r'" content=")[^"]*',r'\g<1>https://sparkys.tv'+m[1],s)
  for key in ['og:image:alt','twitter:image:alt']:
   s=re.sub(r'(<meta (?:property|name)="'+key+r'" content=")[^"]*',lambda x:x[1]+m[2],s)
  s=s.replace('name="twitter:card" content="summary"','name="twitter:card" content="summary_large_image"');p.write_text(s)
print('Updated',len(urls),'current pages; 4 new permanent service routes.')
