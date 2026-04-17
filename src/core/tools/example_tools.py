"""Ferramentas de exemplo — substitua pelas suas."""
from datetime import date


def get_current_date() -> dict:
    """Retorna a data atual."""
    return {"date": date.today().isoformat()}


def search_web(query: str) -> dict:
    """Stub de busca web — implemente com sua API preferida."""
    # Exemplo: integrar com Tavily, Brave Search, SerpAPI...
    return {"results": f"[stub] Resultados para: {query}"}
