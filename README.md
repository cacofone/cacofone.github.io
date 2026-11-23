# cacofone.github.io

Website for [Cacofone](https://cacofone.com), served by GitHub Pages from `main` / root.

- `/` home page listing the apps
- `/streamer/` Cacofone Streamer (plus `/streamer/privacy/`)
- `assets/logo.svg` lyre logo (placeholder), `assets/favicon.svg`, `assets/style.css`

Built by Jekyll on GitHub Pages (no plugins, no theme). The shared page shell lives in `_layouts/default.html`, `_includes/header.html` and `_includes/footer.html`; each page is HTML with a small front matter block (`title`, `description`, optional `lang`, `noindex`, `hide_header`, `nav`).

Preview locally with `bundle install && bundle exec jekyll serve` and open http://localhost:4000.
