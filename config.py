import os
from langchain_community.document_loaders import PDFMinerLoader, PyPDFLoader, PDFPlumberLoader

# — SOURCES —
HTML_SOURCES = [
    {'office': 'France',   'source_dir': r'data\france',   'base_url': 'https://www.transportenvironment.org/te-france/articles'},
    {'office': 'Brussels', 'source_dir': r'data\brussels', 'base_url': 'https://www.transportenvironment.org/articles'},
    {'office': 'Germany',  'source_dir': r'data\germany',  'base_url': 'https://www.transportenvironment.org/te-deutschland/articles'},
]
CCC_SOURCE = {
    'office': 'Clean Cities',
    'source_dir': r'data\ccc',
    'api_url': 'https://cleancitiescampaign.org/wp-json/wp/v2/posts',
    'per_page': 100,
    'statuses': ['publish'],
    'categories': [],
}

BASE_URL_TE  = "https://www.transportenvironment.org"
BASE_URL_CCC = "https://cleancitiescampaign.org/"

ALLOWED_DOMAINS = {
    "www.transportenvironment.org",
    "cleancitiescampaign.org",
    "www.cleancitiescampaign.org",
    "te-cdn.ams3.digitaloceanspaces.com",
    "te-cdn.ams3.cdn.digitaloceanspaces.com",
    "113.wpcdnnode.com",
}

# — PATHS —
OUTPUT_BASE       = "output"
HTML_SAVE_BASE    = "html"
PDF_BASE          = "pdf"

ARTICLES_CSV          = os.path.join(OUTPUT_BASE, "articles.csv")
DOCS_RAW_PARQUET      = os.path.join(OUTPUT_BASE, "docs_raw.parquet")
DOCS_FILTERED_PARQUET = os.path.join(OUTPUT_BASE, "docs_filtered.parquet")
FILTER_LOG_CSV        = os.path.join(OUTPUT_BASE, "filter_log.csv")
ART_DOCS_CSV          = os.path.join(OUTPUT_BASE, "article_docs.csv")

INDEX_OUT         = os.path.join(OUTPUT_BASE, "multilingual-e5-small-docs.index")
MAP_OUT           = os.path.join(OUTPUT_BASE, "multilingual-e5-small-faiss_mapping.csv")
MAP_PARQUET_OUT   = os.path.join(OUTPUT_BASE, "multilingual-e5-small-faiss_mapping.parquet")
PAGES_PARQUET_OUT = os.path.join(OUTPUT_BASE, "metadata_with_fulltext.parquet")

# — SCRAPING SETTINGS —
SAFETY_WAIT  = 2    # seconds between requests
TIMEOUT      = 10   # HTTP request timeout (seconds)
RETRY_WAIT   = 2    # seconds before retry on download failure
MAX_STEM_LEN = 150  # max filename stem length

# — PDF LOADERS (tried in order) —
PRIMARY_LOADERS = [PDFMinerLoader, PyPDFLoader, PDFPlumberLoader]

# — EMBEDDING SETTINGS —
MODEL_NAME    = "intfloat/multilingual-e5-small"
CHUNK_SIZE    = 1024
CHUNK_OVERLAP = 0
INCREMENTAL   = True

SIMILARITY_THRESHOLD = 0.05
EMBED_BATCH_SIZE     = 64

# — FILTER THRESHOLDS —
FILTER_MIN_CHARS          = 500
CHUNK_MIN_CHARS           = 100
FILTER_MAX_SYMBOL_RATIO   = 0.15
FILTER_MIN_ALPHA_RATIO    = 0.60
FILTER_WORD_LEN_MIN       = 3.0
FILTER_WORD_LEN_MAX       = 15.0
FILTER_MAX_LINE_DUP_RATIO = 0.30
FILTER_MAX_FOREIGN_RATIO  = 0.05
DEDUP_JACCARD_THRESHOLD   = 0.85
DEDUP_NUM_PERM            = 128

ORG_KEYWORDS = [
    "transport & environment",
    "transport and environment",
    "t&e",
    "t & e",
    "clean cities campaign",
    "clean cities",
    "ccc"
]

# — WIKI SETTINGS —
WIKI_BASE          = "wiki"
WIKI_SOURCES_DIR   = os.path.join(WIKI_BASE, "sources")
WIKI_TOPICS_DIR    = os.path.join(WIKI_BASE, "topics")
WIKI_SUBSET_FILTER = "Simon Suzan"  # substring match on fulltext; test-subset heuristic only

# — PUBLICATION TYPE NORMALISATION —
pub_type_map = {
    # French
    "Communiqué de presse": "Press release",
    "Rapport": "Report",
    "Briefing": "Briefing",
    "Lettre": "Letter",
    "Publications": "Publication",
    "Tribunes": "Op-ed",
    "Nouvelles": "News",
    # English
    "Unknown Type": "News",
    "Opinion": "Op-ed",
    "Letter": "Letter",
    "Press Release": "Press release",
    "Report": "Report",
    "News": "News",
    "Consultation response": "Consultation response",
    "Publication": "Publication",
    "post": "Post",
    # German
    "Pressemitteilung": "Press release",
    "Meinung": "Op-ed",
    "Aktuelle Meldungen": "News",
    "Publikationen": "Publication",
    "Offener Brief": "Open letter",
    "Bericht": "Report",
}
