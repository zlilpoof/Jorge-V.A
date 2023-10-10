from duckduckgo_search import DDGS
import tempo

def consultar_duckduckgo(prompt):
    dia_atual = tempo.dia_atual()
    mes_atual = tempo.mes_atual()
    ano_atual = tempo.ano_atual()
    pesquisa = f"{prompt} {dia_atual}/{mes_atual}/{ano_atual}"
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(pesquisa, max_results=1)]
    results_str = " ".join(results)
    encoded_results = results_str.encode('utf-8')
    
    return encoded_results