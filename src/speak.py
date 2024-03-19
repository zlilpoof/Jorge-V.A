import interface
import models
import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import sounds
import json
import local_time
import schedule
import weather
import llm_response
from config import settings
import os


if not settings.debug_mode:
    model_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'modelo'))
    audio_model = Model(model_path)
    speaker=pyttsx3.init()
    speaker.setProperty('voice', 'Microsoft Maria Desktop - Portuguese(Brazil)')
    rate = speaker.getProperty('rate')
    speaker.setProperty('rate', rate-200)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)
    stream.start_stream()
    rec = KaldiRecognizer(audio_model, 16000)


def assistant_show_in_interface_and_speak(message):
    if settings.debug_mode or settings.sound_muted:
        interface.show_message_assistant(message)
    else:
        interface.show_message_assistant(message)
        speaker.say(message)
        speaker.runAndWait()


def interactive_speak(message, bip=True):
    if message:
        assistant_show_in_interface_and_speak(message)
    if bip and not settings.sound_muted and not settings.mic_muted and not settings.debug_mode:
        print("PODE FALAR")
        sounds.bip()
    while True:
        user_input = interface.get_user_input()
        if user_input != None:
            return user_input
        else:
            if not settings.mic_muted and not settings.debug_mode:
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
                        if formated_capture != "":
                            return formated_capture
                        break

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
            day_number = models.convert_numbers(day)
            if day_number is None:
                assistant_show_in_interface_and_speak(f"Operação cancelada")
                return
            month = interactive_speak("Em qual mês?")
            month_number = models.convert_numbers(month)
            if month_number is None:
                assistant_show_in_interface_and_speak(f"Operação cancelada")
                return
            listed_appointments = schedule.list_appointments_with_day_and_month(day_number, month_number)
            if not listed_appointments:
                assistant_show_in_interface_and_speak(f"Não há compromissos para o dia {day_number}/{month_number}")
            else:
                listed_appointments__str = "\n".join(listed_appointments)
                assistant_show_in_interface_and_speak(listed_appointments__str)
        elif good_morning >= 0.80:
            day, month, date = local_time.current_day(), local_time.current_month(), local_time.current_date_formatted()
            current_weather = weather.weather_verify()
            listed_appointments = schedule.list_appointments_with_day_and_month(day, month)
            listed_appointments__str = "\n".join(listed_appointments)
            assistant_show_in_interface_and_speak(f"Bom dia, hoje é {date}. {current_weather}")
            if listed_appointments__str != "":
                assistant_show_in_interface_and_speak("Seus compromissos de hoje são:")
                assistant_show_in_interface_and_speak(listed_appointments__str)
        elif register_appointment >= 0.80:
            day_appointment = interactive_speak("Que dia é seu compromisso?")
            converted_day = models.convert_numbers(day_appointment)
            if converted_day is None:
                assistant_show_in_interface_and_speak("Operação cancelada")
                return
            interface.show_message_user(f"{converted_day}")
            month_appointment = interactive_speak("De que mês?")
            converted_month = models.convert_numbers(month_appointment)
            if converted_month is None:
                assistant_show_in_interface_and_speak("Operação cancelada")
                return
            interface.show_message_user(f"{converted_month}")
            hour_appointment = interactive_speak("Que hora?")
            converted_hour = models.convert_numbers(hour_appointment)
            if converted_hour is None:
                assistant_show_in_interface_and_speak("Operação cancelada")
                return
            interface.show_message_user(f"{converted_hour}")
            appointment = interactive_speak("O que fará nesse compromisso?")
            if appointment is None:
                assistant_show_in_interface_and_speak("Operação cancelada")
                return
            interface.show_message_user(appointment)
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
            formated_choice = models.convert_numbers(choice)
            interface.show_message_user(f"{formated_choice}")
            encoded_choice = models.model.encode(choice)
            exit_test = models.util.cos_sim(encoded_choice, models.cancel_reference)
            if exit_test >= 0.70:
                assistant_show_in_interface_and_speak("Operação cancelada")
                return
            result = schedule.delete_appointment_by_id(formated_choice)
            if result:
                assistant_show_in_interface_and_speak(f"Compromisso {formated_choice} deletado com sucesso.")
            else:
                assistant_show_in_interface_and_speak(f"Ocorreu um erro ao deletar o compromisso {choice}.")
        else:
            interface.show_message_user(result)
            response = llm_response.generate_response(result)
            assistant_show_in_interface_and_speak(response)
                
                
def speak_loop():
    if settings.debug_mode or settings.mic_muted:
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
