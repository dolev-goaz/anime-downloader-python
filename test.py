from downloadEpisode import Downloader
import os
import sys 

def download(url, filename, path, downloadFinished = None):
    if downloadFinished:
        downloader = Downloader(url, filename, path, finish_hook=downloadFinished)
    else:
        downloader = Downloader(url, filename, path)
        
    downloader.start()

anime_name = sys.argv[1]
formatted_name = anime_name.replace(' ', '-')
formatted_name = ''.join(ch for ch in formatted_name if ch.isalnum() or ch == '-')

episodes = int(sys.argv[2])

for ep in range(1, episodes + 1):
    #episode = '%02d' % ep
    episode = ep
    hostname = "https://v6.4animu.me/"
    url = f'{hostname}/{formatted_name}/{formatted_name}-Episode-{episode}-1080p.mp4'
    print(url)

    filename = f'{formatted_name} EP {episode}.mp4'
    dirpath = os.getcwd() + f'/{anime_name}/'

    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    
    path = dirpath + filename
    
    if os.path.exists(path):
      os.remove(path)
    
    download(url, filename, path)
