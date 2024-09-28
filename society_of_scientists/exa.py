from exa_py import Exa

# Instantiate the Exa client
exa = Exa("03af6e3c-7b7f-4d46-b541-6771b8a240e0")

# Basic Search
results_basic = exa.search("This is an Exa query:")

# Autoprompted Search
results_autoprompt = exa.search("autopromptable query", use_autoprompt=True)

# Search with Date Filters
results_date_filter = exa.search(
    "This is an Exa query:",
    start_published_date="2019-01-01",
    end_published_date="2019-01-31"
)

# Search with Domain Filters
results_domain_filter = exa.search(
    "This is an Exa query:",
    include_domains=["www.cnn.com", "www.nytimes.com"]
)

# Search and Get Text Contents
results_text_contents = exa.search_and_contents("This is an Exa query:")

# Search and Get Highlights
results_highlights = exa.search_and_contents("This is an Exa query:", highlights=True)

# Search and Get Contents with Options
results_contents_options = exa.search_and_contents(
    "This is an Exa query:",
    text={"include_html_tags": True, "max_characters": 1000},
    highlights={"highlights_per_url": 2, "num_sentences": 1, "query": "This is the highlight query:"}
)

# Find Similar Documents
results_similar = exa.find_similar("https://example.com")

# Find Similar Excluding Source Domain
results_similar_exclude = exa.find_similar("https://example.com", exclude_source_domain=True)

# Find Similar with Contents
results_similar_with_contents = exa.find_similar_and_contents("https://example.com", text=True, highlights=True)

# Get Text Contents
results_get_contents = exa.get_contents(["ids"])

# Get Highlights
results_get_highlights = exa.get_contents(["ids"], highlights=True)

# Get Contents with Options
results_get_contents_options = exa.get_contents(
    ["ids"],
    text={"include_html_tags": True, "max_characters": 1000},
    highlights={"highlights_per_url": 2, "num_sentences": 1, "query": "This is the highlight query:"}
)

# Get the Newest Content of the Results
results_newest_content = exa.search_and_contents(
    "This is an Exa query:",
    text=True,
    livecrawl_timeout=8000,  # default 10000
    livecrawl="always"
)
