import base64
import html
from pathlib import Path

ROOT = Path(__file__).parent
CSS_LINK = '<link rel="stylesheet" href="https://theogalh.github.io/design-system/styles.css">'
AVATAR_FILE = ROOT / "assets" / "avatar.webp"
AVATAR = (
    "data:image/webp;base64," + base64.b64encode(AVATAR_FILE.read_bytes()).decode()
    if AVATAR_FILE.exists() else "assets/avatar.webp"
)

EXTRA_CSS = """
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;margin-bottom:40px}
.hero-art{position:relative;display:flex;justify-content:center}
.hero-art img{width:100%;max-width:520px;height:auto;filter:drop-shadow(0 20px 40px rgba(0,0,0,.5))}
.hero-art::after{content:"";position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);width:60%;height:1px;background:var(--line-soft)}
.contact{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.contact a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;border:1px solid var(--line);border-radius:var(--r-md);color:var(--text);text-decoration:none;font-size:14px;font-weight:500;transition:border-color .15s cubic-bezier(.2,.8,.2,1),background .15s cubic-bezier(.2,.8,.2,1)}
.contact a:hover{border-color:var(--peri);background:var(--panel-2)}
.contact a .k{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
.app-card .stack{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint);margin:0 0 10px}
.feature-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.feature{padding:18px;border:1px solid var(--line-soft);border-radius:var(--r-lg);background:var(--panel)}
.feature h3{font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:15px;margin:0 0 6px}
.feature p{margin:0;color:var(--muted);font-size:14px;line-height:1.55}
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;counter-reset:step}
.flow .step{position:relative;padding:16px 16px 16px 44px;border:1px solid var(--line-soft);border-radius:var(--r-md);background:var(--panel);color:var(--muted);font-size:14px;line-height:1.5}
.flow .step::before{counter-increment:step;content:counter(step,decimal-leading-zero);position:absolute;left:14px;top:16px;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--peri)}
.decisions{margin:0;padding:0;list-style:none}
.decisions li{padding:14px 0;border-bottom:1px solid var(--line-soft);font-size:14px;line-height:1.55;color:var(--muted)}
.decisions li:last-child{border-bottom:0}
.decisions li strong{color:var(--text);font-weight:600;display:block;margin-bottom:2px}
.crumbs{margin-bottom:18px}
.tree pre{font-size:12.5px}
@media (max-width:900px){.hero{grid-template-columns:1fr}.hero-art{order:-1}.hero-art img{max-width:360px}}
"""


def shell(title, body, depth, active=None, context="projects"):
    rel = "../" if depth else ""
    nav_items = [("Projects", f"{rel}index.html#projects", "projects"),
                 ("About", f"{rel}index.html#about", "about"),
                 ("GitHub", "https://github.com/Theogalh", None)]
    nav = "".join(
        f'<a href="{h}"{" class=\"active\"" if k == active else ""}>{t}</a>' for t, h, k in nav_items
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — theogalh.dev</title>
  <link rel="icon" href="https://theogalh.github.io/design-system/assets/logo.svg">
  {CSS_LINK}
  <style>{EXTRA_CSS}</style>
</head>
<body>
<header class="topbar">
  <a class="wordmark" href="{rel}index.html">theogalh<span class="dot"></span></a>
  <nav class="nav collapsible">{nav}</nav>
  <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</header>
<main class="admin-wrap">
{body}
</main>
<footer class="footer">theogalh.dev · {context} · dark by default</footer>
<script>
  const burger = document.querySelector('.burger');
  const links = [...document.querySelectorAll('.nav a')].map(a => [a.textContent, a.getAttribute('href')]);
  burger.addEventListener('click', () => {{
    const overlay = document.createElement('div'); overlay.className = 'drawer-overlay';
    const drawer = document.createElement('nav'); drawer.className = 'drawer';
    drawer.innerHTML = '<div class="drawer-head"><span class="wordmark">theogalh<span class="dot"></span></span><button class="btn btn-ghost btn-sm">Close</button></div>'
      + links.map(([t, h]) => `<a href="${{h}}">${{t}}</a>`).join('');
    const close = () => {{ overlay.remove(); drawer.remove(); burger.setAttribute('aria-expanded', 'false'); }};
    overlay.addEventListener('click', close);
    drawer.querySelector('button').addEventListener('click', close);
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    document.body.append(overlay, drawer);
    burger.setAttribute('aria-expanded', 'true');
  }});
  document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', () => {{
    navigator.clipboard.writeText(b.closest('.code-block').querySelector('code').innerText);
    b.textContent = 'Copied'; setTimeout(() => b.textContent = 'Copy', 1200);
  }}));
</script>
</body>
</html>
"""


# ───────────────────────── project pages ─────────────────────────

def meta(rows):
    return '<div class="meta-grid">' + "".join(
        f'<div class="meta-row"><div class="meta-label">{k}</div><div class="meta-value mono">{v}</div></div>' for k, v in rows
    ) + "</div>"


def ledger(head, rows, first_is_method=False):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = ""
    for r in rows:
        cells = list(r)
        if first_is_method:
            m = cells[0].lower()
            cls = {"delete": "del"}.get(m, m)
            cells[0] = f'<span class="method {cls}">{cells[0]}</span>'
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    return f'<div class="ledger-scroll"><table class="ledger"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def code(head, body, copy=False):
    btn = ' <button class="copy">Copy</button>' if copy else ""
    return f'<div class="code-block"><div class="code-head">{head}{btn}</div><pre><code>{body}</code></pre></div>'


def project_page(p):
    stats = "".join(
        f'<div class="stat-card anim-rise"><div class="stat-label">{l}</div><div class="stat-value">{v}</div><div class="stat-delta muted">{d}</div></div>'
        for l, v, d in p["stats"]
    )
    features = "".join(f'<div class="feature"><h3>{t}</h3><p>{d}</p></div>' for t, d in p["features"])
    flow = "".join(f'<div class="step">{s}</div>' for s in p["flow"])
    decisions = "".join(f"<li><strong>{t}</strong>{d}</li>" for t, d in p["decisions"])
    actions = "".join(
        f'<a class="btn {"btn-primary" if i == 0 else "btn-ghost"}" href="{h}">{t}</a>' for i, (t, h) in enumerate(p["links"])
    )
    body = f"""
  <div class="crumbs"><a href="../index.html">Projects</a><span class="sep">/</span><span class="current">{p["name"]}</span></div>
  <div class="page-head">
    <p class="eyebrow">theogalh.dev · project · {p["num"]}</p>
    <h1 class="display">{p["title"]}</h1>
    <p class="sub">{p["sub"]}</p>
    <div class="action-row">{actions}</div>
  </div>

  <section class="section"><div class="stats-grid stagger">{stats}</div></section>

  <section class="section">
    <h2 class="section-title">What it does</h2>
    <p class="muted" style="margin-bottom:16px">{p["pitch"]}</p>
    <div class="feature-list">{features}</div>
  </section>

  <section class="section">
    <h2 class="section-title">{p["flow_title"]}</h2>
    <div class="flow">{flow}</div>
  </section>

  <div class="hairline" style="margin:36px 0"></div>
  <p class="eyebrow">how it is built</p>

  <section class="section split">
    <div class="panel">
      <h2 class="section-title">Stack</h2>
      {meta(p["stack"])}
    </div>
    <div class="panel">
      <h2 class="section-title">Architecture</h2>
      <p class="muted">{p["arch_text"]}</p>
      <div class="tree">{code(p["tree_head"], p["tree"])}</div>
    </div>
  </section>

  <section class="section panel">
    <h2 class="section-title">Decisions</h2>
    <ul class="decisions">{decisions}</ul>
  </section>

  <section class="section panel">
    <h2 class="section-title">{p["api_title"]}</h2>
    {ledger(p["api_head"], p["api"], first_is_method=p.get("api_methods", True))}
  </section>

  <section class="section split">
    <div class="panel">
      <h2 class="section-title">Run it</h2>
      {code("shell", p["run"], copy=True)}
    </div>
    <div class="panel">
      <h2 class="section-title">Deploy &amp; ops</h2>
      {meta(p["ops"])}
    </div>
  </section>
"""
    return shell(p["name"], body, depth=1, active="projects", context=p["name"])


PROJECTS = [
    # ───────────── screenator ─────────────
    dict(
        slug="screenator", name="screenator", num="01", letter="S",
        title="Guess the game from a single screenshot.",
        sub="A guessing game for people who play a lot. In Discord, or in a browser room with friends.",
        card="Guess the game from a screenshot. Discord bot and multiplayer web rooms.",
        card_stack="python · discord.py · fastapi · redis · websocket",
        links=[("Open screenator.theogalh.dev", "https://screenator.theogalh.dev"), ("Repository", "https://github.com/Theogalh/Screenator-bot")],
        stats=[("Surfaces", "2", "discord · web"), ("Services", "3", "bot · web · playground"),
               ("Round timeout", "12 h", "configurable 1–168"), ("Languages", "2", "en · fr")],
        pitch="One player posts a screenshot of a video game. Everyone else races to name it. The first correct answer scores and picks the next screenshot. Screenator keeps the rounds, the scores and the fairness rules so the group only has to play.",
        features=[
            ("Discord native", "Slash commands under a configurable prefix. An admin registers a channel, starts a game, and each channel runs its own independent game with its own leaderboard."),
            ("Web rooms", "Create a room with an account, or join anonymously from an invite link. Live chat, live leaderboard, and the room owner can kick a player."),
            ("Fair rounds", "After a round with a winner, only the winner can post the next screenshot. Only the round author can declare a winner manually."),
            ("Forgiving answers", "Typos do not lose the round: answers above a minimum length are fuzzy-matched against the solution."),
            ("Timeouts", "If nobody finds the game before the per-channel timeout, the bot ends the round and reveals the answer."),
            ("Bilingual", "The web UI switches between English and French from the navbar."),
        ],
        flow_title="A round, step by step",
        flow=["A player posts a screenshot with <span class=\"mono\">/scr round</span> or from the room.",
              "Players type their guesses in chat.",
              "A guess is compared to the solution, exact or fuzzy.",
              "First correct guess: +1 point, round closes, winner posts next.",
              "No guess before timeout: the bot reveals the game, anyone may post next.",
              "<span class=\"mono\">/scr stop</span> ends the game and prints the final leaderboard."],
        stack=[("language", "Python 3.13 · uv"), ("bot", "discord.py, slash command groups"),
               ("web", "FastAPI · Jinja2 · WebSocket · slowapi"), ("storage", "Redis, hierarchical keys, optional TTL"),
               ("files", "S3-compatible object storage (Scaleway fr-par)"), ("matching", "fuzzy, threshold 85 above 7 chars"),
               ("checks", "black · ruff · mypy · pytest + coverage")],
        arch_text="One package, three entry points. All three share one Redis and one storage interface.",
        tree_head="layout",
        tree="""screenator/
  bot/          discord.py cogs, slash commands
  web/          FastAPI app, WebSocket rooms
    templates/  Jinja2 pages + partials (navbar, footer)
  playground/   matching sandbox service
  storage/      StorageInterface + DTOs (Game, Round, Leaderboard)
  cache/        Redis implementation, key builder
deploy/
  screenator.service · screenator-web.service · screenator-playground.service
  nginx/screenator.conf · deploy.sh · sudoers-screenator""",
        decisions=[
            ("One storage interface, typed DTOs", "Game logic only sees <span class=\"mono\">StorageInterface</span> and dataclasses. Redis is the current backend; SQLite or Postgres can replace it without touching a command handler."),
            ("Three services, one codebase", "Bot, web app and playground are separate systemd units on the same repo. They deploy together and share configuration."),
            ("Anonymous players are first-class", "An invite token creates a <span class=\"mono\">name#1234</span> identity; a session-sync id moves it between devices. Logged-in players recover their rooms server-side."),
            ("The bucket is never public", "Images are served through proxy tokens with their own TTL. Scaleway credentials also accept the native env aliases."),
            ("Same check locally and in CI", "<span class=\"mono\">make check</span> runs formatting, lint, types and tests. CI runs it plus a web smoke import, then deploys on push to master."),
        ],
        api_title="Commands", api_head=["Command", "Who", "What it does"], api_methods=False,
        api=[("<span class=\"mono\">/scr setup [timeout_hours]</span>", "admin", "Register the current channel as a game channel"),
             ("<span class=\"mono\">/scr start</span>", "admin", "Start a new game in the channel"),
             ("<span class=\"mono\">/scr stop</span>", "admin", "End the game, show the final leaderboard"),
             ("<span class=\"mono\">/scr round &lt;image&gt;</span>", "player", "Start a round with a screenshot"),
             ("<span class=\"mono\">/scr win &lt;player&gt;</span>", "round author", "Declare a winner manually"),
             ("<span class=\"mono\">/scr leaderboard</span>", "player", "Show the current leaderboard")],
        run="""uv sync
cp .env.example .env          <span class="c-com"># DISCORD_TOKEN, REDIS_URL</span>
uv run screenator             <span class="c-com"># discord bot</span>
uv run screenator-web         <span class="c-com"># web app on :8000</span>
make check""",
        ops=[("units", "screenator · screenator-web · screenator-playground"), ("proxy", "nginx, websocket upgrade"),
             ("deploy", "deploy.sh: pull → uv sync --no-dev → units → restart → /health"), ("nginx", "managed only if DEPLOY_MANAGE_NGINX=true"),
             ("ci", "GitHub Actions on master/main"), ("license", "MIT")],
    ),
    # ───────────── screen ─────────────
    dict(
        slug="screen", name="screen", num="02", letter="C",
        title="Drop a screenshot. Get a link.",
        sub="Upload, annotate in the browser, choose who can see it. Nothing else.",
        card="Drop a screenshot, annotate it, share a link. Public or private.",
        card_stack="fastapi · redis · s3 · cloudflare · canvas",
        links=[("Open screen.theogalh.dev", "https://screen.theogalh.dev"), ("Repository", "https://github.com/Theogalh/screen")],
        stats=[("Upload limit", "10/min", "per IP"), ("Cache", "1 year", "immutable by id"),
               ("Storage", "S3", "+ Cloudflare CDN"), ("Retention", "setting", "days, cleaned on expiry")],
        pitch="Screenshots pasted into chats end up as attachments nobody can find again. screen turns them into links: drop the image, get a URL that loads fast from a CDN, draw on it if you need to point at something, and flip it private when it is not for everyone.",
        features=[
            ("Drag and drop", "A single dropzone. Files are validated server-side and rejected with a clear message when they are not images."),
            ("Thumbnails", "Every screenshot gets a thumbnail for the gallery, served with the same long-lived cache headers."),
            ("Annotate", "Open a screenshot in the canvas, draw, save. The annotated version keeps its own URL, and the drawing can be reopened later."),
            ("Public or private", "A toggle per screenshot. Private screenshots are only reachable by their owner."),
            ("Delete when done", "One call removes the object, the thumbnail, the canvas and the metadata."),
        ],
        flow_title="From drop to link",
        flow=["Drop an image on the page.",
              "The server validates it, uploads to object storage, builds a thumbnail.",
              "Metadata (id, name, visibility, dates) goes to Redis.",
              "The gallery shows the thumbnail; the link points at the CDN.",
              "Optional: open the canvas, draw, save ops + rendered image.",
              "After the retention window, everything for that id is removed."],
        stack=[("scaffold", "theoproject --fastapi --redis"), ("api", "FastAPI · pydantic-settings · slowapi"),
               ("files", "theolib/storage snippet — S3 + Cloudflare CDN + metadata store"), ("metadata", "Redis, keys built in cache/keys.py"),
               ("ui", "Jinja2 SSR · canvas · shared design tokens"), ("deploy", "systemd · nginx · Ubuntu LXC")],
        arch_text="A standard theoproject layout. The screenshots module is the only business module; storage comes from a versioned snippet.",
        tree_head="layout",
        tree="""app/          config · main (lifespan opens Redis + uploader) · router
modules/
  health/     GET /health — Redis ping
  screenshots/
    controller.py   routes, rate limits, HTTP mapping
    service.py      upload · list · canvas · visibility · delete
    schemas.py      ScreenshotResponse, CanvasSaveRequest, …
theolib/storage/    snippet: S3 uploader, image validation, CDN URLs
cache/        RedisClient + key builder
web/          Jinja2 SSR, GET /
static/ templates/ deploy/ .github/""",
        decisions=[
            ("Constructor injection, no globals", "Services receive the uploader, the store and the retention setting. Controllers build the service per request from <span class=\"mono\">app.state</span>."),
            ("Validation is a 422, not a 500", "<span class=\"mono\">ImageValidationError</span> from the storage snippet maps to a 422 with the reason. Bad files never reach the bucket."),
            ("Annotations are data, then pixels", "The canvas is saved as an op list plus a rendered image. The op list makes it editable; the image makes it shareable."),
            ("Immutable by construction", "The id is the cache key, so <span class=\"mono\">Cache-Control: public, max-age=31536000, immutable</span> is safe. A changed image is a new id."),
            ("Storage is a snippet, not a copy", "<span class=\"mono\">theolib/storage</span> is installed and pinned by theoproject; fixes are released as a tag and pulled with <span class=\"mono\">theoproject update storage</span>."),
        ],
        api_title="API", api_head=["Method", "Path", "Description"],
        api=[("POST", "/api/screenshots/", "Upload; <span class=\"mono\">public</span> form field or query, default true · 10/min"),
             ("GET", "/api/screenshots/", "List, <span class=\"mono\">limit</span> / <span class=\"mono\">offset</span>"),
             ("GET", "/api/screenshots/{id}", "Metadata"),
             ("GET", "/api/screenshots/{id}/image", "Original, immutable cache"),
             ("GET", "/api/screenshots/{id}/thumbnail", "Thumbnail, immutable cache"),
             ("PATCH", "/api/screenshots/{id}/visibility", "Set public / private"),
             ("PUT", "/api/screenshots/{id}/canvas", "Save ops + image_data"),
             ("GET", "/api/screenshots/{id}/canvas", "Ops for re-editing"),
             ("GET", "/api/screenshots/{id}/canvas/image", "Rendered annotated image"),
             ("DELETE", "/api/screenshots/{id}", "Remove everything for this id")],
        run="""uv sync
docker run -p 6379:6379 redis:alpine
cp .env.example .env          <span class="c-com"># REDIS_URL, S3 + CDN settings</span>
uv run uvicorn app.main:app --reload""",
        ops=[("user · dir", "screen · /opt/screen"), ("unit", "screen.service, port 8000"),
             ("deploy", "push to master → GitHub Actions → deploy.sh over SSH"), ("first run", "bash deploy/setup.sh &lt;repo&gt; master"),
             ("secrets", "SSH_HOST · SSH_USER · SSH_PRIVATE_KEY · SSH_PORT")],
    ),
    # ───────────── ytp ─────────────
    dict(
        slug="ytp", name="ytp", num="03", letter="Y",
        title="Paste a URL. Pick a format. Download.",
        sub="A video downloader with trimming, live progress, and an MCP server so an assistant can use it too.",
        card="Paste a video URL, pick a format, trim, download. Also an MCP server.",
        card_stack="fastapi · yt-dlp · redis · sse · mcp",
        links=[("Open ytp.theogalh.dev", "https://ytp.theogalh.dev"), ("Repository", "https://github.com/Theogalh/ytp-downloader")],
        stats=[("Formats", "4", "mp3 · m4a · mp4 · webm"), ("Progress", "SSE", "500 ms refresh"),
               ("Rate limits", "20 / 10", "info · downloads per min"), ("Agent", "MCP", "3 tools")],
        pitch="Most downloaders make you wait on a spinner and give you the whole file. ytp analyses the URL first, lets you choose audio or video and a segment, runs the job in the background and tells you when the file is ready. The same engine is exposed to Claude through MCP.",
        features=[
            ("Analyse first", "Paste a URL and get the title, duration and available formats before committing to a download."),
            ("Audio or video", "mp3 and m4a for audio, mp4 and webm for video. The format id comes straight from the analysis."),
            ("Trim", "Set a start and an end time to keep only the part you want. The cut happens server-side."),
            ("Live progress", "The page subscribes to the job and updates until the file is ready or the job fails."),
            ("From an assistant", "Three MCP tools: get info for a plain download, open the trim editor to choose, download and get a URL back."),
            ("Cleaned up", "Files live under the job id and are removed after retention. A vanished file is reported as such, not as an error."),
        ],
        flow_title="A download, step by step",
        flow=["<span class=\"mono\">POST /api/videos/info</span> with the URL.",
              "Choose a format id, optionally start and end.",
              "<span class=\"mono\">POST /api/downloads</span> returns <span class=\"mono\">202</span> and a job id.",
              "The worker runs yt-dlp (and ffmpeg for trims) and updates the job in Redis.",
              "The page follows <span class=\"mono\">/events</span> until status is ready or failed.",
              "<span class=\"mono\">GET /file</span> streams the result with the right media type."],
        stack=[("scaffold", "theoproject --fastapi --redis"), ("downloader", "yt-dlp · ffmpeg for trims"),
               ("jobs", "job tracker in Redis · files under data/{job_id}"), ("live", "Server-Sent Events, 500 ms poll of job state"),
               ("agent", "mcp 2.x mounted on /mcp"), ("observability", "opentelemetry-api · metrics module"),
               ("limits", "slowapi, per IP")],
        arch_text="Four modules on the theoproject skeleton. The MCP server calls the same services as the HTTP controllers.",
        tree_head="layout",
        tree="""app/          config · main · router · limiter
modules/
  videos/     POST /videos/info — yt-dlp extract_info
  downloads/  jobs: create · status · events (SSE) · file
  metrics/    OpenTelemetry counters
  health/     Redis ping
mcp/          get_video_info · open_trim_editor · download_video
cache/        RedisClient + key builder · job tracker
data/{job_id}/  downloaded artifacts (retention)
web/ templates/ static/ deploy/ .github/""",
        decisions=[
            ("A download is a job", "The request returns <span class=\"mono\">202 Accepted</span> immediately. yt-dlp never runs inside an HTTP request, so a slow source cannot tie up the app."),
            ("SSE rather than WebSocket", "Progress only flows one way. SSE is plain HTTP, reconnects on its own, and <span class=\"mono\">X-Accel-Buffering: no</span> keeps nginx from buffering it."),
            ("410 for cleaned-up files", "A job that existed but whose artifact was removed answers <span class=\"mono\">410 Gone</span>; a job that is not ready answers <span class=\"mono\">409</span>. The client can tell the cases apart."),
            ("One service layer, two front doors", "HTTP controllers and MCP tools both call <span class=\"mono\">VideoService</span> and <span class=\"mono\">DownloadService</span>. Fixing a bug fixes it for both."),
            ("Rate limits at the edge of the app", "20/min on analysis, 10/min on downloads, per IP, enforced in the controller decorators."),
        ],
        api_title="API", api_head=["Method", "Path", "Description"],
        api=[("POST", "/api/videos/info", "Analyse a URL: title, duration, formats · 20/min"),
             ("POST", "/api/downloads", "Create a job: url, format_id, start_time, end_time → 202 · 10/min"),
             ("GET", "/api/downloads/{job_id}", "Job status and filename"),
             ("GET", "/api/downloads/{job_id}/events", "text/event-stream until ready or failed"),
             ("GET", "/api/downloads/{job_id}/file", "The file · 409 not ready · 410 cleaned up"),
             ("GET", "/health", "Redis ping"),
             ("POST", "/mcp", "MCP server: get_video_info · open_trim_editor · download_video")],
        run="""uv sync
docker run -p 6379:6379 redis:alpine
uv run uvicorn app.main:app --reload
<span class="c-com"># MCP client: https://ytp.theogalh.dev/mcp</span>""",
        ops=[("user · dir", "yd · /opt/ytp_downloader"), ("unit", "ytp_downloader.service, port 8000"),
             ("host", "ytp.theogalh.dev"), ("deploy", "push to master → deploy.sh over SSH"),
             ("retention", "job directories removed on schedule")],
    ),
    # ───────────── theoproject ─────────────
    dict(
        slug="theoproject", name="theoproject", num="04", letter="T",
        title="One command. A project that already knows how to ship.",
        sub="The CLI that scaffolds every project on this site: layout, CI/CD, systemd, nginx, and a Claude Code harness.",
        card="The CLI that scaffolds every project here, deploy included.",
        card_stack="python · click · uv · github actions · systemd",
        links=[("Repository", "https://github.com/Theogalh/theoproject")],
        stats=[("Flavors", "3", "simple · cli · fastapi"), ("Overlays", "3", "redis · sql · design"),
               ("Snippets", "2", "smtp · storage"), ("Secrets to set", "4", "SSH only")],
        pitch="Every side project used to start with the same evening of setup: layout, settings, Redis client, health check, a deploy script, a workflow. theoproject makes that a single command, and keeps the result consistent across projects so moving between them costs nothing.",
        features=[
            ("Three flavors", "A plain Python package, an installable Click CLI with plugin discovery, or a full layered FastAPI app with SSR."),
            ("Storage overlays", "Add Redis, SQLite or both. Each brings a client, its settings and a storage-backed health check."),
            ("Deploy layer", "The FastAPI flavor ships a systemd unit, an nginx config, a setup script for a fresh LXC and a deploy script for every push."),
            ("Versioned snippets", "Reusable modules (SMTP email, S3 file storage) pulled from GitHub tags, pinned in a lockfile, updated on demand."),
            ("Claude Code harness", "Every project ships <span class=\"mono\">.claude/</span>: commands, subagents, skills and example hooks, layered per flavor."),
            ("Design tokens", "<span class=\"mono\">--design</span> adds the shared tokens, components and base template so the UI matches the rest."),
        ],
        flow_title="From empty folder to first deploy",
        flow=["<span class=\"mono\">uv tool install</span> the CLI once.",
              "<span class=\"mono\">theoproject create &lt;name&gt; --fastapi --redis</span> in an empty folder.",
              "Set four SSH secrets on the GitHub repo.",
              "Run <span class=\"mono\">deploy/setup.sh</span> once on the LXC as root.",
              "Push to main: check job, then deploy job over SSH.",
              "Add snippets as needed: <span class=\"mono\">theoproject add smtp</span>."],
        stack=[("cli", "Python · Click · installed with uv tool"), ("templates", "layered dirs: base · web · simple · fastapi · cli"),
               ("placeholders", "APPNAME · APPUSER · APPDIR · DOMAIN"), ("snippets", "GitHub tags (smtp/1.1.0) · .snippets.toml lock · PAT in ~/.config"),
               ("release", "pre-commit hook: src change ⇒ version bump; theoproject release"), ("docs", "ADRs in docs/adr, backlogs, plans")],
        arch_text="Templates are directories merged in order. A flavor is the base plus its layer; the web layer is added for --fastapi.",
        tree_head="templates",
        tree="""theoproject/
  templates/           base: .claude/ harness, ADR scaffolding, .gitignore
  templates_web/       --fastapi only: deploy/, systemd, nginx, deploy.yml
  templates_simple/    pure-Python package
  templates_fastapi/   modules, storage interface, web SSR
  templates_cli/       Click group, plugin loader, 4-layer modules
  snippets/
    smtp/    snippet.toml · src/
    storage/ snippet.toml · src/
  cli.py               create · cli new · add · update · list · release""",
        decisions=[
            ("Layers, not forks", "A flavor never copies another flavor. Fixing the base fixes every generated project going forward."),
            ("One storage contract", "Every overlay implements <span class=\"mono\">StorageInterface</span> (close, ping). Two overlays give a combined <span class=\"mono\">/health</span> for free."),
            ("Snippets are released, not pasted", "A snippet lives in this repo, is tagged per version, and lands in a project's <span class=\"mono\">theolib/</span> with its dependencies merged into pyproject. The lockfile is committed."),
            ("The hook enforces the bump", "A pre-commit hook refuses a change under <span class=\"mono\">src/</span> without a new version in <span class=\"mono\">snippet.toml</span>, and refuses a version that already exists as a tag."),
            ("Minimal deploy surface", "One workflow, four SSH secrets. The server pulls, syncs, restarts and checks health. Nothing else to configure."),
            ("Settled next steps", "Pluggable SSO through an OIDC broker, a runtime contract per deploy tier, and a bug-report library are decided directions, not shipped features."),
        ],
        api_title="Commands", api_head=["Command", "Scope", "What it does"], api_methods=False,
        api=[("<span class=\"mono\">theoproject create &lt;name&gt; [--fastapi|--cli] [--redis] [--sql] [--design]</span>", "new project", "Scaffold the chosen flavor and overlays"),
             ("<span class=\"mono\">theoproject cli new &lt;module&gt;</span>", "--cli project", "Add a 4-layer module"),
             ("<span class=\"mono\">theoproject github-login / github-logout</span>", "machine", "Store or remove the PAT used for snippets"),
             ("<span class=\"mono\">theoproject list</span>", "project", "Available snippets and installed versions (offline)"),
             ("<span class=\"mono\">theoproject add &lt;snippet&gt; [--force]</span>", "project", "Install a snippet at latest"),
             ("<span class=\"mono\">theoproject update &lt;snippet&gt; [--version x.y.z]</span>", "project", "Update or pin"),
             ("<span class=\"mono\">theoproject install-hooks</span>", "this repo", "Pre-commit version guard"),
             ("<span class=\"mono\">theoproject release [snippet]</span>", "this repo", "Tag and push snippet versions")],
        run="""uv tool install git+ssh://git@github.com/Theogalh/theoproject.git
mkdir invoices &amp;&amp; cd invoices
theoproject create invoices --fastapi --redis --design \\
  --user inv --domain invoices.theogalh.dev
theoproject add storage""",
        ops=[("generated workflow", ".github/workflows/deploy.yml — check on PR, deploy on main"), ("generated unit", "deploy/APPNAME.service"),
             ("generated nginx", "deploy/nginx/APPNAME.conf"), ("app dir", "/opt/APPNAME"),
             ("first deploy", "bash deploy/setup.sh &lt;repo&gt; · then sudo -u &lt;user&gt; deploy/deploy.sh")],
    ),
    # ───────────── guess ─────────────
    dict(
        slug="guess", name="guess", num="05", letter="G",
        title="One question. Secret answers. Who wrote what?",
        sub="A party game for two to many players, online with a lobby code or local on one screen.",
        card="Party game. One question, secret answers, guess who wrote what.",
        card_stack="fastapi · redis pub/sub · sse · jinja2",
        links=[("Open guess.theogalh.dev", "https://guess.theogalh.dev"), ("Repository", "https://github.com/Theogalh/guess-game")],
        stats=[("Players", "2+", "per lobby"), ("Lobby code", "6", "chars, no 0/O/1/I"),
               ("Modes", "2", "online · local"), ("Question pools", "2", "en · fr")],
        pitch="The game master asks a question. Everyone answers in secret. The answers come back one at a time, in a shuffled order, and the group debates then votes on who wrote each one. Points for guessing right, points for fooling everyone.",
        features=[
            ("Lobby by code", "Six letters, easy to read out loud. Each player joins from their own phone and picks a nickname."),
            ("Question pools", "Built-in questions in English and French. The game master can also type a custom one; custom questions are kept for later review."),
            ("Reveal and vote", "Each answer is shown alone. A debate timer, then a vote timer. Votes can be changed until the timer closes."),
            ("Local mode", "Same game, one device passed around. Timers and scoring are dropped; the flow stays."),
            ("Chat", "In-lobby chat, capped at 200 characters and one message per second."),
            ("Rounds", "Results, then the game master starts the next round. Round numbers and stats are tracked."),
        ],
        flow_title="A round, state by state",
        flow=["<span class=\"mono\">LOBBY_WAITING</span> — players join; GM starts with at least two.",
              "<span class=\"mono\">QUESTION_SELECTION</span> — GM types a question or draws a random one.",
              "<span class=\"mono\">ANSWERING</span> — everyone answers; auto-advances on the last submit, or GM forces it.",
              "<span class=\"mono\">REVEALING</span> — one answer is shown, order shuffled.",
              "<span class=\"mono\">VOTING</span> — debate, then vote on the author; then next answer or results.",
              "<span class=\"mono\">RESULTS</span> — scores; GM resets for the next round."],
        stack=[("scaffold", "theoproject --fastapi --redis"), ("state", "Redis hashes per lobby, TTL on expiry"),
               ("live", "Redis pub/sub → one SSE stream per lobby"), ("modules", "lobby · game · online · local · questions · session · sse · stats"),
               ("ids", "secrets.choice over a 32-char alphabet"), ("ui", "Jinja2 SSR, vanilla JS subscribing to SSE")],
        arch_text="A base GameService owns everything mode-agnostic. Online and local subclasses add or drop timers and scoring.",
        tree_head="layout",
        tree="""modules/
  lobby/      create · join · leave · kick
  game/       GameService: question, answers, reveal, votes, chat, reset
  online/     OnlineGameService: debate/vote timers, scoring
  local/      LocalGameService: no timers, pass-the-phone
  questions/  pools per language, custom question capture
  session/    player identity cookie
  sse/        GET /lobbies/{code}/events — subscribe to pub/sub
  stats/      rounds started · finished · replays
storage/      DTOs: LobbyDTO, RoundDTO, ChatMessageDTO, GameState
cache/        Redis client, Keys.sse_channel(code), …""",
        decisions=[
            ("A round is a state machine", "Every action first asserts the lobby state it expects and, when relevant, that the caller is the game master. Invalid actions are a <span class=\"mono\">GameError</span>, not a corrupted lobby."),
            ("The browser never computes state", "Each transition publishes a typed event on the lobby's Redis channel; the SSE endpoint relays it. Clients only render what they receive."),
            ("Shuffle once, at question time", "The reveal order is fixed when the question is set and stored on the round, so every client sees the same order."),
            ("Inheritance where it pays", "<span class=\"mono\">GameService</span> holds the shared logic; online overrides <span class=\"mono\">start_reveal</span> to arm timers and <span class=\"mono\">_end_round</span> to score. Local keeps the defaults."),
            ("Best-effort anti-repeat", "Random questions retry a few times to avoid the previous one, then fall back to a scan. No repeat when there is more than one question."),
        ],
        api_title="Events on the lobby stream", api_head=["Event", "Payload", "When"], api_methods=False,
        api=[("<span class=\"mono\">state_changed</span>", "state", "Every transition"),
             ("<span class=\"mono\">question_set</span>", "question", "GM selected or drew a question"),
             ("<span class=\"mono\">answer_submitted</span>", "player_id · submitted · total", "A player answered"),
             ("<span class=\"mono\">reveal_started</span>", "reveal_index · nickname · answer", "An answer is shown"),
             ("<span class=\"mono\">voting_open</span>", "reveal_index · debate_secs · vote_secs", "Timers armed"),
             ("<span class=\"mono\">vote_cast</span>", "reveal_index · total_voted · total_players", "A vote landed"),
             ("<span class=\"mono\">voting_closed</span>", "reveal_index · votes", "Votes revealed"),
             ("<span class=\"mono\">chat_message</span>", "nickname · message · ts", "Chat"),
             ("<span class=\"mono\">lobby_reset</span>", "round_number", "Next round")],
        run="""uv sync
docker run -p 6379:6379 redis:alpine
uv run uvicorn app.main:app --reload""",
        ops=[("user · dir", "guess · /opt/guess"), ("unit", "guess.service, port 8000"),
             ("deploy", "push to master → deploy.sh over SSH"), ("lobby expiry", "Redis TTL on lobby keys")],
    ),
    # ───────────── bbc ─────────────
    dict(
        slug="bbc", name="bbc", num="06", letter="B",
        title="A leaderboard for a fighting game crew.",
        sub="Brésil Bagarre Club. Report your sets, watch your rating move, run a bracket on tournament night.",
        card="Fighting game leaderboard. Elo across 2XKO, SF6 and Tekken 8, plus tournaments.",
        card_stack="fastapi · sqlite · elo · sse · tailwind",
        links=[("Open bbc.theogalh.dev", "https://bbc.theogalh.dev"), ("Repository", "https://github.com/Theogalh/BresilBagarreClub")],
        stats=[("Games", "3", "2XKO · SF6 · Tekken 8"), ("Elo K", "32", "start 1000 · floor 0"),
               ("Bracket size", "2–32", "single or double elim"), ("CI gate", "tests", "red run blocks deploy")],
        pitch="Offline sets deserve a ranking that means something. BBC keeps one rating per player per game, asks the opponent to confirm each result, shows match history with the rating delta, and turns a list of players into a seeded bracket when the crew runs a tournament.",
        features=[
            ("Per-game and global boards", "A rating per player per game, and a global leaderboard across all three."),
            ("Confirmed results", "A match is submitted by one player and stays pending until the opponent approves it. Both get notified live."),
            ("Profiles", "Per-game stats, full match history with the delta, and head-to-head records against any player."),
            ("Tournaments", "Pick 2 to 32 players, single or double elimination, best-of-N. Seeded by rating; byes resolve instantly."),
            ("Grand final reset", "In double elimination the losers' champion must beat the winners' champion twice."),
            ("Accounts", "Players link an account to submit, approve and receive notifications."),
        ],
        flow_title="A set, from result to rating",
        flow=["A player submits game, opponent and winner.",
              "The match is stored as pending; the opponent is notified over SSE.",
              "The opponent approves (or rejects) from their account.",
              "Approval replays the match through <span class=\"mono\">submit_match</span>.",
              "Elo expected score and delta are computed for both players.",
              "History, profiles and both leaderboards update."],
        stack=[("backend", "FastAPI · Python 3.11 · uv"), ("db", "SQLite, raw sqlite3, no ORM"),
               ("layers", "controllers → services → datastore"), ("rating", "Elo · K 32 · scale 400 · floor 0"),
               ("live", "SSE per account for notifications"), ("front", "plain HTML/JS · Tailwind"),
               ("tests", "pytest, isolated SQLite per test · ruff")],
        arch_text="Services carry the rules; datastore modules carry the SQL. No ORM in between.",
        tree_head="layout",
        tree="""app/
  controllers/   FastAPI routes
  services/      account · games · match · mmr · pending · session · tournament
  datastore/     one module per table group, raw SQL
  models/        pydantic schemas
  sse.py         per-account event push
  database.py    connection + schema
  static/        HTML/JS pages, Tailwind
deploy/          setup.sh · deploy.sh · nginx/bresil-bagarre.conf
tests/""",
        decisions=[
            ("Approval reuses the write path", "Approving a pending match calls the same <span class=\"mono\">submit_match</span> as a direct submission, with <span class=\"mono\">force=True</span>. One place computes ratings."),
            ("Brackets are pre-linked", "All matches are created up front as shells; each knows its next match and slot, and in double elimination where its loser drops. Advancing is a pointer update."),
            ("Byes never touch ratings", "Round-one byes complete on creation and advance the player without a global match."),
            ("Tournament sets feed Elo, best-effort", "A completed series is submitted as a regular match; a rating error never breaks the bracket."),
            ("Seeding is standard", "Seeds 1 and 2 can only meet in the final; order is generated recursively for the next power of two."),
            ("Tests gate production", "Each test runs on its own SQLite file with no network. Deploy runs only after lint and tests pass on master."),
        ],
        api_title="API", api_head=["Method", "Path", "Description"],
        api=[("GET", "/api/games", "List games"),
             ("GET", "/api/players", "List players"), ("POST", "/api/players", "Create player"),
             ("GET", "/api/players/{id}", "Profile + per-game MMR"), ("GET", "/api/players/{id}/matches", "Match history"),
             ("GET", "/api/leaderboard/global", "Global leaderboard"), ("GET", "/api/leaderboard/{game}", "Per-game leaderboard"),
             ("POST", "/api/matches", "Submit a match result"), ("GET", "/api/matches/recent", "Recent matches, all games"),
             ("GET", "/api/matches/{game}", "Recent matches for one game"), ("GET", "/health", "Health check")],
        run="""uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
uv run pytest --cov=app
uv run ruff check .""",
        ops=[("user · dir", "bbc · /opt/bresil-bagarre"), ("port", "8000, nginx in a separate container"),
             ("ci", ".github/workflows/ci.yml — lint + tests, then deploy on master"), ("first run", "bash deploy/setup.sh &lt;repo&gt; main")],
    ),
    # ───────────── theoapi ─────────────
    dict(
        slug="theoapi", name="theoapi", num="07", letter="A",
        title="One account for every app.",
        sub="TheoAPI is the identity layer under the rest: sign in once, and each app decides what that account may do.",
        card="One account for every app. Login, roles, admin console.",
        card_stack="fastapi · sqlite · oauth · rbac · jinja2",
        links=[("Open console.theogalh.dev", "https://console.theogalh.dev"), ("Repository", "https://github.com/Theogalh/console_theogalh_dev")],
        stats=[("Login methods", "3", "password · Google · Jellyfin"), ("Access token", "60 min", "refresh 30 days"),
               ("RBAC layers", "2", "platform · per app"), ("Password hash", "200k", "PBKDF2-HMAC-SHA256")],
        pitch="Every app on this site needs users, and none of them should have to implement login. TheoAPI issues tokens, holds accounts and roles, lets each app define its own roles and delegate admin to specific people, and gives users a console that only shows what they may open.",
        features=[
            ("Sign in three ways", "Email and password with verification and reset, Google OAuth, or a Jellyfin login. All end in the same token pair."),
            ("Per-app roles", "An app registers its roles. A user can be an admin of one app without any platform rights."),
            ("Console", "A dashboard listing the apps your roles allow, plus admin screens for users, apps and roles."),
            ("Audit log", "Every app-scoped admin action is logged; platform actions are logged against the platform app."),
            ("API keys and bearer tokens", "Apps and scripts authenticate with a header; browsers with a cookie and CSRF token."),
            ("Jellyfin link", "Media-server accounts can be linked to TheoAPI accounts, so one identity spans apps and media."),
        ],
        flow_title="A login, step by step",
        flow=["Credentials arrive: ApiKey header, Bearer header, or the <span class=\"mono\">theoapi_token</span> cookie.",
              "The principal is resolved; verified, deleted and forced-reset flags are checked.",
              "Platform roles are loaded from <span class=\"mono\">principal_roles</span>.",
              "Per-app roles come from <span class=\"mono\">user_app_roles</span> when the route is app-scoped.",
              "Cookie requests must also carry the double-submit CSRF header on unsafe methods.",
              "Access token expires after 60 minutes; refresh issues a new pair, revoking per policy."],
        stack=[("backend", "FastAPI · Python 3.12 · uv"), ("db", "SQLite, raw sqlite3, all SQL in src/data/db.py"),
               ("layers", "controller → service → manager → db"), ("credentials", "ApiKey header · Bearer header · cookie + CSRF"),
               ("hashing", "PBKDF2-HMAC-SHA256 200k · sha256 for tokens and keys"), ("tokens", "access 60 min · refresh 30 d · revoke-all policies"),
               ("ui", "Jinja2 · theo-ui SDK (shared design system)"), ("hosts", "console.theogalh.dev · api.console.theogalh.dev")],
        arch_text="One module per domain, each four layers deep. Cross-cutting concerns live in src/common.",
        tree_head="layout",
        tree="""src/app/       app factory, settings, router assembly
src/common/    auth middleware · RBAC deps · CSRF · rate limit · hashing · email · Jellyfin client
src/data/db.py all SQL, one connection per call
src/modules/
  auth/        login · register · refresh · logout · google · jellyfin
  users/       profile, verification, password reset
  apps/        app registry, app roles, user-app roles
  admin/       platform and app-scoped admin
  toolbox/     stub
src/web/       Jinja page routes under /web, redirect instead of 401
templates/ · sdk/theo_ui/ · scripts/migrate_db.py · scripts/seed_admin.py""",
        decisions=[
            ("Principals, not users", "Anything that can act is a principal: a user, a dev bearer token, an API key. Roles attach to principals, so scripts and apps get permissions without a fake user."),
            ("Two RBAC layers, kept apart", "Platform roles (<span class=\"mono\">super_admin · admin · user · app</span>) and per-app roles with an <span class=\"mono\">is_admin</span> flag. <span class=\"mono\">super_admin</span> bypasses app checks everywhere."),
            ("Three doors, one token model", "Password, Google and Jellyfin logins all issue the same bearer/refresh pair, auto-verify, and auto-link by email or Jellyfin user id."),
            ("Secrets are never stored raw", "Tokens and keys are sha256-hashed at rest; passwords use PBKDF2 with a random salt. Dev tokens can be injected from env for local testing only."),
            ("CSRF only where cookies are", "Cookie auth pairs with a double-submit CSRF cookie and header. Header-based auth is exempt because it is not cookie-based."),
            ("Boring schema management", "<span class=\"mono\">CREATE TABLE IF NOT EXISTS</span> on boot, plus an additive migration script guarded by column checks. No ORM, no migration framework."),
            ("Errors have one shape", "Services raise <span class=\"mono\">ValueError</span>; controllers map to HTTP. Web routes redirect to login rather than raising 401."),
        ],
        api_title="API", api_head=["Method", "Path", "Description"],
        api=[("POST", "/auth/register", "Create an account, send verification"),
             ("POST", "/auth/login", "Password login → bearer + refresh, sets cookie"),
             ("POST", "/auth/refresh", "Rotate tokens per revocation policy"),
             ("POST", "/auth/logout", "Revoke current or all tokens"),
             ("GET", "/auth/google/start → /auth/google/callback", "Google OAuth"),
             ("POST", "/auth/jellyfin/login", "Jellyfin credentials → same token pair"),
             ("GET", "/apps", "Apps visible to the principal"),
             ("GET", "/apps/{app_id}/roles", "Roles defined by an app"),
             ("GET", "/admin/…", "Platform-wide (super_admin) or app-scoped (app admin)"),
             ("GET", "/web/…", "Server-rendered console")],
        run="""make install
cp .env.example .env
make migrate
make dev
make seed-admin USER_ID=user:your-id""",
        ops=[("hosts", "console.theogalh.dev · api.console.theogalh.dev"), ("db", "./data/theoapi.db"),
             ("env", "OAuth Google · SMTP · Jellyfin · token TTLs"), ("migrate", "scripts/migrate_db.py, idempotent"),
             ("tests", "make test wired, suite not yet written")],
    ),
]


def index_page():
    cards = "".join(f"""
      <div class="app-card anim-rise">
        <div class="head"><span class="applogo">{p["letter"]}</span><h3>{p["name"]}</h3><span class="dot ok"></span></div>
        <p class="stack">{p["card_stack"]}</p>
        <p>{p["card"]}</p>
        <a class="open" href="projects/{p["slug"]}.html">Open →</a>
      </div>""" for p in PROJECTS)

    body = f"""
  <section class="hero" id="about">
    <div>
      <p class="eyebrow">theogalh.dev · Thomas</p>
      <h1 class="display">Senior software engineer. I build small tools that ship.</h1>
      <p class="sub">Python, TypeScript, event-driven backends on GCP and AWS. Ten years in. Everything below runs on my own infrastructure, from the same project framework.</p>
      <div class="contact">
        <a href="mailto:theogalh.dev@gmail.com"><span class="k">mail</span>theogalh.dev@gmail.com</a>
        <a href="https://github.com/Theogalh"><span class="k">github</span>Theogalh</a>
        <a href="https://www.linkedin.com/in/thomas-bouillon-dev/"><span class="k">linkedin</span>thomas-bouillon-dev</a>
      </div>
    </div>
    <div class="hero-art"><img src="{AVATAR}" alt="Thomas, illustrated" width="760" height="567"></div>
  </section>

  <section class="section">
    <div class="stats-grid stagger">
      <div class="stat-card anim-rise"><div class="stat-label">Projects</div><div class="stat-value">{len(PROJECTS)}</div><div class="stat-delta"><span class="dot ok"></span> all running</div></div>
      <div class="stat-card anim-rise"><div class="stat-label">Experience</div><div class="stat-value">10 y</div><div class="stat-delta muted">python · typescript · cloud</div></div>
      <div class="stat-card anim-rise"><div class="stat-label">Runs on</div><div class="stat-value">LXC</div><div class="stat-delta muted">self-hosted, systemd + nginx</div></div>
      <div class="stat-card anim-rise"><div class="stat-label">Scaffolded by</div><div class="stat-value">1 CLI</div><div class="stat-delta muted">theoproject</div></div>
    </div>
  </section>

  <section class="section" id="projects">
    <h2 class="section-title">Projects</h2>
    <p class="muted" style="margin-bottom:16px">Each page has a plain-language overview and a full technical section: stack, architecture, decisions, API, deploy.</p>
    <div class="apps-grid stagger">{cards}
    </div>
  </section>
"""
    return shell("Projects", body, depth=0, active="projects", context="home")


OUT = ROOT / "dist"
(OUT / "projects").mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(index_page())
(OUT / ".nojekyll").write_text("")
for p in PROJECTS:
    (OUT / "projects" / f"{p['slug']}.html").write_text(project_page(p))
print("built", len(PROJECTS) + 1, "pages")
