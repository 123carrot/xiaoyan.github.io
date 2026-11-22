# Xiaoyan Gu — Academic homepage

Static academic homepage, published at https://123carrot.github.io/xiaoyan.github.io/ through GitHub Pages (`main`, repository root).

## Update

- Edit the biography, interests, and inline CSS in `index.html`.
- Maintain papers and their status, authors, figures, links, and selection in `publications.json`.
- After changing publication data, run `python3 build_publications.py`.
- Paper descriptions and figure captions remain available in metadata but are omitted from the page. Paper/PDF links are rendered as one Paper link.
- `python3 build_single_file.py` creates an optional self-contained HTML for offline use; this generated file is not required for deployment.

## Preview

```sh
python3 -m http.server 8766
```

Research has Selected work / All work tabs; the full view is grouped by research direction. Images can be enlarged. The site has no framework or build dependency.

Human and bot icons are from [Lucide](https://lucide.dev/), licensed under ISC; see `LUCIDE-LICENSE.txt`.
