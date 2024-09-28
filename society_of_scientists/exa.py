from exa_py import Exa

class ExaSearch:
    def __init__(self, api_key):
        """Initialize the ExaSearch class with an API key."""
        self.exa = Exa(api_key=api_key)

    def search_papers(self, query, search_type="neural", num_results=2, category="research paper", start_date="2019-09-01T04:00:01.000Z", autoprompt=True, exclude_domains=None, include_html_tags=True, livecrawl="always", highlights=True):
        """Search for papers based on the provided parameters."""
        # Perform search and get results
        if exclude_domains is None:
            exclude_domains = ["en.wikipedia.org"]
        
        self.result = self.exa.search_and_contents(
            query,
            type=search_type,
            use_autoprompt=autoprompt,
            num_results=num_results,
            summary={
                "query": "Please provide only the Abstract of this paper."
            },
            category=category,
            exclude_domains=exclude_domains,
            text={
                "include_html_tags": include_html_tags
            },
            livecrawl=livecrawl,
            highlights=highlights,
            start_published_date=start_date
        )
        return self.result

    def parse_results(self, fields):
        """Parse the search results and extract specified fields."""
        parsed_data = []
        if hasattr(self.result, 'results'):
            # Access the 'results' attribute of the SearchResponse object
            for entry in self.result.results:
                parsed_entry = {field: getattr(entry, field, None) for field in fields}
                parsed_data.append(parsed_entry)
        else:
            raise ValueError("No 'results' found in the response. Please check the search query or result structure.")
        
        return parsed_data

    def print_parsed_results(self, fields):
        """Print the parsed results for easy viewing."""
        parsed_results = self.parse_results(fields)
        for entry in parsed_results:
            print(entry)

# Example usage of the class
if __name__ == "__main__":
    # Initialize the class with your API key
    search_tool = ExaSearch(api_key="03af6e3c-7b7f-4d46-b541-6771b8a240e0")
    
    # Search for papers
    search_tool.search_papers("Search researchgate for papers on computational neuroscience.", num_results=2)
    
    # Define fields to extract
    fields_to_extract = ["title", "url", "publishedDate", "author", "summary"]
    
    # Print parsed results
    search_tool.print_parsed_results(fields_to_extract)
