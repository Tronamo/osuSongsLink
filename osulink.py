import os
from tkinter import filedialog
import time
import threading

localAppDataPath = os.getenv('LOCALAPPDATA')
songsPath = f'{localAppDataPath}\\osu!\\Songs'

# TODO 
# upload to github
# concurrency
# UI/UX

# Returns a list of osu files in a given directory
def findOsu(path: str):
    sus = []
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1] == '.osu':
            sus.append(filename)
    if not sus:
        raise Exception('No .osu files')
    
    return sus

# Returns a list of tuples with song filepaths and their associated beatmapids and setids
# for maps where multiple setids associate to the same song, the osu file to generate the filepath will be used for the setid
def loadSongs(path: str):
    path = f'{songsPath}\\{path}'
    osuFiles = findOsu(path)

    songs = []
    for file in osuFiles:
        with open(f'{path}\\{file}', 'r', encoding='utf-8') as osu:
            song = None

            for line in osu:
                data = line.split(':', 1)
                if data[0] == 'AudioFilename':
                    song = data[1].strip()
                    songs.append(song)
                    break;

    if not songs:
        raise Exception('No songs')
    
    return songs

# Generate links for given songs in folder
def generateLinks(folder: str, songs: list):
    fin = []
    i = 0
    name = folder

    name = name.split(maxsplit=1)
    if name[0].isnumeric():
        name = f'{name[1]} - {name[0]}'
    else:
        name = ''.join(name)

    for song in songs:
        if song in fin:
            continue
        if i > 0:
            nameFinal = f'{name} - {i}'
        else:
            nameFinal = name

        newLink = f'{nameFinal}{os.path.splitext(song)[1]}'
        ogLink =  f'{songsPath}\\{folder}\\{song}'

        if not os.path.exists(ogLink):
            continue

        os.link(ogLink, newLink)
        # print(f'{nameFinal} generated')

        fin.append(song)
        i += 1

# Finds songs and generates links for each folder in given dir
def loadFolders(path: str):
    for folder in os.listdir(songsPath):
        try:
            songs = loadSongs(folder)
        except Exception as e:
            print(f'No songs found for {folder}: {e}')
        else:
            generateLinks(folder, songs)
            

# Songs and output setup
# Entry point
if __name__ == '__main__':
    if not os.path.exists(songsPath):
        print('osu Songs path not found')
        exit()

    outPath = filedialog.askdirectory(mustexist=False, title='Select output directory')
    if not outPath:
        print('No output path specified')
        exit()
    os.chdir(outPath)

    print(f'osu Songs path is {songsPath}')
    print(f'output path is {outPath}')

    start = time.time()
    pstart = time.process_time()

    try:
        loadFolders(songsPath)
    except KeyboardInterrupt:
        pass

    end = time.time()
    pend = time.process_time()
    print(
        f'Hard links generated in \n{end - start}s (realtime)',
        f'\n{pend - pstart}s (process time)'
        )