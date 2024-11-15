#!/usr/bin/env python3

import pathlib
import platform
import requests
import shutil
import subprocess
import sys


OUTPUT_FOLDER = 'elix_videos'
pathlib.Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# Compress and resize video files
SMALLER_VIDEOS = False
# Specify the path to the folder that contains `ffmpeg.exe`
path_to_ffmpeg = "C:/Programmes_portables/ffmpeg-6.1-essentials_build/bin"
video_target_rate = '100k' # target rate (bit/s)
video_height = 480 # pixels (set to -1 to disable)


def run_command(command: str):
    # Run a command using subprocess
    process = subprocess.Popen(command, shell=True)
    process.communicate()


def download_file(url: str, filename: str):
    with requests.get(url, stream=True) as resp:
        with open(filename, 'wb') as out:
            shutil.copyfileobj(resp.raw, out)


if SMALLER_VIDEOS:
    # Determine OS to set null device
    if platform.system() == 'Windows':
        ffmpeg_suffix = 'NUL'
    elif platform.system() in ('Linux', 'Darwin'): # macOS is Darwin (Apple)
        ffmpeg_suffix = '/dev/null'
    else:
        raise ValueError("Unexpected OS. Please edit the script.")

    # Add FFMPEG to PATH
    sys.path.insert(0, pathlib.Path(path_to_ffmpeg))

    # Prepare command
    command_header = 'ffmpeg -hide_banner -loglevel error '
    command_encoding = f'-c:v libx264 -preset medium -b:v {video_target_rate} '
    if video_height > 0:
        command_resize = f'-vf "scale=-2:\'min({video_height},ih)\'" '
    else:
        command_resize = ''

    def compress_video(input_filename: str, temporary_filename: str="elixtemp.mp4"):
        # Converts video to MP4 (overwrites the original)

        # First pass (use -y to overwrite)
        command_1 = f'{command_header} -y -i "{input_filename}" {command_encoding} {command_resize} -an -pass 1 -f mp4 NUL'
        # Second pass
        command_2 = f'{command_header} -i "{input_filename}" {command_encoding} {command_resize} -an -pass 2 "{temporary_filename}"'

        # Call FFMPEG
        run_command(command_1)
        run_command(command_2)

        # Delete the original file
        pathlib.Path(input_filename).unlink()

        # Rename processed video to original name
        pathlib.Path(temporary_filename).rename(input_filename)


def create_video_files(words: list):
    for word in words:
        print(f'Traitement de "{word}"...')
        try:
            json_response = requests.get(f'https://api.elix-lsf.fr/words?q={word}').json()

            result_list = [result for result in json_response['data'] if result['typology'] != 'n.prop.' and result['meanings'] and result['meanings'][0]['wordSigns']]

            if not result_list:
                print(f'\t/!\\ Aucun résultat pour "{word}".')
                continue

            for result in result_list:  
                url = 'https://www.elix-lsf.fr/IMG/' + result['meanings'][0]['wordSigns'][0]['uri']
                ext = url.split('.')[-1]
                filename = pathlib.Path(OUTPUT_FOLDER).joinpath(f'{result["name"]}_{result["typology"]}{ext}')

                print(f'\tTéléchargement : {filename}', end="")
                download_file(url, filename)

                if SMALLER_VIDEOS:
                    try:
                        print(' -> Réduction...', end="")
                        compress_video(filename)
                    except:
                        print(f'\t/!\\ Erreur lors du traitement de la vidéo "{filename}".')
                        raise

                print("")

        except Exception as ex:
            print(f'\t/!\\ Erreur lors du traitement de "{word}": {ex}')

    # Clean temporary files
    if SMALLER_VIDEOS:
        pathlib.Path("ffmpeg2pass-0.log").unlink(missing_ok=True)
        pathlib.Path("ffmpeg2pass-0.log.mbtree").unlink(missing_ok=True)






if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Écrivez les mots que vous souhaitez télécharger (séparés par des espaces). Laisser vider pour fermer.")
        while True:
            query = input("> Mots : ")
            if query == "":
                break
            create_video_files(query.split(" "))

    else:
        # Show help when asked
        if sys.argv[1] in ('-h', '--help'):
            print(f'Usage: {sys.argv[0]} <word1 word2...>')
            exit(0)

        # Otherwise, process words
        create_video_files(sys.argv[1:])
