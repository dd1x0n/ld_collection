import os
import pandas as pd
from flask import Flask, render_template_string, request
from markupsafe import Markup

app = Flask(__name__)

FILM_CSV_CANDIDATES = ['ld_collection.csv', 'LD_collection.csv', 'collection.csv']
GAME_CSV_CANDIDATES = ['games_2026.csv', 'games.csv', 'collection.csv']

BASE_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LD Collection</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f8fc;
      --surface: #ffffff;
      --surface-strong: #f0f6ff;
      --primary: #123962;
      --primary-soft: #d9e7ff;
      --text: #172b4d;
      --muted: #4d6175;
      --border: #c2d0e4;
      --accent: #1565d8;
      --accent-soft: #e5efff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top left, #e8f0ff 0%, var(--bg) 45%);
      color: var(--text);
      line-height: 1.6;
    }
    header {
      padding: 24px 32px 16px;
      background: white;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 10;
    }
    .shell { max-width: 1100px; margin: 0 auto; padding: 20px 24px 40px; }
    .brand {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .brand h1 {
      margin: 0;
      font-size: clamp(1.8rem, 2vw, 2.6rem);
      letter-spacing: -0.04em;
      color: var(--primary);
    }
    .brand p { margin: 6px 0 0; color: var(--muted); max-width: 42rem; }
    nav {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 18px;
    }
    nav a {
      color: var(--primary);
      text-decoration: none;
      padding: 10px 14px;
      border-radius: 999px;
      transition: background 0.2s ease;
    }
    nav a:hover { background: var(--primary-soft); }
    .content {
      margin-top: 24px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 22px;
      padding: 28px;
      box-shadow: 0 18px 60px rgba(15, 23, 42, 0.08);
    }
    .hero {
      display: grid;
      gap: 20px;
      margin-bottom: 28px;
    }
    .hero h2 { margin-top: 0; color: var(--primary); }
    .hero p { margin-bottom: 0; }
    .stats {
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      margin-top: 26px;
    }
    .card {
      padding: 22px;
      border-radius: 18px;
      background: var(--surface-strong);
      border: 1px solid var(--border);
    }
    .card strong { display: block; font-size: 2rem; margin-bottom: 8px; color: var(--primary); }
    .button-row {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 24px;
    }
    button,
    .button-link {
      border: none;
      background: var(--accent);
      color: white;
      padding: 12px 18px;
      border-radius: 999px;
      cursor: pointer;
      font-weight: 600;
      text-decoration: none;
    }
    button:hover,
    .button-link:hover { opacity: 0.95; }
    .notice, .callout {
      margin: 22px 0;
      padding: 18px 20px;
      border-radius: 16px;
      background: #eef4ff;
      border: 1px solid #d4e3ff;
      color: var(--muted);
    }
    .search-form label { font-weight: 600; color: var(--text); }
    .search-form input,
    .search-form select,
    .search-form button {
      width: 100%;
      max-width: 420px;
      display: block;
      margin-top: 10px;
    }
    input, select { border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; background: white; }
    .search-form button { margin-top: 16px; }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 22px;
      font-size: 0.95rem;
    }
    th, td { padding: 12px 14px; border: 1px solid var(--border); text-align: left; }
    th { background: var(--surface-strong); color: var(--primary); }
    tr:nth-child(even) { background: #fbfdff; }
    .table-wrapper { overflow-x: auto; }
    .fallback { color: #334155; }
  </style>
</head>
<body>
  <header>
    <div class="shell brand">
      <div>
        <h1>LD Collection</h1>
        <p>Browse your laserdisc and classic game collections with a polished search interface and clean tables.</p>
      </div>
      <nav>
        <a href="/">Home</a>
        <a href="/films">Films</a>
        <a href="/games">Games</a>
        <a href="/add/film">Add Film</a>
        <a href="/add/game">Add Game</a>
        <a href="/search/films">Search Films</a>
        <a href="/search/games">Search Games</a>
      </nav>
    </div>
  </header>
  <main class="shell">
    <section class="content">
      {{ content|safe }}
    </section>
  </main>
</body>
</html>'''


def detect_csv_type(path):
    try:
        df = pd.read_csv(path, encoding='utf8', nrows=0)
    except Exception:
        return None

    headers = [str(c).strip() for c in df.columns]
    if 'Game' in headers and 'System' in headers:
        return 'game'
    if 'Title' in headers and 'Genre' in headers:
        return 'film'
    return None


def find_csv_path(candidates, expected):
    for candidate in candidates:
        if os.path.isfile(candidate) and detect_csv_type(candidate) == expected:
            return candidate
    return None


def load_films():
    path = find_csv_path(FILM_CSV_CANDIDATES, 'film')
    if not path:
        return None, None

    try:
        df = pd.read_csv(path, encoding='utf8')
    except Exception:
        return None, path

    df.columns = [str(c).strip() for c in df.columns]
    if 'Title' not in df.columns and len(df.columns) >= 1:
        df.rename(columns={df.columns[0]: 'Title'}, inplace=True)
    return df, path


def load_game_file(path):
  try:
    df = pd.read_csv(path, encoding='utf8')
  except Exception:
    return None

  # Preserve all columns; just normalize header strings
  df.columns = [str(c).strip() for c in df.columns]
  # If there are at least two columns but no explicit 'Game' header,
  # keep original headers rather than forcing rename — callers may
  # prefer the CSV's schema.
  return df.copy()


def load_game_file_v2(path):
    """Replacement loader that preserves all CSV columns."""
    try:
        df = pd.read_csv(path, encoding='utf8')
    except Exception:
        return None
    df.columns = [str(c).strip() for c in df.columns]
    return df.copy()


def load_games():
  frames = []
  sources = []
  for candidate in GAME_CSV_CANDIDATES:
    if os.path.isfile(candidate) and detect_csv_type(candidate) == 'game':
      try:
        df = pd.read_csv(candidate, encoding='utf8')
      except Exception:
        continue
      df.columns = [str(c).strip() for c in df.columns]
      frames.append(df)
      sources.append(candidate)
  if not frames:
    return None, None

  result = pd.concat(frames, ignore_index=True, sort=False)
  result.drop_duplicates(inplace=True)
  return result, sources


def get_search_fields(df):
    # Return all columns but prefer some common film columns first for nicer ordering
    preferred = ['Title', 'Genre', 'Release', 'Year', 'Director', 'Rating']
    fields = list(df.columns)
    # Move preferred fields to front if present
    ordered = [f for f in preferred if f in fields]
    ordered += [f for f in fields if f not in ordered]
    return ordered


def render_html(content):
    return render_template_string(BASE_TEMPLATE, content=Markup(content))


def render_collection_table(df, caption=None, base_url='', current_sort=None, current_order='asc'):
  # Build a table with clickable headers that toggle sort order.
  def _col_link(col):
    next_order = 'desc' if (current_sort == col and current_order == 'asc') else 'asc'
    if base_url:
      return f'{base_url}?sort={col}&order={next_order}'
    return f'?sort={col}&order={next_order}'

  html = '<div class="table-wrapper">'
  # Header
  html += '<table class="collection-table">'
  html += '<thead><tr>'
  for col in df.columns:
    indicator = ''
    if current_sort == col:
      indicator = ' ▲' if current_order == 'asc' else ' ▼'
    link = _col_link(col)
    html += f'<th><a href="{link}">{col}{indicator}</a></th>'
  html += '</tr></thead>'
  # Body
  html += '<tbody>'
  for _, row in df.fillna('').iterrows():
    html += '<tr>'
    for col in df.columns:
      cell = str(row[col])
      html += f'<td>{cell}</td>'
    html += '</tr>'
  html += '</tbody></table>'
  html += '</div>'
  if caption:
    html = f'<p>{caption}</p>' + html
  return html


def append_row_to_csv(path, row_dict, columns=None):
    df_row = pd.DataFrame([row_dict])
    write_header = not os.path.isfile(path)
    # If columns provided, ensure ordering
    if columns:
        df_row = df_row.reindex(columns=columns)
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    df_row.to_csv(path, index=False, mode='a' if not write_header else 'w', header=write_header, encoding='utf8')


@app.route('/')
def home():
    films, film_path = load_films()
    games, game_paths = load_games()
    film_count = len(films) if films is not None else 0
    game_count = len(games) if games is not None else 0

    sources = []
    if film_path:
        sources.append(f'<strong>Film source:</strong> {film_path}')
    if game_paths:
        sources.append(f'<strong>Game source(s):</strong> {", ".join(game_paths)}')
    if not sources:
        sources.append('<strong>No CSV sources detected.</strong>')

    content = '<div class="hero">'
    content += '<h2>Your LD and classic game collection dashboard</h2>'
    content += '<p>Quickly browse film and game collections, search titles, and explore your imported CSV data with a more polished experience.</p>'
    content += '<div class="stats">'
    content += f'<div class="card"><strong>{film_count}</strong> films available</div>'
    content += f'<div class="card"><strong>{game_count}</strong> games available</div>'
    content += '</div>'
    content += '<div class="button-row">'
    content += '<a class="button-link" href="/films">Browse Films</a>'
    content += '<a class="button-link" href="/games">Browse Games</a>'
    content += '<a class="button-link" href="/search/films">Search Films</a>'
    content += '<a class="button-link" href="/search/games">Search Games</a>'
    content += '</div>'
    content += '<div class="callout">' + '<br>'.join(sources) + '</div>'
    content += '</div>'
    return render_html(content)


@app.route('/films')
def films():
    df, path = load_films()
    if df is None:
        return render_html('<h2>Film Collection</h2><p class="fallback">No film CSV could be loaded. Check that one of ld_collection.csv, LD_collection.csv, or collection.csv exists with Title and Genre columns.</p>')

    # Sorting
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')
    if sort in df.columns:
        # Attempt numeric conversion for smart sorting
        col_series = pd.to_numeric(df[sort], errors='coerce')
        if col_series.notna().sum() > 0:
            df[sort] = col_series
        df = df.sort_values(by=sort, ascending=(order == 'asc'))

    content = f'<h2>Film Collection</h2><p>Loaded from: <strong>{path}</strong></p>'
    content += render_collection_table(df, base_url='/films', current_sort=sort, current_order=order)
    return render_html(content)


@app.route('/games')
def games():
    df, sources = load_games()
    if df is None:
        return render_html('<h2>Game Collection</h2><p class="fallback">No game CSV could be loaded. Check that games_2026.csv, games.csv, or collection.csv exists with Game and System columns.</p>')

    # Sorting
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')
    if sort in df.columns:
        col_series = pd.to_numeric(df[sort], errors='coerce')
        if col_series.notna().sum() > 0:
            df[sort] = col_series
        df = df.sort_values(by=sort, ascending=(order == 'asc'))

    content = f'<h2>Game Collection</h2><p>Loaded from: <strong>{", ".join(sources)}</strong></p>'
    content += render_collection_table(df, base_url='/games', current_sort=sort, current_order=order)
    return render_html(content)


@app.route('/search/<collection>', methods=['GET', 'POST'])
def search_collection(collection):
    collection = collection.lower()
    if collection not in ('films', 'games'):
        return render_html('<h2>Search</h2><p class="fallback">Collection not found. Use /search/films or /search/games.</p>')

    if collection == 'films':
        df, _ = load_films()
    else:
        df, _ = load_games()

    if df is None:
        return render_html(f'<h2>Search {collection.capitalize()}</h2><p class="fallback">No {collection} CSV could be loaded.</p>')

    query = ''
    field = None
    results = None
    search_fields = get_search_fields(df)
    if request.method == 'POST':
      query = request.form.get('query', '').strip()
      field = request.form.get('field', search_fields[0] if search_fields else df.columns[0])
      all_fields = request.form.get('all_fields', '') == 'on'
      if field not in df.columns:
        field = search_fields[0]
      if query:
        if all_fields:
          mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
          results = df[mask]
        else:
          results = df[df[field].astype(str).str.contains(query, case=False, na=False)]

    content = f'<h2>Search {collection.capitalize()}</h2>'
    content += '<form class="search-form" method="post">'
    content += '<label for="field">Search field</label>'
    content += '<select id="field" name="field">'
    for option in search_fields:
      selected = ' selected' if option == field else ''
      content += f'<option value="{option}"{selected}>{option}</option>'
    content += '</select>'
    content += '<label for="query">Search text</label>'
    content += f'<input id="query" name="query" value="{query}" placeholder="Enter a search term" required>'
    content += '<label style="margin-top:8px"><input type="checkbox" name="all_fields"> Search across all fields</label>'
    content += '<button type="submit">Search</button>'
    content += '</form>'

    if results is not None:
        if results.empty:
            content += '<p>No items matched that query.</p>'
        else:
            content += f'<p>Found {len(results)} matching rows.</p>'
            content += render_collection_table(results)
    elif request.method == 'POST':
        content += '<p>Enter search text and hit Search to filter the collection.</p>'

    return render_html(content)


@app.route('/add/film', methods=['GET', 'POST'])
def add_film():
    df, path = load_films()
    # Determine fields to prompt for
    if df is not None:
        fields = list(get_search_fields(df))
    else:
        fields = ['Title', 'Genre', 'Release', 'Year', 'Director', 'Rating']

    if request.method == 'POST':
        row = {f: request.form.get(f, '').strip() for f in fields}
        dest = path or FILM_CSV_CANDIDATES[0]
        try:
            append_row_to_csv(dest, row, columns=fields)
            content = '<h2>Add Film</h2>'
            content += f'<p>Added film to <strong>{dest}</strong>.</p>'
            content += '<p><a class="button-link" href="/films">View Films</a> <a class="button-link" href="/add/film">Add Another</a></p>'
            return render_html(content)
        except Exception as exc:
            return render_html(f'<h2>Add Film</h2><p class="fallback">Error saving film: {exc}</p>')

    # render form
    content = '<h2>Add Film</h2>'
    content += '<form class="search-form" method="post">'
    for f in fields:
        content += f'<label for="{f}">{f}</label>'
        content += f'<input id="{f}" name="{f}" placeholder="{f}">'
    content += '<button type="submit">Add Film</button>'
    content += '</form>'
    return render_html(content)


@app.route('/add/game', methods=['GET', 'POST'])
def add_game():
  # Load existing game CSV to discover columns
  games_df, sources = load_games()
  if games_df is not None:
    fields = list(games_df.columns)
  else:
    fields = ['Game', 'System']

  if request.method == 'POST':
    row = {f: request.form.get(f, '').strip() for f in fields}
    # Choose destination: first existing game CSV or default
    dest = None
    for candidate in GAME_CSV_CANDIDATES:
      if os.path.isfile(candidate) and detect_csv_type(candidate) == 'game':
        dest = candidate
        break
    if not dest:
      dest = GAME_CSV_CANDIDATES[0]

    try:
      append_row_to_csv(dest, row, columns=fields)
      content = '<h2>Add Game</h2>'
      content += f'<p>Added game to <strong>{dest}</strong>.</p>'
      content += '<p><a class="button-link" href="/games">View Games</a> <a class="button-link" href="/add/game">Add Another</a></p>'
      return render_html(content)
    except Exception as exc:
      return render_html(f'<h2>Add Game</h2><p class="fallback">Error saving game: {exc}</p>')

  # render form
  content = '<h2>Add Game</h2>'
  content += '<form class="search-form" method="post">'
  for f in fields:
    content += f'<label for="{f}">{f}</label>'
    content += f'<input id="{f}" name="{f}" placeholder="{f}">'
  content += '<button type="submit">Add Game</button>'
  content += '</form>'
  return render_html(content)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
