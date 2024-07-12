from tkinter import *
from tkinter import filedialog
from tkinter import Label
import csv
import asyncio
from GetName import GetNames 
from SpeechStudio import *

def button1clicked():
    asyncio.run(GenerateSpeech())
async def GenerateSpeech():
    filename = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]) 
    if filename:
        status_label.config(text="Generating audio...")
        # Force the update of the UI
        window.update_idletasks()
        task = asyncio.create_task(TextToSpeech(GetNames(filename)))
        await task
        status_label.config(text="Done!!!\nGenerated audio files are stored at <the default path>")
def button2clicked():
    asyncio.run(CorrectAudio())
async def CorrectAudio():
    filename = filedialog.askopenfilenames(defaultextension=".wav", filetypes=[("Wav Files", "*.wav")]) 
    if filename:
        status_label.config(text="Correcting pronunciation...")
        # Force the update of the UI
        window.update_idletasks()
        names = CorrectPronunciation(filename)
        task = asyncio.create_task(TextToSpeech(names))
        await task
        status_label.config(text="Done!!!\nCorrected audio files are stored at <the default path>")
window = Tk()
window.title("Speech Studio")
window.geometry('900x300')
window.tk.call('tk','scaling',3.0)
generate_speech_btn = Button(window,text="Start Generating Speech",command=button1clicked)
generate_speech_btn.place(x=100,y=100)
correct_pronunciation_btn = Button(window,text="Correct Pronunciation",command=button2clicked)
correct_pronunciation_btn.place(x=500,y=100)
status_label = Label(window, text="")
status_label.pack()
window.mainloop()