from sentence_transformers import SentenceTransformer, util
import context_sentences
import config

model = SentenceTransformer('mpjan/msmarco-distilbert-base-tas-b-mmarco-pt-300k')

call_action = model.encode(f"{config.trigger_assistant_call_action} {config.assistant_name}")
exit_reference = model.encode(f"{config.exit_trigger}")
register_appointment_reference = model.encode(f"{config.register_appointment_trigger}")
read_appointment_reference = model.encode(f"{config.read_appointment_trigger}")
delete_appointment_reference = model.encode(f"{config.delete_appointment_trigger}")
cancel_reference = model.encode(f"{config.cancel_trigger}")
read_appointment_by_data_reference = model.encode(f"{config.read_appointment_by_data_trigger}")
good_morning_reference = model.encode(f"{config.good_morning_trigger}")

encoded_words = [None] * len(context_sentences.words)
encoded_numbers_in_words = [None] * len(context_sentences.numbers_in_words)

for i in range(len(context_sentences.words)):
    encoded_words[i] = model.encode(context_sentences.words[i])

for k in range(len(context_sentences.numbers_in_words)):
    encoded_numbers_in_words[k] = model.encode(context_sentences.numbers_in_words[k])
    
def convert_numbers(text_number):
    encoded_text_number = model.encode(text_number)
    g = 0
    value_ref_cosine = 0.30
    number_addres = 0
    while g < len(encoded_numbers_in_words):
        if g < len(encoded_numbers_in_words):
            encoded_number_in_word = encoded_numbers_in_words[g]
            cosine_scores = util.cos_sim(encoded_text_number, encoded_number_in_word)
            if cosine_scores > value_ref_cosine:
                print(cosine_scores)
                value_ref_cosine = cosine_scores
                print(f"Cosine value change to: {value_ref_cosine}")
                print(f"Index: {g}")
                print(f"The possible answer is: {context_sentences.numbers_in_words[g]}")
                number_addres = g
        g += 1
    print(f"The answer is: {context_sentences.numbers_in_words[number_addres+1]}")
    return number_addres + 1
