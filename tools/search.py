import logging
from ddgs import DDGS

logger = logging.getLogger("ADK_Tools")


def duckduckgo_search(query: str, max_results: int = 5) -> str:
    """Performs a web search using DuckDuckGo and returns the top results.

    Args:
        query: The search string/keywords.
        max_results: The maximum number of search results to return.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return "No search results found."

            formatted_results = []
            for r in results:
                title = r.get("title", "")
                snippet = r.get("body", "")
                link = r.get("href", "")
                formatted_results.append(
                    f"Title: {title}\nSnippet: {snippet}\nURL: {link}"
                )

            return "\n\n".join(formatted_results)
    except Exception as e:
        error_msg = f"Error executing DuckDuckGo Search: {str(e)}"
        logger.error(error_msg)
        return error_msg
