import tkinter.filedialog

root = tkinter.Tk()
root.withdraw() # cache la fenêtre principale de tkinter

dir_path = tkinter.filedialog.DirectoryChooser()
print("Répertoire sélectionné :", dir_path)