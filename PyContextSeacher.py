from pytube import YouTube
import os

def downloadYouTube(url, path):
    yt = YouTube(url)
    if not os.path.exists(path):
        print(f'Criando pasta em {path}')
        os.makedirs(path)
    print('Convertendo vídeo para formato de áudio')
    print('Baixando áudio do vídeo')
    yt = yt.streams.filter(only_audio=True).first().download(path)
    print('Download concluído com sucesso')
    

link = input('Informe o link do vídeo\n')

try:
  downloadYouTube(link, './contextseacher_audios')
  print('Tudo certo, iniciando transcrição...')
except:
  print("Um erro ocorreu ao baixar o vídeo...")