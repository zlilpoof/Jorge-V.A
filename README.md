# Criando um novo amigo - Assistente virtual

Olá, sou Florêncio Soares, um entusiasta de tecnologia de 22 anos e estudante de Engenharia de Software.
Recentemente, fui movido pela ideia de criar um assistente virtual que funcione por comandos de voz, com o objetivo de transformar minha casa em um ambiente inteligente e totalmente offline. No entanto, minha visão não se limita a um assistente virtual comum, como a Alexa ou o Google Assistente.
Quero um assistente que compreenda e se comunique em linguagem natural para a maior imersão e satisfação do usuário, se aproximando ao máximo do Jarvis (Assistente virtual do Iron Man).

Minha jornada de desenvolvimento teve início com a escolha cuidadosa das tecnologias. Para o reconhecimento de voz, optei pelo Vosk (https://alphacephei.com/vosk/) e seu modelo de linguagem em português, o vosk-model-small-pt-0.3. Para a compreensão do conteúdo falado, integrei um modelo treinado em português com base no Sentence Transformers (mpjan/msmarco-distilbert-base-tas-b-mmarco-pt-300k).
A ativação do assistente se dá por meio de uma frase-chave, neste caso, "Salve Jorge", que, quando detectada, desencadeia o início da captura de comandos do usuário, semelhante ao clássico "Ok Google". Assim que um novo comando é capturado, realiza-se uma comparação com comandos previamente estabelecidos, permitindo interações intuitivas e personalizadas.

# Exemplos:

    Usuário - “Quero cadastrar um compromisso”
        Vídeo de demonstração: https://youtu.be/gdE-0V3JtJk
		Jorge perguntará: “Que dia é seu compromisso?”
		Usuário - “12”
		Jorge perguntará: “De que mês?”
		Usuário - “10”
		Jorge perguntará: “Que hora?”
		Usuário - “18”
		Jorge perguntará: “O que fará nesse compromisso?”
		Usuário - “Irei ao mercado”
		Jorge responderá: “Compromisso registrado com sucesso para o dia 12/10”
		// Obs: A qualquer momento o usuário poderá dizer “cancelar” ou ficar em silêncio que a operação será cancelada sem efetuar qualquer registro.

    Usuário - “Quais compromissos tenho na data”
        Vídeo de demonstração: https://youtu.be/S7OzjHdE1m4
        Jorge perguntará: “Em qual dia?”
        Usuário - “12”
        Jorge perguntará: “Qual mês?”
        Usuário - “10”
        Jorge responderá: “(ID) Dia 12 do Mês 10, às 18 horas: Irei ao mercado”
        // Obs: Jorge listará todos os compromissos que a pessoa tiver registrado para o dia consultado.

    Usuário - “Quais meus compromissos”
        Vídeo de demonstração: https://youtu.be/nGqQ_0tmb3Y
        Jorge responderá: “(ID) Dia 12 do Mês 10, às 18 horas: irei ao mercado”
        // Obs: Jorge listará todos os compromissos que a pessoa tiver registrado.

	Usuário - “Deletar compromisso”
		Vídeo de Demonstração: https://youtu.be/NXu-a4ffbCE
		Jorge perguntará: “Qual compromisso quer deletar?”
		Usuário - “(ID)”
		Jorge responderá: “Compromisso (ID) deletado com sucesso.”
		// Obs: Jorge deletar apenas o compromisso do ID mencionado.
		// Obs: O usuário pode falar “Cancelar” e Jorge responderá: “Operação cancelada”

	Usuário - “Bom dia”
		Vídeo de demonstração: https://youtu.be/yUG7LNiBfco
		Jorge responderá: “Bom dia, hoje é Terça-Feira 10/10/2023.
        Clima em (Cidade desejada) Céu limpo, Temperatura: 29.96°C, Umidade: 42%
        Seus compromissos de hoje são 
        (ID): Dia 10 do Mês 10, às 18 horas: lavar roupa
        (ID): Dia 10 do Mês 10, às 19 horas: levar o cachorro para passear”
        // Obs: Jorge listará todos os compromissos que a pessoa tiver registrado para o dia atual.
	
Se não houver correspondência semântica entre a entrada do usuário e os comandos pré-estabelecidos, é realizada uma análise semântica para verificar se há correspondência de perguntas e respostas pré-estabelecidas.
Assim, se houver uma correspondência acima de 0.30 entre a entrada do usuário e alguma das perguntas pré-estabelecidas, a resposta dessa correspondência é armazenada em um dicionário que suporta 5 valores e voltamos ao loop, se for encontrada uma correspondência maior, a correspondência é armazenada na próxima posição, se o último valor armazenado for na posição 5, o valor da primeira posição é substituída até que todas as perguntas pré-estabelecidas sejam comparadas com a entrada do usuário e a melhor correspondência seja encontrada.
Se a melhor correspondência encontrada tiver uma pontuação acima de 0.80, essa correspondência é retornada ao usuário como resposta.

Se não houver correspondência acima de 0.80, entra em um fluxo de resposta da API da OPENAI utilizando o modelo gpt-3.5-turbo-0301 com texto de embasamento para a personalidade do assistente, 5 respostas pré-estabelecidas com maior correspondência, resultado de pesquisa na internet, hora atual, clima atual, compromissos do dia atual, compromissos do dia posterior e a entrada atual do usuário.
Após isso, o resultado do retorno da API da OPENAI é exibido ao usuário com sintetização de voz e impressão em campo dedicado na interface.

Exemplos de uso:

Se o usuário falar algo similar a “Que dia é hoje”, haverá uma alta correspondência semântica e será retornado a função tempo.data_atual_formatada que conterá ex: Terça-Feira 10/10/2023.
Vídeo de demonstração: https://youtu.be/2Jc86rD5zHM

Se o usuário falar algo similar a  “Como está o clima hoje”, haverá uma alta correspondência semântica e será retornado a função tempo.clima que responderá com o resultado coletado pela api da OpenWeatherMap.
Vídeo de demonstração: https://youtu.be/E-_2p17CA1E

Se o usuário perguntar algo similar a “Estou pensando em passear com o cachorro, acha uma boa ideia?”, a entrada do usuário irá no fluxo de geração de texto com todo o embasamento encontrado pela análise semântica, personalidade do assistente, resultado de pesquisa na internet, hora atual, clima atual, compromissos do dia atual, compromissos do dia posterior e a entrada atual do usuário.
Exemplo de resposta: Pode crer, mano! Dar um rolê com o Akamaru é uma baita ideia. Além de ser um rolêzão, é um ótimo exercício pra ele e pra você também. Mas, não esquece de levar uns petiscos pra recompensar o bichinho! Ta ligado né?
Vídeo de demonstração: https://youtu.be/l-85IzoTbrw

# Conclusão

Em resumo, minha jornada de desenvolvimento para criar um assistente virtual com alto grau de imersão e comunicação em linguagem natural está progredindo de forma promissora. Até o momento, usei tecnologias como Vosk para o reconhecimento de voz e modelos treinados em português para a análise semântica e respostas personalizadas.
Embora meu objetivo final seja ter um assistente completamente offline, atualmente, devido a limitações técnicas, estou fazendo uso da API da OpenAI para a geração de texto. No entanto, isso não é um obstáculo, uma vez que minha solução ainda está em fase de desenvolvimento e, à medida que avanço, planejo realizar a implementação de modelos de processamento local para alcançar a independência completa da nuvem.
Acredito que esse projeto pode se tornar uma contribuição significativa para a integração de assistentes virtuais em casas inteligentes, proporcionando uma experiência de usuário excepcional, semelhante ao que vemos nos filmes de ficção científica. À medida que continuo aprimorando e desenvolvendo meu assistente virtual, estou empolgado para compartilhar com a comunidade de desenvolvedores e entusiastas de tecnologia os progressos e conquistas alcançados ao longo desta empolgante jornada.

# Agradecimentos

Gostaria de expressar minha sincera gratidão a Diego Recaman por fornecer generosamente uma chave de API da OpenAI, que foi fundamental para o desenvolvimento do meu assistente virtual.

Além disso, um agradecimento especial a Sthorm, que criou o som de responsividade do assistente, o característico "bip" que indica quando o assistente está pronto para ouvir comandos. Esse som tornou a interação com o assistente mais envolvente e intuitiva, proporcionando uma experiência mais agradável para os usuários.

Quero expressar minha gratidão a Ana Luiza por sua brilhante sugestão de adicionar gírias ao meu assistente virtual. Graças a ela, agora meu assistente é "descolado" e está totalmente "antenado" com a linguagem atual. 👌😎

Gostaria de expressar meu sincero agradecimento ao DALL-E 3 do Bing por sua incrível capacidade de criar a imagem visual do meu assistente.
Sua habilidade em transformar conceitos em representações visuais é verdadeiramente notável e contribuiu significativamente para a identidade e personalidade do meu assistente virtual.

Um super obrigado para o ChatGPT por criar essas frases de agradecimento. Sua contribuição na geração de palavras de apreço é inestimável e, sem dúvida, enriqueceu minha capacidade de expressar gratidão de forma eloquente.