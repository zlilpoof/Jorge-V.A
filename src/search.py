from duckduckgo_search import DDGS
import local_time
import config

def search_duckduckgo(prompt):
    search = f"{prompt} {local_time.current_day()}/{local_time.current_month()}/{local_time.current_year()}"
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(search, max_results=config.search_max_results)]
    results_str = " ".join(results)
    encoded_results = results_str.encode('utf-8')
    return encoded_results
