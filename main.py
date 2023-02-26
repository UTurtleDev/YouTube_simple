from pytube import YouTube
from pathlib import Path
import tkinter
from tkinter import filedialog
import ssl

# squize les problèmes de certificats 
ssl._create_default_https_context = ssl._create_unverified_context

video_to_convert = ""
choosen_folder = ""
video_name = ""
file_name = ""


def choose_folder():
    """
    Open dialog ask directory
    """
    # Efface la zone
    entry_dest_folder.delete(0, tkinter.END)
    # Remise à zéro du statut
    label_song_status.configure(text=(""))
    # Ouvre la boite de dialog choisir un répertoire
    choosen_folder = tkinter.filedialog.askdirectory()
    # Insère le répertoire choisi dans la zone du repertoire
    entry_dest_folder.insert(0, choosen_folder)


def test_choosen_folder():
    """Test if choosen folder is not empty

    Returns:
        str: path of the directory for download
    """
    # Récupération du répertoire selectionné
    choosen_folder = entry_dest_folder.get()
    # Vérification qu'un répertoire à bien été selectionné
    if choosen_folder == "":
        label_song_status.configure(text="Sélectionnez un répertoire", fg="red")
        return ""

    else:
        return choosen_folder


def test_url(choosen_folder):
    """
    Test if the url could be use to create an pytube objet

    Args:
        choosen_folder (str): folder to download file

    Returns:
        video_to_convert: youtube objet of the video to download
        video_name: title of the video to download
    """
    if choose_folder:
        # Récupération de l'url de la vidéo entrée
        entry_url = entry_url_video.get()

        try:
            # Création de l'objet Youtube
            video_to_convert = YouTube(entry_url)
            # Stockage du nom de la vidéo en supprimant les éventuels /
            video_name = video_to_convert.title.replace("/", "")
            return video_to_convert, video_name

        except:
            # Statut : URL incorrect si l'url n'est pas bonne
            label_song_status.configure(text="URL incorrecte", fg="red")


def test_if_song_exist(choosen_folder, video_to_convert, video_name):
    """_
    Test if the song already exists

    Args:
        choosen_folder (str): folder to download file
        video_to_convert (youtube): youtube objet of the video to download
        video_name (str): title of the video to download

    Returns:
        file_name: name with extension of the video
    """
    if video_to_convert and video_name:
        # Rajout de l'extention au nom de la video
        file_name = f"{video_name}.mp3"
        # Chemin complet de fichier à télécharger
        complete_path = Path(f"{choosen_folder}/{file_name}")
        # Vérification de l'existance du fichier
        if not complete_path.is_file():
            return file_name

        else:
            label_song_status.configure(
                text=f"Le fichier {video_name} existe déjà", fg="red")


def download_song(video_to_convert, choosen_folder, file_name):
    """
    Select the audio file and download it

    Args:
        video_to_convert (youtube): youtube objet of the video to download
        choosen_folder (str): folder to download file
        file_name (str): name with extension of the video
    """
    if video_to_convert and choosen_folder and file_name:
        label_song_status.configure(text=f"Téléchargement de {file_name} en cours ...", fg="blue")
        # Selection du fichier audio
        audio_file = video_to_convert.streams.filter(only_audio=True).first()
        # Téléchargement
        audio_file.download(choosen_folder, filename=file_name, skip_existing=False)
        # Statut : Téléchargement terminé
        label_song_status.configure(text=f"Téléchargement de {file_name} terminé !", fg="blue")
        # efface l'url de la vidéo téléchargée
        entry_url_video.delete(0, tkinter.END)


def start():
    """
    Run the process of download file
    """
    label_song_status.configure(text=(""))
    choosen_folder = test_choosen_folder()
    video_to_convert, video_name = test_url(choosen_folder)
    file_name = test_if_song_exist(choosen_folder, video_to_convert, video_name)
    download_song(video_to_convert, choosen_folder, file_name)


app = tkinter.Tk()

# Fenetre
app.title("Convertisseur YouTube => MP3")
app.geometry("680x260")
app.resizable(height=None, width=None)

# Repertoire de destination
label_dest_folder = tkinter.Label(app, text="Répertoire de destination : ")
label_dest_folder.grid(column=0, row=0, padx=10, pady=10, sticky="W")

entry_dest_folder = tkinter.Entry(app, width=55)
entry_dest_folder.grid(column=0, row=1, padx=10)

button_chose_folder = tkinter.Button(app, text="...", command=choose_folder)
button_chose_folder.grid(column=1, row=1, sticky="W")

# URL de la video
label_url_video = tkinter.Label(app, text="URL de la vidéo")
label_url_video.grid(column=0, row=4, padx=10, sticky="W")

entry_url_video = tkinter.Entry(app, width=55)
entry_url_video.grid(column=0, row=5, padx=10, pady=10, sticky="W")

button_download = tkinter.Button(app, text="Télécharger", command=start)
button_download.grid(column=1, row=5, sticky="W")

# Label Etat
label_song_status = tkinter.Label(app, text=video_to_convert)
label_song_status.grid(column=0, row=7, pady=15)

# Footer
label_footer = tkinter.Label(app, text="© 2023 UTurtleDev")
label_footer.grid(column=0, row=8, pady=15, columnspan=2, sticky="E")


app.mainloop()
