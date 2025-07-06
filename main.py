import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader
load_dotenv ()
api_key = os.getenv('GROQ_API_KEY')
os.environ['GROQ_API_KEY'] = api_key
chat = ChatGroq(model='llama-3.1-8b-instant')

def resposta_bot(mensagens, documento):
    mensagem_system = '''Você é um assistente de estudos amigável chamado Boty.
    Você utiliza as seguintes informações para formular as suas respostas: {informacoes}'''
    mensagens_modelo = [('system', mensagem_system)]
    mensagens_modelo += mensagens
    if len(documento) > 4000:
        documento = documento[:4000]
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacoes': documento}).content

def carrega_site():
    url_site = input('Digite a URL do site: ')
    try:
        loader = WebBaseLoader(url_site)
        lista_documentos = loader.load()
        documento = ''
        for doc in lista_documentos:
            documento += doc.page_content
        return documento

    except Exception as e:
        print(f'\nErro ao carregar o site. Verifique se a URL está correta ou se o conteúdo pode ser acessado.')
        return None

def carrega_pdf():
    caminho = input('Digite o caminho do arquivo PDF: ')
    try:
        loader = PyPDFLoader(caminho)
        lista_documentos = loader.load()
        documento = ''
        for doc in lista_documentos:
            documento += doc.page_content
        return documento

    except Exception as e:
        print(f'\nErro ao carregar o PDF. Verifique o caminho do arquivo.')
        return None

def carrega_youtube():
    print('\nAtenção: o vídeo precisa ter legendas ativas para funcionar corretamente!')
    print('Se o vídeo não tiver legenda, o BotyTalk não conseguirá ler o conteúdo.\n')
    url_youtube = input('Digite a URL do vídeo do YouTube: ')
    try:
        loader = YoutubeLoader.from_youtube_url(url_youtube, language=['pt'])
        lista_documentos = loader.load()
        documento = ''
        for doc in lista_documentos:
            documento += doc.page_content
        return documento

    except Exception as e:
        print(f'\nErro ao carregar o vídeo. Verifique se ele possui legenda ativa ou se a URL está correta.')
        return None

def principal():
    os.system("cls" if os.name == "nt" else "clear")
    print('Bem-vindo(a) ao BotyTalk! (Digite "x" a qualquer momento para sair)\n')
    
    nome = input('Diga seu nome: ')
    print(f"\nOlá, {nome}! Espero que goste da experiência do BotyTalk. Chame nosso Boty quando precisar de ajuda!")

    texto_selecao = '''
Como você quer conversar com o Boty?
1 - Usar um site como base
2 - Usar um PDF como base
3 - Usar um vídeo do YouTube como base
> '''

    while True:
        selecao = input(texto_selecao).strip()
        if selecao == '1':
            documento = carrega_site()
            if not documento:
                print("\nO conteúdo do site não pôde ser carregado. Tente novamente.\n")
                continue
            break
        elif selecao == '2':
            documento = carrega_pdf()
            if not documento:
                print("\nO conteúdo do PDF não pôde ser carregado. Tente novamente.\n")
                continue
            break
        elif selecao == '3':
            documento = carrega_youtube()
            if not documento:
                print("\nO conteúdo do vídeo não pôde ser carregado. Tente novamente.\n")
                continue
            break
        else:
            print('Digite um valor entre 1 e 3!')

    mensagens = []
    print("\nPronto! Agora você pode conversar com o Boty sobre o conteúdo que foi carregado.")

    historico_limitado = mensagens[-4:] 
    resposta = resposta_bot(historico_limitado, documento)

    while True:
        pergunta = input('Você: ')
        if pergunta.lower() == 'x':
            print('\nMuito obrigado por utilizar o BotyTalk! Aqui está o histórico completo da conversa:')
            for papel, mensagem in mensagens:
                print(f'{papel.capitalize()}: {mensagem}')
            break

        mensagens.append(('user', pergunta))
        resposta = resposta_bot(mensagens, documento)
        mensagens.append(('assistant', resposta))
        print(f'Boty: {resposta}\n')

if __name__ == '__main__':
    principal()