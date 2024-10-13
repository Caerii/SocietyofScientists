import requests
from exa_py import Exa
from autogen import ConversableAgent

# Define Exa Search API as a tool
def exa_search_tool(query):
    # Make Exa API call
    exa = Exa(api_key="03af6e3c-7b7f-4d46-b541-6771b8a240e0")
    result = exa.search_and_contents(
        query,
        type="neural",
        use_autoprompt=True,
        num_results=20,
        summary={
            "query": "What does this paper cover?"
        },
        category="research paper",
        exclude_domains=["en.wikipedia.org"],
        start_published_date="2023-01-01",
        text={
            "include_html_tags": True
        },
        livecrawl="always",
        highlights=True
    )
    return result

