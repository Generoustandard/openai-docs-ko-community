from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import tempfile
from pathlib import Path
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from mvp.text_utils import normalize_prose


ARTICLE_BLOCK_SCRIPT = r"""
const article = document.querySelector('article');
const body = article && article.children && article.children[1];
if (!article || !body) {
  return null;
}

const blocks = [];
for (const el of body.querySelectorAll('p, li, h2, h3, h4')) {
  if (el.closest('pre, code')) {
    continue;
  }

  const rawText = (el.innerText || '').replace(/\u2060/g, '').trim();
  if (!rawText) {
    continue;
  }

  const domPath = [];
  let node = el;
  while (node && node !== body) {
    const parent = node.parentElement;
    if (!parent) {
      break;
    }
    const index = Array.from(parent.children).indexOf(node);
    domPath.unshift(`${node.tagName}:${index}`);
    node = parent;
  }

  blocks.push({
    tag: el.tagName,
    raw_text: rawText,
    dom_path: domPath.join('>')
  });
}

return {
  title: document.title,
  final_url: window.location.href,
  article_text: (article.innerText || '').replace(/\u2060/g, '').trim(),
  blocks
};
"""


@dataclass(frozen=True)
class PageLocale:
    code: str
    accept_languages: str


EN_LOCALE = PageLocale(code="en-US", accept_languages="en-US,en")
KO_LOCALE = PageLocale(code="ko-KR", accept_languages="ko-KR,ko,en-US,en")


def _build_options(profile_dir: Path, locale: PageLocale, headless: bool) -> Options:
    options = Options()
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument(f"--lang={locale.code}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,1200")
    if headless:
        options.add_argument("--headless=new")
    options.add_experimental_option(
        "prefs",
        {"intl.accept_languages": locale.accept_languages},
    )
    return options


def _wait_for_article(driver: webdriver.Chrome, timeout_seconds: int) -> None:
    wait = WebDriverWait(driver, timeout_seconds)

    def _title_ready(current_driver: webdriver.Chrome) -> bool:
        title = current_driver.title or ""
        blocked_titles = {"Just a moment...", "잠시만 기다리십시오…"}
        return title not in blocked_titles

    wait.until(_title_ready)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))


def fetch_page_snapshot(
    *,
    url: str,
    locale: PageLocale,
    headless: bool = False,
    timeout_seconds: int = 60,
) -> dict:
    profile_dir = Path(tempfile.mkdtemp(prefix="openai-docs-pair-"))
    driver = webdriver.Chrome(options=_build_options(profile_dir, locale, headless))

    try:
        driver.get(url)
        _wait_for_article(driver, timeout_seconds)
        payload = driver.execute_script(ARTICLE_BLOCK_SCRIPT)
        if not payload:
            raise RuntimeError(f"Failed to extract article payload from {url}")

        blocks = []
        for index, block in enumerate(payload["blocks"], start=1):
            clean_text = normalize_prose(block["raw_text"])
            if not clean_text:
                continue
            blocks.append(
                {
                    "index": index,
                    "tag": block["tag"],
                    "dom_path": block["dom_path"],
                    "raw_text": block["raw_text"],
                    "clean_text": clean_text,
                }
            )

        return {
            "requested_url": url,
            "final_url": payload["final_url"],
            "title": payload["title"],
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "article_text_raw": payload["article_text"],
            "article_text_clean": normalize_prose(payload["article_text"]),
            "block_count": len(blocks),
            "blocks": blocks,
            "html": driver.page_source,
        }
    finally:
        driver.quit()
        shutil.rmtree(profile_dir, ignore_errors=True)
