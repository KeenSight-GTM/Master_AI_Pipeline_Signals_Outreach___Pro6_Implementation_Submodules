#!/usr/bin/env python3
"""Render a dependency-free offline HTML navigator from the review Markdown."""
from pathlib import Path
from markdown_it import MarkdownIt
import html,re,json
R=Path(__file__).resolve().parent
md=MarkdownIt('commonmark', {'html':False}).enable('table')
def render(text):return md.render(text)
def accordion(name, pattern):
    text=(R/name).read_text()
    chunks=re.split(pattern,text,flags=re.M)
    if len(chunks)<3:return render(text)
    result=render(chunks[0])
    for i in range(1,len(chunks),2):
        title=chunks[i];body=chunks[i+1]
        identifier=re.search(r'\b(?:F\d{2}|J\d{2})\b',title)
        anchor=f'{name.split(".")[0].lower()}-{identifier.group()}' if identifier else f'{name}-{i}'
        result+=f'<details id="{anchor}"><summary>{html.escape(title)}</summary><div class="card">{render(body)}</div></details>'
    return result
sections=[
 ('start','How to use this review',render((R/'README.md').read_text())),
 ('features','Feature map',render((R/'FEATURE_MAP.md').read_text())),
 ('journeys','19 user journeys',accordion('USER_JOURNEYS.md',r'^### (J\d{2}[^\n]*)\n')),
 ('stages','27 implementation stages',accordion('UPDATED_STAGE_WALKTHROUGHS.md',r'^## (F\d{2}[^\n]*)\n')),
 ('findings','Findings and repair decisions',accordion('AUDIT.md',r'^### (F\d{2}[^\n]*)\n')),
 ('modules','All module and submodule owners',render((R/'SUBMODULE_TRACEABILITY.md').read_text())),
]
nav=''.join(f'<a href="#{key}">{html.escape(title)}</a>' for key,title,_ in sections)
body=''.join(f'<section id="{key}"><div class="section-title"><span>{i:02d}</span><h2>{html.escape(title)}</h2></div>{content}</section>' for i,(key,title,content) in enumerate(sections,1))
css='''
:root { --ink:#16283b; --muted:#506578; --line:#d8e1e8; --paper:#ffffff; --canvas:#eef2f6; --accent:#16626b; }
* {box-sizing:border-box;} html{scroll-behavior:smooth;} body{margin:0;font:16px/1.65 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--canvas);}
header{background:#172d42;color:white;padding:44px max(24px,calc((100% - 1160px)/2));}
header .kicker{font-size:12px;letter-spacing:.16em;font-weight:700;text-transform:uppercase;color:#a7d5da;}header h1{font-size:36px;line-height:1.16;max-width:850px;margin:12px 0 16px;}header p{max-width:890px;color:#d2e0eb;}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px;}.stat{border:1px solid #507084;border-radius:6px;padding:10px 16px;}.stat strong{font-size:22px;display:block;}.stat span{font-size:12px;color:#d2e0eb;}
nav{position:sticky;top:0;z-index:10;background:white;border-bottom:1px solid var(--line);padding:12px 20px;display:flex;justify-content:center;flex-wrap:wrap;gap:8px 18px;}nav a{font-size:13px;font-weight:650;text-decoration:none;color:var(--accent);}
main{max-width:1220px;margin:30px auto;padding:0 20px;}section{scroll-margin-top:95px;background:var(--paper);border:1px solid var(--line);border-radius:10px;margin:0 0 32px;padding:30px;overflow:hidden;}.section-title{display:flex;align-items:center;gap:14px;border-bottom:2px solid var(--line);padding-bottom:15px;margin-bottom:25px;}.section-title span{font-size:22px;font-weight:700;color:var(--accent);}.section-title h2{margin:0;font-size:25px;}
h1,h2,h3,h4{line-height:1.3;}section h1{font-size:27px;}h2{font-size:23px;margin-top:32px;}h3{font-size:20px;margin-top:26px;}a{color:#145f7a;}p{max-width:1000px;}
table{border-collapse:collapse;display:block;overflow-x:auto;margin:20px 0;font-size:14px;line-height:1.55;}th,td{text-align:left;vertical-align:top;border:1px solid var(--line);padding:11px 13px;min-width:100px;}th{background:#e9f0f4;font-weight:700;}tr:nth-child(even) td{background:#f7f9fb;}
code{font:13px/1.6 ui-monospace,SFMono-Regular,Consolas,monospace;background:#edf2f6;padding:2px 4px;border-radius:3px;overflow-wrap:anywhere;}pre{background:#122638;color:#e9f2f9;padding:19px;border-radius:6px;overflow:auto;}pre code{background:transparent;padding:0;color:inherit;white-space:pre;overflow-wrap:normal;}
details{border:1px solid var(--line);border-radius:7px;margin:14px 0;scroll-margin-top:105px;}summary{cursor:pointer;font-size:16px;font-weight:700;padding:17px 20px;background:#f4f8fa;}details[open] summary{border-bottom:1px solid var(--line);background:#eaf3f4;}.card{padding:8px 23px 20px;}.card>p:first-child{color:var(--muted);}blockquote{margin:20px 0;border-left:4px solid var(--accent);padding:1px 20px;background:#f4f8fa;}footer{max-width:1180px;margin:0 auto;padding:0 20px 35px;color:var(--muted);font-size:13px;}li{margin:5px 0;}
@media(max-width:700px){header h1{font-size:28px;}main{padding:0 10px;}section{padding:20px 14px;}nav{position:static;justify-content:flex-start;}section,details{scroll-margin-top:10px;}.card{padding:8px 13px 16px;}}
@media print{body{background:white;font-size:11pt;}nav,.stats{display:none;}header{background:white;color:black;padding:0 0 20px;}header p,header .kicker{color:black;}main{padding:0;margin:0;max-width:none;}section{border:none;padding:0;page-break-before:always;}details{break-inside:avoid;}details:not([open])>.card{display:block!important;}summary{background:white!important;}table{font-size:9pt;}pre{white-space:pre-wrap;}a{color:inherit;text-decoration:none;}}
'''
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KeenSight — features, journeys and iteration 2 audit</title><style>{css}</style></head><body>
<header><div class="kicker">KeenSight / implementation review / 15 September 2026</div><h1>Feature map, user journeys<br>and submodule audit</h1><p>Start with the user’s goal. Follow its exact inputs, commands, evidence and failure states. Then inspect the owning submodule and the regression case that must pass before release.</p><p><strong>Read-only audit:</strong> runtime sources remain unchanged. Local fixture success is not a live system or provider test.</p><div class="stats"><div class="stat"><strong>36</strong><span>feature cards</span></div><div class="stat"><strong>19</strong><span>user journeys</span></div><div class="stat"><strong>27</strong><span>stage walkthroughs</span></div><div class="stat"><strong>8 / 20</strong><span>tested journeys / subprocesses</span></div><div class="stat"><strong>15 + 1</strong><span>findings + policy decision</span></div></div></header>
<nav aria-label="Review sections">{nav}</nav><main>{body}</main><footer>Self-contained document. No external assets, analytics, forms, provider calls or sender. The downloadable package includes numbered source excerpts, unchanged baseline source, failing safety expectations and actual invocation logs.</footer></body></html>'''
# Links to package files are useful when unpacked; all navigation/content remains offline.
(R/'REVIEW_NAVIGATOR.html').write_text(page,encoding='utf-8')
print('HTML bytes',len(page.encode()),'collapsible cards',page.count('<details'))
