from newsapi import NewsApiClient
from rebranding_app import config

def get_latest_news():
    try:
        newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)
        sources_response = newsapi.get_sources(country="us")
        sources = sources_response.get("sources", [])
        return sources
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
