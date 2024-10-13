from exa_py import Exa
import os

class ExaSearch:
    def __init__(self, api_key):
        """Initialize the ExaSearch class with an API key."""
        self.exa = Exa(api_key=api_key)
        self.result = None

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
            for entry in self.result.results:
                parsed_entry = {field: getattr(entry, field, None) for field in fields}
                parsed_data.append(parsed_entry)
        else:
            raise ValueError("No 'results' found in the response. Please check the search query or result structure.")
        
        return parsed_data

    def get_parsed_results(self, fields):
        """Return parsed results for further usage."""
        return self.parse_results(fields)

    def print_parsed_results(self, fields):
        """Print the parsed results for easy viewing."""
        parsed_results = self.parse_results(fields)
        for entry in parsed_results:
            print(entry)

    def export_results_to_file(self, fields, filename="search_results.txt"):
        """Export the parsed results to a text file."""
        parsed_results = self.parse_results(fields)
        # Get the current directory
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, filename)
        
        # Open the file with utf-8 encoding to handle all Unicode characters
        with open(file_path, 'w', encoding='utf-8') as file:
            for entry in parsed_results:
                for field, value in entry.items():
                    file.write(f"{field}: {value}\n")
                file.write("\n")
        
        print(f"Results exported to {file_path}")

if __name__ == "__main__":
    # Initialize the class with your API key
    search_tool = ExaSearch(api_key="03af6e3c-7b7f-4d46-b541-6771b8a240e0")
    
    # List of queries
    queries = [
        "computational neuroscience",
        "computer vision",
        "large language models",
        "hardware for AI"
    ]

    # List of result counts
    result_counts = [400]

    # Define fields to extract
    # fields_to_extract = ["title", "url", "publishedDate", "author", "summary"]
    fields_to_extract = ["summary"]

    # Loop over each query and result count, and export the results to files
    for query in queries:
        for count in result_counts:
            # Search for papers with the specific query and result count
            search_tool.search_papers(query, num_results=count)
            
            # Create a filename that includes the query and the result count
            query_clean = query.replace(" ", "_")
            filename = f"exported_{query_clean}_{count}.txt"
            
            # Export the results to a text file
            search_tool.export_results_to_file(fields_to_extract, filename=filename)
            
            print(f"Exported {count} results for query '{query}' to {filename}")
