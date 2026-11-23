"""Edit publications.json, then run python3 build_publications.py."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parent
PAPERS = json.loads((ROOT / 'publications.json').read_text())
STATUS_CLASSES = {'Published': 'published', 'Accepted': 'accepted', 'Under review': 'under-review', 'Preprint': 'preprint', 'In preparation': 'in-preparation'}

ADVISORS = {'Wei Zhang', 'Yifang Wang', 'Wei Chen'}
AUTHOR_URLS = {
    'Wei Zhang': 'https://silverbullete.com/',
    'Yifang Wang': 'https://wangyifang.top/',
    'Wei Chen': 'https://www.cad.zju.edu.cn/home/chenwei/',
    'Haibo Hu': 'https://faculty.cqu.edu.cn/HaiboHu/en/index.htm',
}

def author_html(name):
    text = escape(name)
    url = AUTHOR_URLS.get(name.rstrip('*†‡'))
    if url:
        text = f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener">{text}</a>'
    if name.rstrip('*†‡') in ADVISORS:
        text += '<sup class="advisor-mark" title="My advisor" aria-label="My advisor">‡</sup>'
    return text

def work(p, scope, heading_level=3, show_category=False):
    key = scope + '-' + p['id']
    if p['image']:
        image = escape(p['image'], quote=True)
        caption = escape(p['name'] + ' · ' + p['image_caption'], quote=True)
        figure = f'<button type="button" data-image="{image}" data-caption="{caption}" aria-label="Enlarge {escape(p["name"])} figure"><img src="{image}" alt="{escape(p["image_alt"], quote=True)}" loading="lazy"></button>'
    else:
        figure = '<div class="figure-pending"><strong>Construction figure</strong><span>Awaiting manuscript</span></div>'
    people = p['authors']
    full = ', '.join(author_html(a) for a in people)
    author_row = '<p class="authors">' + full + '.</p>' if people else ''
    status_class = STATUS_CLASSES[p['status']]
    contribution = f'<span class="contribution">{escape(p["contribution"])}</span>' if p['contribution'] else ''
    has_paper = any(label == 'Paper' for label, _ in p['links'])
    visible_links = [('Paper' if label == 'PDF' else label, url) for label, url in p['links'] if not (label == 'PDF' and has_paper)]
    links = ''.join(f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener">{escape(label)}</a>' for label,url in visible_links)
    links = '<div class="work-links">' + links + '</div>' if links else ''
    category = p['research_category']
    if category == 'Digital Humanities and Cultural Reasoning':
        category = 'Digital humanities'
    category_tag = f'<span class="research-tag">{escape(category)}</span>' if show_category else ''
    html = f'''<article class="work" aria-labelledby="{key}-title">
  <figure class="work-figure">{figure}</figure>
  <div class="work-copy"><h{heading_level} id="{key}-title">{escape(p['title'])}</h{heading_level}>
    <div class="work-tags"><span class="venue">{escape(p['venue'])}</span><span class="status status-{status_class}">{escape(p['status'])}</span>{contribution}{category_tag}</div>
    {author_row}
    {links}
  </div>
</article>'''
    return '\n'.join(line.rstrip() for line in html.splitlines())

note = '<p class="publication-note">* Equal contribution &nbsp; · &nbsp; † Corresponding author(s) &nbsp; · &nbsp; ‡ My advisors</p>'
RESEARCH_MODULES = [
    ('people-shaping-ai', 'Human → AI', 'How human intentions, knowledge, and feedback are expressed through interaction to inform the design of AI systems and guide changes in their behavior and capabilities.'),
    ('ai-shaping-people', 'AI → Human', 'How interactions with AI shape human cognition, behavior, and agency, both within and beyond immediate tasks.'),
    ('mutual-augmentation', 'Human ↔ AI', 'How people and AI influence one another within a shared interaction episode or over a sustained period of engagement.'),
    ('digital-humanities', 'Digital Humanities and Cultural Reasoning', 'How can AI support evidence-based interpretation of art and culture?'),
    ('foundational-research', 'Foundations of Reliable Visual Reasoning', 'What visual evidence makes a model’s interpretation trustworthy?'),
    ('early-work', 'Early Work in Software Security', 'Learning structural representations for code vulnerability detection.'),
]
def modules(scope, selected_only=False):
    parts = []
    for slug, category, description in RESEARCH_MODULES:
        papers = [p for p in PAPERS if p['research_category'] == category and (not selected_only or p['selected'])]
        if not papers:
            continue
        items = '\n'.join(work(p, scope, heading_level=4) for p in papers)
        heading_id = f'{scope}-module-{slug}'
        category_html = escape(category)
        for symbol in ('→', '↔'):
            if symbol in category:
                start, end = category.split(f' {symbol} ')
                left_head = '<path d="M7 4 2 9l5 5"/>' if symbol == '↔' else ''
                arrow = f'<svg class="direction-arrow" viewBox="0 0 40 18" aria-hidden="true"><path d="M2 9h35M32 4l5 5-5 5"/>{left_head}</svg>'
                category_html = f'<span>{escape(start)}</span><span class="sr-only"> {symbol} </span>{arrow}<span>{escape(end)}</span>'
        category_html = '<span class="direction-title">' + category_html + '</span>'
        parts.append(f'''<section class="research-module" data-direction="{slug}" aria-labelledby="{heading_id}">
<header class="module-heading"><h3 id="{heading_id}">{category_html}</h3><p>{escape(description)}</p></header>
{items}
</section>''')
    return '\n'.join(parts)

def direction_overview(label):
    rows = ''.join(f'<div class="direction-entry"><dt>{escape(category)}</dt><dd>{escape(description)}</dd></div>' for _, category, description in RESEARCH_MODULES[:3])
    return f'<dl class="direction-overview" aria-label="{escape(label, quote=True)}">{rows}</dl>'

SELECTED_IDS = ['dava', 'artanno', 'tcpsbench']
selected_papers = sorted((p for p in PAPERS if p['selected']), key=lambda p: SELECTED_IDS.index(p['id']) if p['id'] in SELECTED_IDS else len(SELECTED_IDS))
selected = '\n'.join(work(p, 'selected', show_category=True) for p in selected_papers)
all_html = modules('all')
human_icon = (ROOT / 'assets/user-round.svg').read_text().replace('stroke-width="2"', 'stroke-width="1.35"').replace('<svg', '<svg aria-hidden="true"', 1)
ai_icon = (ROOT / 'assets/bot.svg').read_text().replace('stroke-width="2"', 'stroke-width="1.35"').replace('<svg', '<svg aria-hidden="true"', 1)
model = f'''<!-- Icons: Lucide, ISC license; see LUCIDE-LICENSE.txt. -->
<figure class="research-model" aria-labelledby="research-model-caption">
<div class="model-cycle">
  <div class="model-entity model-human" role="img" aria-label="Human"><span class="model-symbol">{human_icon}</span></div>
  <div class="model-exchange">
    <span class="model-flow model-flow-forward">Intentions · Knowledge · Feedback</span>
    <svg class="model-arrows" viewBox="0 0 260 100" aria-hidden="true"><path class="model-forward" d="M4 38 C72 10 188 10 256 38m-9-11 9 11-14-1"/><path class="model-return" d="M256 66 C188 94 72 94 4 66m9 11L4 66l14 1"/></svg>
    <span class="model-center">Interaction</span>
    <span class="model-flow model-flow-return">Assistance · Inspiration · Influence</span>
  </div>
  <div class="model-entity model-ai" role="img" aria-label="AI agent"><span class="model-symbol">{ai_icon}</span></div>
</div>
<figcaption id="research-model-caption">Reciprocal influence through sustained interaction.</figcaption>
</figure>'''
body = f'''<section id="research" class="research" aria-labelledby="research-heading">
<div class="section-head"><h2 id="research-heading">Research</h2></div>
{direction_overview("Research directions")}
{model}
<div class="publication-toolbar"><div class="research-tabs" role="tablist" aria-label="Research works">
<button type="button" role="tab" id="selected-tab" aria-controls="selected-work" aria-selected="true" tabindex="0">Selected work <span>{len(selected_papers)}</span></button>
<button type="button" role="tab" id="all-tab" aria-controls="all-work" aria-selected="false" tabindex="-1">All work <span>{len(PAPERS)}</span></button>
</div><a class="scholar-link" href="https://scholar.google.com/citations?user=epqOK68AAAAJ&amp;hl=en" target="_blank" rel="noopener">Google Scholar ↗</a></div>
<div id="selected-work" class="research-panel selected-work" role="tabpanel" aria-labelledby="selected-tab" tabindex="0">
{direction_overview("Selected work research directions")}
{selected}
{note}
</div>
<div id="all-work" class="research-panel all-work" role="tabpanel" aria-labelledby="all-tab" tabindex="0" hidden>
{all_html}
{note}
</div>
</section>'''
page = (ROOT / 'index.html').read_text()
page, count = re.subn(r'<!-- PUBLICATIONS:START -->.*?<!-- PUBLICATIONS:END -->', '<!-- PUBLICATIONS:START -->\n'+body+'\n<!-- PUBLICATIONS:END -->',page,flags=re.S)
assert count == 1, 'Publication markers missing or duplicated'
(ROOT / 'index.html').write_text(page)
print(f'Built {sum(bool(p["selected"]) for p in PAPERS)} selected works and {len(PAPERS)} total works.')
