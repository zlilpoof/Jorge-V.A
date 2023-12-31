import openai
import config
import local_time
import weather
import schedule
import models
import context_sentences
import interface
import search

possible_matches = {}
possible_matches[0] = weather.weather()
possible_matches[1] = local_time.current_date_formatted()

openai.api_key = config.openai_api_key
def llm_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": f"Seu nome é {config.assistant_name} {config.assistant_lastname}."},
            {"role": "system", "content": f"Você é um assistente {config.assistant_humor}."},
            {"role": "system", "content": f"Hora atual: {local_time.current_hour()};"},
            {"role": "system", "content": f"Clima atual: {weather.weather()};"},
            {"role": "system", "content": f"Minha cidade é {config.city_name};"},
            {"role": "system", "content": f"Responda com girias; Exemplo: {config.assistant_slangs}."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        temperature=0.8,
    )
    return response['choices'][0]['message']['content']

def generate_response(user_prompt):
    j = 0
    it = 3
    possible_len = 5
    value_ref_cosine = 0.30
    value_ref_flux = 0.80
    user_prompt_encoded = models.model.encode(user_prompt)
    while j < len(models.encoded_words):
        if j < len(models.encoded_words):
            current_encoded_word = models.encoded_words[j]
            cosine_scores = models.util.cos_sim(user_prompt_encoded, current_encoded_word)
            print(cosine_scores)
            if cosine_scores > value_ref_cosine:
                value_ref_cosine = cosine_scores
                print(f"Cosine value change to: {value_ref_cosine}")
                print(f"Index: {j}")
                print(f"The possible answer is: {context_sentences.answers[j]}")
                answer_address = j
                if it < possible_len:
                    possible_matches[it] = context_sentences.answers[answer_address]
                    print(f"Stored correspondence: {context_sentences.answers[answer_address]}")
                    print(possible_matches)
                    it += 1
                else:
                    it = 0
                    possible_matches[it] = context_sentences.answers[answer_address]
                    print(f"Stored correspondence: {context_sentences.answers[answer_address]}")
                    print(possible_matches)
                    it += 1
        j += 1
    if value_ref_cosine >= value_ref_flux:
        return context_sentences.answers[answer_address]
    else:
        formated_possible_matches = format_possible_matches(possible_matches)
        print(f"List of possible matches: {formated_possible_matches};")
        search_result = search.search_duckduckgo(user_prompt)
        interface.show_message_search_result(f"Resultado da internet: {search_result.decode('utf-8')}")
        appointments_today = f"{local_time.day_string(local_time.current_day())} {schedule.list_appointments_with_day_and_month(local_time.current_day(), local_time.current_month())}"
        appointments_tomorrow = f"{local_time.day_string(local_time.current_day()+1)} {schedule.list_appointments_with_day_and_month(local_time.current_day()+1, local_time.current_month())}"
        if appointments_today != []:
            print("Appointments today not a EMPTY LIST")
            validated_appointments_today = f"Compromissos para hoje: {appointments_today};"
        if appointments_tomorrow != []:
            print("Appointments tomorrow not a EMPTY LIST")
            validated_appointments_tomorrow = f"Compromissos para amanhã: {appointments_tomorrow};"
        model_response = llm_response(f"Resultado da internet do dia {local_time.day_string(local_time.current_day())} {local_time.current_day()}/{local_time.current_month()}/{local_time.current_year()} (Utilize essa informação apenas se fizer sentido com a pergunta): {search_result}; {validated_appointments_today} {validated_appointments_tomorrow} Contexto (Utilize essa informação apenas se fizer sentido com a pergunta): {formated_possible_matches}; Pergunta: {user_prompt}.")
        print(f"Internet result: {local_time.day_string(local_time.current_day())} {local_time.current_day()}/{local_time.current_month()}/{local_time.current_year()} (Utilize essa informação apenas se fizer sentido com a pergunta): {search_result};")
        return model_response
    
def format_possible_matches(list_matches):
    list_of_possible_matches = " ".join(str(list_matches[k]) for k in list_matches)
    return list_of_possible_matches