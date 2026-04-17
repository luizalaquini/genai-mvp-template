"""Example tools — replace these with your own implementations."""
from datetime import date


def get_current_date() -> dict:
    """Returns the current date."""
    return {"date": date.today().isoformat()}


def search_web(query: str) -> dict:
    """Web search stub — implement with your preferred API."""
    # Example: integrate with Tavily, Brave Search, SerpAPI...
    return {"results": f"[stub] Results for: {query}"}
