import os
import re
import time
import hashlib
import uuid
import warnings
import logging
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit, quote, unquote, urldefrag

import requests
import ftfy
import pandas as pd
from bs4 import BeautifulSoup

from config import TIMEOUT, RETRY_WAIT, MAX_STEM_LEN, PRIMARY_LOADERS, ALLOWED_DOMAINS


def debug(msg):
    print(f"[DEBUG] {msg}")


def sanitize(name):
    name = re.sub(r'[<>:"/\\|?*\']', '', name)
    name = re.sub(r'[^0-9A-Za-z]+', '_', name)
    return name.strip('_').lower()


def sanitize_html_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def sanitize_pdf_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*\']', '', filename)
    filename = re.sub(r'[^a-zA-Z0-9]+', '_', filename)
    filename = filename.strip('_')
    return filename.lower()


def gen_unique(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(os.path.basename(path))
    parent = os.path.dirname(path)
    i = 1
    while True:
        candidate = os.path.join(parent, f"{base}_{i}{ext}")
        if not os.path.exists(candidate):
            return candidate
        i += 1


def truncate(s):
    return s if len(s) <= MAX_STEM_LEN else s[:MAX_STEM_LEN]


def fetch(url, save_dir, force: bool = False):
    fn = sanitize_html_filename(url.replace('https://', ''))
    fn = truncate(fn)
    save_path = Path(os.path.join(save_dir, f"{fn}.html"))

    if save_path.exists() and not force:
        try:
            html = save_path.read_text(encoding="utf-8")
        except Exception as e:
            debug(f"Error reading cached HTML from {save_path}: {e}")
            return None, save_path
        if not html:
            debug(f"Cached HTML at {save_path} is empty.")
            return None, save_path
        return BeautifulSoup(html, "html.parser"), save_path

    try:
        debug(f"Download HTML: {url}")
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        print(f"Fetch error: {e}")
        return None, None

    save_path.write_text(r.text, encoding="utf-8")
    return BeautifulSoup(r.text, "html.parser"), save_path


def download_pdf_with_retry(url, path):
    if os.path.isfile(path):
        debug(f"PDF already exists locally: {path}")
        return path

    for att in (1, 2):
        debug(f"Download attempt {att}: {url}")
        try:
            r = requests.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            if 'pdf' not in r.headers.get('Content-Type', '').lower():
                raise ValueError('Not PDF')
            with open(path, 'wb') as f:
                f.write(r.content)
            return path
        except Exception as e:
            debug(f"Error: {e}")
            if att == 1:
                time.sleep(RETRY_WAIT)

    return None


def load_pdf_pages(path):
    for Loader in PRIMARY_LOADERS:
        try:
            return Loader(path).load()
        except Exception as e:
            logging.debug(e)
    warnings.warn(f"All loaders failed for {path}")
    return []


_URL_RE       = re.compile(
    r'https?://\S+'               # full URLs with scheme
    r'|www\.\S+'                  # www-prefixed bare URLs
    r'|(?<!\w)[a-z0-9-]+\.[a-z]{2,6}(?:/\S+)+'  # bare domain + path (e.g. te.org/topics/cars)
    r'|(?<!\w)/(?:\S+/)+\S+\.(?:pdf|docx?|xlsx?|pptx?|csv|zip|html?)(?=\s|$)',  # file paths
    re.I
)
_EMAIL_RE     = re.compile(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', re.I)
_PHONE_RE     = re.compile(r'\+?[\d][\d\s\(\)\-\.]{6,18}[\d]')
_COPYRIGHT_RE = re.compile(r'©[^.\n]*\d{4}[^.\n]*', re.I)
_CTA_RE       = re.compile(
    r'\b(read more|view all|subscribe|click here|share this|back to top|download pdf)\b', re.I
)
# T&E site-wide topic-nav block that survives parse-time stripping on some pages
_TE_NAV_RE    = re.compile(
    r'\bView\s+all\b[^.]{0,20}?\bCars\b.*?\bVacancies\b[^.]*',
    re.I | re.S
)
# T&E organisation tagline that appears in footers / about-us sections
_TE_TAGLINE_RE = re.compile(
    r"Europe'?s\s+leading\s+advocates\s+for\s+clean\s+transport[^.]*\.",
    re.I
)
# "Further information" contact block: name + job title + Transport & Environment + social handles.
# [^.]{0,250}? ensures no sentence-ending period between the header and the org name,
# which prevents matching legitimate body text that mentions both phrases.
_TE_CONTACT_RE = re.compile(
    r'\bFurther\s+information[^.]{0,250}?Transport\s*&(?:\s*Environment)?[^.]{0,200}',
    re.I
)
# PDF footnote/table separator lines extracted as literal characters
_SEPARATOR_RE  = re.compile(r'[=_\-]{4,}')
# Concatenated chart axis labels / barcodes (8+ consecutive digits)
_DIGIT_RUN_RE  = re.compile(r'\b\d{8,}\b')


def clean_text(text):
    if not isinstance(text, str):
        return text
    text = ftfy.fix_text(text)
    text = unicodedata.normalize('NFC', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C')
    text = _URL_RE.sub('', text)
    text = _EMAIL_RE.sub('', text)
    text = _PHONE_RE.sub('', text)
    text = _COPYRIGHT_RE.sub('', text)
    text = _CTA_RE.sub('', text)
    text = _TE_NAV_RE.sub('', text)
    text = _TE_TAGLINE_RE.sub('', text)
    text = _TE_CONTACT_RE.sub('', text)
    text = _SEPARATOR_RE.sub('', text)
    text = _DIGIT_RUN_RE.sub('', text)
    text = re.sub(r'\s+([,\.;:])', r'\1', text)  # fix orphaned punctuation from removals
    return re.sub(r"\s+", " ", text).strip()


def dedup_sentences(text):
    """Remove duplicate sentences — targets repeating PDF headers/footers."""
    parts = text.split('. ')
    seen, out = set(), []
    for part in parts:
        key = part.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(part)
    return '. '.join(out)


def clean_url(url, base=None):
    if not isinstance(url, str):
        return url
    url = url.strip()
    url = ''.join(ch for ch in url if unicodedata.category(ch)[0] != 'C')
    if base:
        url = urljoin(base, url)
    url, _ = urldefrag(url)
    parts = urlsplit(url)
    path  = quote(unquote(parts.path), safe="/:@&=+$,-._~;")
    query = quote(unquote(parts.query), safe=":/@?&=+$,-._~;[]%")
    return urlunsplit((parts.scheme, parts.netloc, path, query, ""))


_BOILERPLATE_TAGS = frozenset(['script', 'style', 'iframe', 'noscript', 'nav', 'header', 'footer', 'aside'])
_BOILERPLATE_ROLES = frozenset(['navigation', 'banner', 'search', 'complementary'])
_BOILERPLATE_ID_RE = re.compile(
    r'site-header|site-footer|cookie|banner|breadcrumb|mega-menu|mobile-menu|nav-dropdown|site-nav',
    re.I
)
_BOILERPLATE_CLASS_RE = re.compile(
    r'\b(mega-menu|mobile-menu|nav-dropdown|site-nav|topic-filter|tag-filter|topics-nav)\b',
    re.I
)


def _main_content_node(soup):
    """Return the node most likely to contain the article body, progressively broader."""
    # T&E: article prose wrapper
    node = soup.find(class_=re.compile(r'\bc_Prose\b'))
    if node:
        return node
    # CCC (Elementor): wp-post data attribute
    node = soup.find(attrs={'data-elementor-type': 'wp-post'})
    if node:
        return node
    # Semantic HTML5
    for sel in ('main', 'article'):
        node = soup.find(sel)
        if node:
            return node
    return soup.body or soup


def html_to_plain(html):
    soup = BeautifulSoup(html, 'lxml')
    # Drop hidden elements
    for tag in soup.find_all(style=True):
        st = re.sub(r'\s+', '', tag['style'].lower())
        if 'display:none' in st or 'visibility:hidden' in st:
            tag.decompose()
    # Drop structural boilerplate
    for t in soup(_BOILERPLATE_TAGS):
        t.decompose()
    # Drop ARIA landmark roles used for nav/header divs that don't use semantic tags
    for tag in soup.find_all(role=True):
        if tag.get('role', '').strip().lower() in _BOILERPLATE_ROLES:
            tag.decompose()
    # Drop known boilerplate IDs (site-header, site-footer, etc.)
    for tag in soup.find_all(id=_BOILERPLATE_ID_RE):
        tag.decompose()
    # Drop known boilerplate CSS class patterns (mega-menu, topic-filter, etc.)
    for tag in soup.find_all(class_=True):
        if _BOILERPLATE_CLASS_RE.search(' '.join(tag.get('class', []))):
            tag.decompose()
    main = _main_content_node(soup)
    txt = main.get_text(' ', strip=True)
    return re.sub(r'\s+', ' ', txt)


def safe_filename_from_url(url: str, max_name_len: int = 50) -> str:
    base = os.path.basename(urlparse(url).path).lower()
    base = re.sub(r'[^A-Za-z0-9._-]+', '_', base)
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    # Split before truncating; replace dots in name so embedded .docx etc. don't bleed through
    name, _ = os.path.splitext(base)
    name = name.replace('.', '_')[:max_name_len]
    return f"{name}_{h}.pdf"


def clean_url_for_id(url: str) -> str:
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return f"{parsed.scheme.lower()}://{netloc}{path}"


def key_from_url(url: str) -> str:
    cleaned = clean_url_for_id(url)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, cleaned))


def register_doc(source_type, source_url, docs_csv, doc_url_to_id, fulltext="", local_fn=""):
    doc_id = key_from_url(source_url)
    if doc_id not in doc_url_to_id:
        doc_url_to_id[doc_id] = True
        pd.DataFrame([{
            'Doc ID': doc_id,
            'Source Type': source_type,
            'Source URL': source_url,
            'Local Filename': local_fn,
            'Status': 'fetched' if fulltext else 'pending',
            'Fetched At': datetime.utcnow().isoformat(timespec='seconds') if fulltext else '',
            'Text Hash': hashlib.sha256(fulltext.encode('utf-8')).hexdigest() if fulltext else '',
            'Fulltext': fulltext,
        }]).to_csv(docs_csv, mode='a', header=False, index=False)
    return doc_id


def filter_min_length(text: str, min_chars: int) -> bool:
    return len(text.strip()) >= min_chars


def filter_symbol_ratio(text: str, max_ratio: float) -> bool:
    if not text:
        return False
    non_alnum_ws = sum(1 for c in text if not c.isalnum() and not c.isspace())
    return non_alnum_ws / len(text) <= max_ratio


def filter_alpha_ratio(text: str, min_ratio: float) -> bool:
    if not text:
        return False
    return sum(c.isalpha() for c in text) / len(text) >= min_ratio


def filter_mean_word_length(text: str, min_wl: float, max_wl: float) -> bool:
    words = text.split()
    if not words:
        return False
    mean = sum(len(w) for w in words) / len(words)
    return min_wl <= mean <= max_wl


def filter_line_repetition(text: str, max_dup_ratio: float) -> bool:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return False
    return (len(lines) - len(set(lines))) / len(lines) <= max_dup_ratio


def filter_unexpected_charset(text: str, max_foreign_ratio: float) -> bool:
    if not text:
        return False
    foreign = sum(1 for c in text if unicodedata.category(c) == 'Lo' and ord(c) > 0x2000)
    return foreign / len(text) <= max_foreign_ratio


def filter_org_affiliation(text: str, keywords: list) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in keywords)


def is_allowed_url(url: str) -> bool:
    try:
        return urlparse(url).netloc.lower() in ALLOWED_DOMAINS
    except Exception:
        return False


def parse_publication_date(val):
    if not isinstance(val, str):
        return None
    replacements = {
        "janv.": "Jan", "févr.": "Feb", "mars": "Mar", "avr.": "Apr",
        "mai": "May", "juin": "Jun", "juil.": "Jul", "août": "Aug",
        "sept.": "Sep", "oct.": "Oct", "nov.": "Nov", "déc.": "Dec",
    }
    for fr, en in replacements.items():
        val = val.replace(fr, en)
    val = re.sub(r'\s+', ' ', val.strip())
    val = re.sub(r',', '', val)
    try:
        if re.match(r"^\d{4}-\d{2}-\d{2}T", val):
            dt = pd.to_datetime(val, errors="coerce")
        else:
            dt = pd.to_datetime(val, dayfirst=True, errors="coerce")
        if not pd.isna(dt):
            return dt.isoformat()
    except Exception:
        pass
    print(f"Failed to parse {val}")
    return None
