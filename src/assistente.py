import openai
from sentence_transformers import SentenceTransformer, util
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyttsx3
import tempo
import sons
import interface
import agenda
import pesquisa

speaker=pyttsx3.init()

speaker.setProperty('voice', 'Microsoft Maria Desktop - Portuguese(Brazil)')
rate = speaker.getProperty('rate')
speaker.setProperty('rate', rate-200)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)

stream.start_stream()

try:
    modelo_audio = Model("modelo")
    print("Model loaded successfully.")
except Exception as e:
    print("Failed to create a model:", str(e))
    exit(1)

rec = KaldiRecognizer(modelo_audio, 16000)

openai.api_key = "CHAVE_DA_API"
prompt = ""

tempo_hoje = tempo.clima()
dia_atual = tempo.dia_atual()
mes_atual = tempo.mes_atual()
compromissos_hoje = f"{tempo.dia_string()} {agenda.listar_compromissos_por_dia_mes(dia_atual, mes_atual)}"
compromissos_amanha = f"{tempo.dia_amanha_string()} {agenda.listar_compromissos_por_dia_mes(dia_atual + 1, mes_atual)}"
compromissos_deletados = agenda.deletar_compromisso_por_dia(dia_atual - 1)
print(compromissos_deletados)
print(compromissos_hoje)
print(compromissos_amanha)

palavras = {0:"Quem é seu criador?",
            1:"Qual o nome do cachorro do seu criador?",
            2:"Que dia é hoje",
            3:"Obrigado",
            4:"Qual é o seu nome",
            5:"Você está bem",
            6:"Como você está",
            7:"Que horas são",
            8:"Que hora é agora",
            9:"Qual a marca da ração do cachorro",
            10:"Qual a comida preferida do seu criador?",
            11:"como está o clima hoje",
            12:"quantos graus está hoje",
            13:"como está o tempo"
            }

respostas = {
            0:"Meu criador se chama Florencio Soares",
            1:"O nome do cachorro é Akamaru",
            2:tempo.data_atual_formatada(),
            3:"De nada",
            4:"Meu nome é Jorge, prazer.",
            5:"Estou ótimo, obrigado por perguntar",
            6:"Estou muito bem e você?",
            7:"Agora são " + tempo.hora_atual(),
            8:"Agora são " + tempo.hora_atual(),
            9:"A ração da Akamaru é a Golden Premier Pet",
            10:"A comida preferida do meu criador é Lasanha bolonhesa",
            11:tempo_hoje,
            12:tempo_hoje,
            13:tempo_hoje
            }

numeros_palavras = [
    "um",
    "dois",
    "tres",
    "quatro",
    "cinco",
    "seis",
    "sete",
    "oito",
    "nove",
    "dez",
    "onze",
    "doze",
    "treze",
    "quatorze",
    "quinze",
    "dezesseis",
    "dezessete",
    "dezoito",
    "dezenove",
    "vinte",
    "vinte e um",
    "vinte e dois",
    "vinte e tres",
    "vinte e quatro",
    "vinte e cinco",
    "vinte e seis",
    "vinte e sete",
    "vinte e oito",
    "vinte e nove",
    "trinta",
    "trinta e um"
]

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "Seu nome é Jorge."},
            {"role": "system", "content": "Você é um assistente engraçado."},
            {"role": "system", "content": f"Hora atual: {hora_agora};"},
            {"role": "system", "content": f"Clima atual: {tempo_hoje};"},
            {"role": "system", "content": f"Minha cidade é Uruguaiana;"},
            {"role": "system", "content": f"Compromissos para hoje: {compromissos_hoje};"},
            {"role": "system", "content": f"Compromissos para amanhã: {compromissos_amanha};"},
            {"role": "system", "content": "Responda com girias; Exemplo: Sim, mano; Pode crer; Ta ligado né; Poggers."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        temperature=0.8,
    )
    return response['choices'][0]['message']['content']

model = SentenceTransformer('mpjan/msmarco-distilbert-base-tas-b-mmarco-pt-300k')

possiveis_correspondencias = {}
possiveis_correspondencias[0] = tempo_hoje
possiveis_correspondencias[1] = tempo.data_atual_formatada()
palavras_encodadas = [None] * len(palavras)
numeros_palavras_encodadas = [None] * len(numeros_palavras)

x = 0
kj = 0

def format_respostas_possiveis():
    lista_respostas_possiveis = ""
    global possiveis_correspondencias
    print(possiveis_correspondencias)
    for k in possiveis_correspondencias:
        lista_respostas_possiveis = lista_respostas_possiveis + " " + str(possiveis_correspondencias[k])
    print(lista_respostas_possiveis)
    return lista_respostas_possiveis

for i in range(len(palavras)):
    palavras_encodadas[i] = model.encode(palavras[i])

for k in range(len(numeros_palavras)):
    numeros_palavras_encodadas[k] = model.encode(numeros_palavras[k])
    
def converter_numeros(numero_texto):
    numero_t = model.encode(numero_texto)
    g = 0
    valorRefCos = 0.30
    endereco_numero = 0
    while g < len(numeros_palavras_encodadas):
        if g < len(numeros_palavras_encodadas):
            numero_encodado = numeros_palavras_encodadas[g]
            cosine_scores = util.cos_sim(numero_t, numero_encodado)
            print(cosine_scores)
            if cosine_scores > valorRefCos:
                print("caiu no if", cosine_scores)
                valorRefCos = cosine_scores
                print("Valor cos alterado para: ", valorRefCos)
                print("o index dela é: ", g)
                print("A resposta é: ", numeros_palavras[g])
                endereco_numero = g
        g += 1
    return endereco_numero + 1

def responder(palavraRef):
    j = 0
    it = 3
    lenPossivel = 5
    valorRefCos = 0.30
    valorRefFlux = 0.80
    encodado2 = model.encode(palavraRef)
    while j < len(palavras_encodadas):
        if j < len(palavras_encodadas):
            encodado = palavras_encodadas[j]
            cosine_scores = util.cos_sim(encodado2, encodado)
            print(cosine_scores)
            if cosine_scores > valorRefCos:
                valorRefCos = cosine_scores
                print("Valor cos alterado para: ", valorRefCos)
                print("o index dela é: ", j)
                print("A resposta é: ", respostas[j])
                endereco_resposta = j
                if it < lenPossivel:
                    possiveis_correspondencias[it] = respostas[endereco_resposta]
                    print("#######################################")
                    print(f"Armazenado correspondência: {respostas[endereco_resposta]}")
                    print(possiveis_correspondencias)
                    print("#######################################")
                    it += 1
                else:
                    it = 0
                    possiveis_correspondencias[it] = respostas[endereco_resposta]
                    print("#######################################")
                    print(f"Armazenado correspondência: {respostas[endereco_resposta]}")
                    print(possiveis_correspondencias)
                    print("#######################################")
                    it += 1
        j += 1
    if valorRefCos >= valorRefFlux:
        return respostas[endereco_resposta]
    else:
        global compromissos_hoje
        global compromissos_amanha
        possiveis_respostas = format_respostas_possiveis()
        print("////////////////////////////////////////////////////////////////////////////")
        print(f"Possiveis respostas: {possiveis_respostas};")
        print("////////////////////////////////////////////////////////////////////////////")
        resultado_pesquisa = pesquisa.consultar_duckduckgo(palavraRef)
        interface.exibir_mensagem_chat3(f"Resultado da internet: {resultado_pesquisa.decode('utf-8')}")
        print(resultado_pesquisa)
        compromissos_hoje = f"{tempo.dia_string()} {agenda.listar_compromissos_por_dia_mes(dia_atual, mes_atual)}"
        compromissos_amanha = f"{tempo.dia_amanha_string()} {agenda.listar_compromissos_por_dia_mes(dia_atual + 1, mes_atual)}"
        retornoModelo = generate_response(f"Resultado da internet: {resultado_pesquisa}; Contexto: {possiveis_respostas}; Pergunta: {palavraRef}.")
        return retornoModelo

chamada = model.encode("Salve jorge")
sair_ref = model.encode("sair")
reg_compromisso = model.encode("Quero cadastrar um compromisso")
ler_compromissos = model.encode("Quais meus compromissos")
deletar_compromisso = model.encode("Deletar compromisso")
cancelar = model.encode("Cancelar")
consultar_compromissos = model.encode("Quais compromissos tenho na data")
bom_dia = model.encode("Bom dia")

def falar():
    global hora_agora
    global tempo_hoje
    global compromissos_hoje
    global compromissos_amanha
    respostas[7] = "Agora são " + tempo.hora_atual()
    respostas[8] = "Agora são " + tempo.hora_atual()
    hora_agora = tempo.hora_atual()
    if tempo.hora_atual() == "00:00:00" or tempo.hora_atual() == "03:00:00" or tempo.hora_atual() == "06:00:00" or tempo.hora_atual() == "09:00:00" or tempo.hora_atual() == "12:00:00" or tempo.hora_atual() == "15:00:00" or tempo.hora_atual() == "18:00:00" or tempo.hora_atual() == "21:00:00":
        tempo_hoje = tempo.clima()
        dia_atual = tempo.dia_atual()
        mes_atual = tempo.mes_atual()
        compromissos_hoje = f"{tempo.dia_string()} {agenda.listar_compromissos_por_dia_mes(dia_atual, mes_atual)}"
        compromissos_amanha = f"{tempo.dia_amanha_string()} {agenda.listar_compromissos_por_dia_mes(dia_atual + 1, mes_atual)}"
        agenda.deletar_compromisso_por_dia(dia_atual - 1)
    try:
        print("PODE FALAR")
        sons.bip()
    except OSError as e:
        print("Erro no audio")
    while True:
        try:
            data = stream.read(512)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_dict = json.loads(result)
                print(result_dict.get('text'))
                interface.exibir_mensagem_chat2(result_dict.get('text'))
                interacao_encodada = model.encode(result_dict.get('text'))
                saideira = util.cos_sim(sair_ref, interacao_encodada)
                registrar = util.cos_sim(reg_compromisso, interacao_encodada)
                ler_com = util.cos_sim(ler_compromissos, interacao_encodada)
                del_com = util.cos_sim(deletar_compromisso, interacao_encodada)
                com_data = util.cos_sim(consultar_compromissos, interacao_encodada)
                bom = util.cos_sim(bom_dia, interacao_encodada)
                print(f"Chance de sair de: {saideira}") 
                if saideira >= 0.90:
                    print(saideira)
                    break
                if com_data >= 0.80:
                    dia = falar_generico("Em qual dia?")
                    interface.exibir_mensagem_chat2(dia)
                    if dia != None:
                        mes = falar_generico("Qual mês?")
                        interface.exibir_mensagem_chat2(mes)
                        if mes != None:
                            dia_numero = converter_numeros(dia)
                            mes_numero = converter_numeros(mes)
                            compromissos_listados = agenda.listar_compromissos_por_dia_mes(dia_numero, mes_numero)
                            compromissos__listados_str = "\n".join(compromissos_listados)
                            interface.exibir_mensagem(compromissos__listados_str)
                            speaker.say(compromissos__listados_str)
                            speaker.runAndWait()
                    break
                elif bom >= 0.80:
                    dia_numero = tempo.dia_atual()
                    mes_numero = tempo.mes_atual()
                    data_atual = tempo.data_atual_formatada()
                    clima_atual = tempo.clima()
                    compromissos_listados = agenda.listar_compromissos_por_dia_mes(dia_numero, mes_numero)
                    compromissos__listados_str = "\n".join(compromissos_listados)
                    interface.exibir_mensagem(f"Bom dia, hoje é {data_atual}. {clima_atual}")
                    speaker.say(f"Bom dia, hoje é {data_atual}. {clima_atual}")
                    speaker.runAndWait()
                    interface.exibir_mensagem("Seus compromissos de hoje são")
                    speaker.say("Seus compromissos de hoje são")
                    speaker.runAndWait()
                    interface.exibir_mensagem(compromissos__listados_str)
                    speaker.say(compromissos__listados_str)
                    speaker.runAndWait()
                    break
                elif registrar >= 0.80:
                    print("CAIU NO CADASTRO DE AGENDA")
                    mes_compromisso = None
                    hora_compromisso = None
                    sobre_compromisso = None
                    dia_compromisso = falar_generico("Que dia é seu compromisso?")
                    interface.exibir_mensagem_chat2(dia_compromisso)
                    if dia_compromisso != None:
                        mes_compromisso = falar_generico("De que mês?")
                        interface.exibir_mensagem_chat2(mes_compromisso)
                        if mes_compromisso != None:
                            hora_compromisso = falar_generico("Que hora?")
                            interface.exibir_mensagem_chat2(hora_compromisso)
                            if hora_compromisso != None:
                                sobre_compromisso = falar_generico("O que fará nesse compromisso?")
                                interface.exibir_mensagem_chat2(sobre_compromisso)
                                if sobre_compromisso == None:
                                    interface.exibir_mensagem("Operação cancelada")
                                    speaker.say("Operação cancelada")
                                    speaker.runAndWait()
                            else:
                                interface.exibir_mensagem("Operação cancelada")
                                speaker.say("Operação cancelada")
                                speaker.runAndWait()
                        else:
                            interface.exibir_mensagem("Operação cancelada")
                            speaker.say("Operação cancelada")
                            speaker.runAndWait()
                    else:
                        interface.exibir_mensagem("Operação cancelada")
                        speaker.say("Operação cancelada")
                        speaker.runAndWait()
                        
                    if dia_compromisso != None and mes_compromisso != None and hora_compromisso != None and sobre_compromisso != None:
                        dia_convertido = converter_numeros(dia_compromisso)
                        mes_convertido = converter_numeros(mes_compromisso)
                        hora_convertida = converter_numeros(hora_compromisso)
                        status = agenda.registrar_compromisso(dia_convertido, mes_convertido, hora_convertida, sobre_compromisso)
                        interface.exibir_mensagem(f"{status} para o dia {dia_convertido} / {mes_convertido}")
                        speaker.say(f"{status} para o dia {dia_convertido} do {mes_convertido}")
                        speaker.runAndWait()
                    break
                elif ler_com >= 0.80:
                    print("CAIU NA LEITURA DE COMPROMISSOS")
                    compromissos = agenda.listar_compromissos()
                    print(compromissos)
                    if compromissos != []:
                        compromissos_str = "\n".join(compromissos)
                        print(compromissos_str)
                        interface.exibir_mensagem(compromissos_str)
                        speaker.say(compromissos_str)
                        speaker.runAndWait()
                    else:
                        interface.exibir_mensagem("Não há compromissos registrados")
                        speaker.say("Não há compromissos registrados")
                        speaker.runAndWait()
                    break
                elif del_com >= 0.80:
                    print("CAIU NO DELETE DE COMPROMISSOS")
                    alvo = falar_generico("Qual compromisso quer deletar?")
                    interface.exibir_mensagem("Qual compromisso quer deletar?")
                    interface.exibir_mensagem_chat2(alvo)
                    alvo_encodado = model.encode(alvo)
                    teste_sair = util.cos_sim(alvo_encodado, cancelar)
                    if teste_sair >= 0.70:
                        interface.exibir_mensagem("Operação cancelada")
                        speaker.say("Operação cancelada")
                        speaker.runAndWait()
                        break
                    else:
                        alvo_formatado = converter_numeros(alvo)
                        resultado = agenda.deletar_compromisso_por_id(alvo_formatado)
                        if resultado == True:
                            interface.exibir_mensagem(f"Compromisso {alvo_formatado} deletado com sucesso.")
                            speaker.say(f"Compromisso {alvo_formatado} deletado com sucesso.")
                            speaker.runAndWait()
                            break
                        else:
                            speaker.say(f"Ocorreu um erro ao deletar o compromisso {alvo_formatado}.")
                            speaker.runAndWait()
                            break
                else:
                    interface.exibir_mensagem_chat2(result_dict.get('text'))
                    resposta = responder(result_dict.get('text'))
                    interface.exibir_mensagem(resposta)
                    speaker.say(resposta)
                    speaker.runAndWait()
                    break
                    
        except OSError as e:
            print("OSError:", str(e))
            while stream.get_read_available() > 0:
                stream.read(stream.get_read_available())
                
def falar_generico(mensagem):
    try:
        interface.exibir_mensagem(mensagem)
        speaker.say(mensagem)
        speaker.runAndWait()
        print("PODE FALAR")
        sons.bip()
    except OSError as e:
        print("Erro no audio")
    while True:
        try:
            data = stream.read(512)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                resposta = rec.Result()
                resposta_dict = json.loads(resposta)
                print(resposta_dict.get('text'))
                interacao_encodada = model.encode(resposta_dict.get('text'))
                cancelar_ver = util.cos_sim(cancelar, interacao_encodada)
                print(f"Chance de cancelar de: {cancelar_ver}") 
                if cancelar_ver >= 0.90:
                    print(cancelar_ver)
                    break
                else:
                    if resposta_dict.get('text') != "":
                        return resposta_dict.get('text')
        except OSError as e:
            print("OSError:", str(e))
            while stream.get_read_available() > 0:
                stream.read(stream.get_read_available())
                
while True:
    try:
        data = stream.read(512)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result_dict = json.loads(result)
            entrada_usuario = result_dict.get('text')
            print(entrada_usuario)
            interacao_encodada = model.encode(result_dict.get('text'))
            pontuacao = util.cos_sim(chamada, interacao_encodada)
            print(f"Pontuação de: {pontuacao}")
            if pontuacao >= 0.70:
                print(pontuacao)
                print("Comando reconhecido!")
                falar()
    except OSError as e:
        print("OSError:", str(e))
        while stream.get_read_available() > 0:
            stream.read(stream.get_read_available())