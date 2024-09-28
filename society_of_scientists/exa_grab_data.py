from exa_py import Exa

exa = Exa(api_key="03af6e3c-7b7f-4d46-b541-6771b8a240e0")

result = exa.search_and_contents(
  "Search researchgate for papers on computational neuroscience.",
  type="neural",
  use_autoprompt=True,
  num_results=20,
  summary={
    "query": "Please provide only the Abstract of this paper."
  },
  category="research paper",
  exclude_domains=["en.wikipedia.org"],
  text={
    "include_html_tags": True
  },
  livecrawl="always",
  highlights=True,
  start_published_date="2019-09-01T04:00:01.000Z"
)

print(result)
