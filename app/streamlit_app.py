from __future__ import annotations

import json
import os
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


APP_DIR = Path(__file__).resolve().parent
DEFAULT_API_URL = os.getenv("FANTASY_API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="The Black Ledger | Fantasy Worlds",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def read_asset(name: str) -> str:
    path = APP_DIR / name
    if not path.is_file():
        st.error(f"Required UI asset is missing: {name}")
        st.stop()
    return path.read_text(encoding="utf-8")


def build_embedded_page(api_url: str) -> str:
    html = read_asset("index.html")
    css = read_asset("style.css")
    javascript = read_asset("script.js")

    html, css_replacements = re.subn(
        r'<link\b[^>]*href=["\']style\.css["\'][^>]*>',
        lambda _: f"<style>\n{css}\n</style>",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    html, script_replacements = re.subn(
        r'<script\b[^>]*src=["\']script\.js["\'][^>]*>\s*</script>',
        "",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    fetch_bridge = f"""<script>
(() => {{
  const apiBase = {json.dumps(api_url.rstrip('/'))};
  const originalFetch = window.fetch.bind(window);
  window.fetch = (input, options) => {{
    const requestUrl = typeof input === 'string' ? input : input.url;
    if (requestUrl.startsWith('/worlds') || requestUrl.startsWith('/world/') || requestUrl === '/predict') {{
      return originalFetch(new URL(requestUrl, apiBase).toString(), options);
    }}
    return originalFetch(input, options);
  }};
}})();
</script>
<script>
{javascript}
</script>"""
    html, body_replacements = re.subn(
        r'</body\s*>',
        lambda _: f"{fetch_bridge}\n</body>",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    if css_replacements != 1 or script_replacements != 1 or body_replacements != 1:
        st.error(
            "Could not embed the original frontend assets. "
            "Expected one style.css link, one script.js reference, and a body close tag in index.html."
        )
        st.stop()
    return html


st.sidebar.markdown("### Backend connection")
api_url = st.sidebar.text_input(
    "FastAPI base URL",
    value=DEFAULT_API_URL,
    help="Local default: http://127.0.0.1:8000. For deployment, enter your hosted FastAPI URL.",
).strip().rstrip("/")
if not api_url.startswith(("http://", "https://")):
    st.sidebar.error("Enter a backend URL beginning with http:// or https://.")
    st.stop()

components.html(build_embedded_page(api_url), height=1120, scrolling=True)
