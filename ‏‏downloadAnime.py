from downloadAnimeLib import *

def main():
    url = 'https://animekisa.tv'
    anime_name = ''
    if len(sys.argv) == 1:
        anime_name = input('Insert anime name: ')
    else:
        anime_name = sys.argv[1]
    start_download(anime_name, url)

if __name__ == '__main__':
    main()
