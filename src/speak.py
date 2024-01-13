import interface
import models
import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import sounds
import json
import context_sentences
import local_time
import schedule
import weather
import llm_response
import config

if not config.debug_mode:
    audio_model = Model("modelo")
    speaker=pyttsx3.init()
    speaker.setProperty('voice', 'Microsoft Maria Desktop - Portuguese(Brazil)')
    rate = speaker.getProperty('rate')
    speaker.setProperty('rate', rate-200)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)
    stream.start_stream()
    rec = KaldiRecognizer(audio_model, 16000)

def assistant_show_in_interface_and_speak(message):
    if config.debug_mode:
        interface.show_message_assistant(message)
    else:
        interface.show_message_assistant(message)
        speaker.say(message)
        speaker.runAndWait()

def interactive_speak(message, bip=True):
    assistant_show_in_interface_and_speak(message)
    if bip:
        print("PODE FALAR")
        sounds.bip()
    while True:
        user_input = interface.get_user_input()
        if user_input != None:
            print(user_input)
            return user_input
        else:
            if not config.debug_mode:
                try:
                    data = stream.read(512)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        captured = rec.Result()
                        captured_dict = json.loads(captured)
                        print(captured_dict.get('text'))
                        formated_capture = captured_dict.get('text')
                        encoded_interaction = models.model.encode(formated_capture)
                        cancel = models.util.cos_sim(models.cancel_reference, encoded_interaction)
                        print(f"Chance de cancelar de: {cancel}") 
                        if cancel >= 0.90:
                            print(cancel)
                            break
                        else:
                            if formated_capture != "":
                                return formated_capture
                except OSError as e:
                    print("OSError:", str(e))
                    while stream.get_read_available() > 0:
                        stream.read(stream.get_read_available())
def menu():
    if local_time.complete_current_time() == "00:00:00":
        print(f"Appointment deleted: {schedule.delete_appointment_by_day(local_time.current_day()-1)}")
    result = interactive_speak("")
    print(result)
    if result:
        interface.show_message_user(result)
        encoded_result = models.model.encode(result)
        exit = models.util.cos_sim(models.exit_reference, encoded_result)
        register_appointment = models.util.cos_sim(models.register_appointment_reference, encoded_result)
        read_appointments = models.util.cos_sim(models.read_appointment_reference, encoded_result)
        delete_appointment = models.util.cos_sim(models.delete_appointment_reference, encoded_result)
        read_appointment_by_data = models.util.cos_sim(models.read_appointment_by_data_reference, encoded_result)
        good_morning = models.util.cos_sim(models.good_morning_reference, encoded_result)
        print(f"Chance de sair de: {exit}") 
        if exit >= 0.90:
            print("user exit")
        if read_appointment_by_data >= 0.80:
            day = interactive_speak("Em qual dia?")
            if day != None:
                month = interactive_speak("Em qual mês?")
                if month != None:
                    day_number = models.convert_numbers(day)
                    month_number = models.convert_numbers(month)
                    listed_appointments = schedule.list_appointments_with_day_and_month(day_number, month_number)
                    listed_appointments__str = "\n".join(listed_appointments)
                    assistant_show_in_interface_and_speak(listed_appointments__str)
        elif good_morning >= 0.80:
            day = local_time.current_day()
            month = local_time.current_month()
            date = local_time.current_date_formatted()
            current_weather = weather.weather_verify()
            listed_appointments = schedule.list_appointments_with_day_and_month(day, month)
            listed_appointments__str = "\n".join(listed_appointments)
            assistant_show_in_interface_and_speak(f"Bom dia, hoje é {date}. {current_weather}")
            if listed_appointments__str != "":
                assistant_show_in_interface_and_speak("Seus compromissos de hoje são")
                assistant_show_in_interface_and_speak(listed_appointments__str)
        elif register_appointment >= 0.80:
            month_appointment = None
            hour_appointment = None
            appointment = None
            day_appointment = interactive_speak("Que dia é seu compromisso?")
            interface.show_message_user(day_appointment)
            if day_appointment != None:
                month_appointment = interactive_speak("De que mês?")
                interface.show_message_user(month_appointment)
                if month_appointment != None:
                    hour_appointment = interactive_speak("Que hora?")
                    interface.show_message_user(hour_appointment)
                    if hour_appointment != None:
                        appointment = interactive_speak("O que fará nesse compromisso?")
                        interface.show_message_user(appointment)
                        if appointment == None:
                            assistant_show_in_interface_and_speak("Operação cancelada")
                    else:
                        assistant_show_in_interface_and_speak("Operação cancelada")
                else:
                    assistant_show_in_interface_and_speak("Operação cancelada")
            else:
                assistant_show_in_interface_and_speak("Operação cancelada")
                
            if day_appointment != None and month_appointment != None and hour_appointment != None and appointment != None:
                converted_day = models.convert_numbers(day_appointment)
                converted_month = models.convert_numbers(month_appointment)
                converted_hour = models.convert_numbers(hour_appointment)
                status = schedule.register_appointment(converted_day, converted_month, converted_hour, appointment)
                assistant_show_in_interface_and_speak(f"{status} para o dia {converted_day} do {converted_month}")
        elif read_appointments >= 0.80:
            appointments = schedule.list_appointments()
            if appointments != []:
                appointments_str = "\n".join(appointments)
                print(appointments_str)
                assistant_show_in_interface_and_speak(appointments_str)
            else:
                assistant_show_in_interface_and_speak("Não há compromissos registrados")
        elif delete_appointment >= 0.80:
            choice = interactive_speak("Qual compromisso quer deletar?")
            assistant_show_in_interface_and_speak("Qual compromisso quer deletar?")
            interface.show_message_user(choice)
            encoded_choice = models.model.encode(choice)
            exit_test = models.util.cos_sim(encoded_choice, models.cancel_reference)
            if exit_test >= 0.70:
                assistant_show_in_interface_and_speak("Operação cancelada")
            else:
                formated_choice = models.convert_numbers(choice)
                result = schedule.delete_appointment_by_id(formated_choice)
                if result == True:
                    assistant_show_in_interface_and_speak(f"Compromisso {formated_choice} deletado com sucesso.")
                else:
                    assistant_show_in_interface_and_speak(f"Ocorreu um erro ao deletar o compromisso {formated_choice}.")
        else:
            interface.show_message_user(result)
            response = llm_response.generate_response(result)
            assistant_show_in_interface_and_speak(response)
                
def speak_loop():
    if config.debug_mode:
        menu()
    else:
        try:
            user_input = interactive_speak("", False)
            if user_input != "" and user_input != None:
                encoded_input = models.model.encode(user_input)
                call_action_probability = models.util.cos_sim(models.call_action, encoded_input)
                print(f"Activation probability: {call_action_probability}")
                if call_action_probability >= 0.70:
                    print("Command recognized!")
                    menu()
        except OSError as e:
            print("OSError:", str(e))
            while stream.get_read_available() > 0:
                stream.read(stream.get_read_available())