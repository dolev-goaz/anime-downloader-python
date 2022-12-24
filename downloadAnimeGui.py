from downloadAnimeLib import *
from tkinter import *
from multiprocessing import Process

root = Tk()
listbox = Listbox(root)
threads = []
episodes = {}
anime_name_entry = Entry(root, width=50, borderwidth=5)
anime_name_entry.pack()

def download_update_hook(filename, percentage):
        if percentage == 100:
                del episodes[filename]
        else:
                episodes[filename] = percentage
        listbox.delete(0, END)
        if not episodes:
                downloadButton["state"] = "normal"
        for episode in episodes:
                listbox.insert(END, (episode, f'{episodes[episode]}%'))

def download_episodes_tk(directory_name, download_hrefs, hook=None):
        threads.clear()
        if os.path.exists(directory_name):
                shutil.rmtree(directory_name)
        os.mkdir(directory_name)

        for href in download_hrefs:
                t = Thread(target=download, args=(href[0], href[1], f'{directory_name}\{href[1]}', hook))
                #t = Process(target=download, args=(href[0], href[1], f'{directory_name}\{href[1]}', hook))
                episodes[href[1]] = '0%'
                t.start()
                threads.append(t)
        #for thread in threads:
        #        thread.join()


def start_download_tk(anime_name):
        parsed_anime_name = re.sub('[^A-Za-z0-9 ]+', '', anime_name.strip().lower()).replace(' ', '-')
        Label(root, text=anime_name).pack()
        hrefs = get_episode_hrefs(parsed_anime_name)
        download_hrefs = get_all_download_hrefs(hrefs)
        listbox.pack()
        download_episodes_tk(parsed_anime_name, download_hrefs, hook = download_update_hook)

        for episode in episodes:
                listbox.insert(END, (episode, episodes[episode]))



def downloadClick():
        global downloadButton
        text = anime_name_entry.get()
        start_download_tk(anime_name = text)
        downloadButton["state"] = "disabled"

def abortClick():
        for thread in threads:
                thread.terminate()
        
downloadButton = Button(root, text="Download", command=downloadClick)
downloadButton.pack()
pauseButtoon = Button(root, text="Abort", command=abortClick)
pauseButtoon.pack()


root.mainloop()
