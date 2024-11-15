# 🇫🇷 Télécharger facilement des vidéos de signes (Langue des Signes Française) depuis [Elix](https://dico.elix-lsf.fr)

## Utilisation
Ouvrir un terminal dans le dossier du script `main.py` :
```txt
python main.py papa yoda tata
Traitement de "papa"...
        Téléchargement : elix_videos\papa_n.mp4 -> Réduction...
        Téléchargement : elix_videos\papa_n.m.mp4 -> Réduction...
Traitement de "yoda"...
        /!\ Aucun résultat pour "yoda".
Traitement de "tata"...
        Téléchargement : elix_videos\tata_n.f.mp4 -> Réduction...

```
Résultat :
```txt
ls elix_videos
papa_n.m.mp4 papa_n.mp4 tata_n.f.mp4
```

## Option
Pour réduire le poids des vidéos téléchargées :
1. [Installer FFMPEG](https://www.gyan.dev/ffmpeg/builds/)
2. Modifier `main.py` :
```py
# Compresser et redimensionner les fichiers vidéo
SMALLER_VIDEOS = True
# Indiquer le chemin du dossier `bin` qui contient `ffmpeg.exe`
path_to_ffmpeg = "C:/Programmes_portables/ffmpeg-6.1-essentials_build/bin"
```


# 🤟 Easily download French Sign Language videos of French words from [Le Dico Elix](https://dico.elix-lsf.fr)
