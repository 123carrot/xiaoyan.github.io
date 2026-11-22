"""Build a standalone HTML after updating index.html. Embeds referenced local assets only."""
from pathlib import Path
import base64
import mimetypes
import re
root = Path(__file__).resolve().parent
html = (root / 'index.html').read_text()
for asset in sorted(set(re.findall(r'assets/[A-Za-z0-9_.-]+', html)), key=len, reverse=True):
    data = (root / asset).read_bytes()
    mime = mimetypes.guess_type(asset)[0] or 'application/octet-stream'
    uri = 'data:' + mime + ';base64,' + base64.b64encode(data).decode()
    html = html.replace(asset, uri)
(root / 'Xiaoyan-Gu.html').write_text(html)
print('Built Xiaoyan-Gu.html')
