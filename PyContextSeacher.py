from tkinter import messagebox
from dotenv import load_dotenv
from pytube import YouTube
from openai import OpenAI
import tkinter as tk
import os

load_dotenv()

api_sk = os.getenv('SECRET_KEY')
client = OpenAI(api_key=api_sk)

global filename
file_name = 'contextlastaudio.mp4'

def downloadYouTube(url, path):
    yt = YouTube(url)
    if not os.path.exists(path):
        print(f'Criando pasta em {path}')
        os.makedirs(path)
    print('Convertendo vídeo para formato de áudio')
    print('Baixando áudio do vídeo')
    yt = yt.streams.filter(only_audio=True).first().download(filename=file_name, output_path=path)
    print('Download concluído com sucesso')

def transcriptionAudio(path, palavra_chave):
    audio_file_path = f'{path}/{file_name}'
    transcript_file_path = f'{path}/transcript.txt'

    try:
        with open(audio_file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            transcript_text = transcript.text
            with open(transcript_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(transcript_text)

            print(f'Transcrição concluída para o arquivo {audio_file_path}')

            if palavra_chave in transcript_text:
                messagebox.showinfo("Confirmação", "Esse assunto é falado nesse vídeo informado")

    except OSError as e:
        print(f'Erro ao abrir o arquivo: {e}')
    except Exception as ex:
        print(f'Erro durante a transcrição: {ex}')

path = './contextseacher_audios'

def iniciarTranscricao():
    link = entry_link.get()
    palavra_chave = entry_palavra.get()
    downloadYouTube(link, path)
    print('Tudo certo, iniciando transcrição...')
    transcriptionAudio(path, palavra_chave)
    print('Transcrição finalizada...')
    print('Deletando arquivo de áudio...')
    os.remove(f'{path}/{file_name}')

root = tk.Tk()
root.title("Transcrição de Áudio")

label_link = tk.Label(root, text="Link:")
label_link.pack()

global entry_link
entry_link = tk.Entry(root, width=50)
entry_link.pack()

label_palavra = tk.Label(root, text="Palavra-chave:")
label_palavra.pack()

global entry_palavra
entry_palavra = tk.Entry(root, width=50)
entry_palavra.pack()

btn_iniciar = tk.Button(root, text="Iniciar Transcrição", command=iniciarTranscricao)
btn_iniciar.pack()

root.mainloop()

