from tkinter import *
from tkinter import filedialog
from tkinter import Label
import time
import csv
import asyncio
from SpeechStudio import *

def button1clicked():
    GenerateSpeech()
def GenerateSpeech():
    filename = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]) 
    if filename:
        status_label.config(text="Generating audio...")
        # Force the update of the UI
        window.update_idletasks()
        names= GetNames(filename)
        # await names 
        # start_time = time.perf_counter() 
        # TextToSpeech(names)
        # end_time = time.perf_counter() 
        # total_time = end_time - start_time 
        # print(total_time) 
        start_time = time.perf_counter() 
        Start_TTS(names)
        end_time = time.perf_counter() 
        total_time = end_time - start_time 
        print(total_time) 
        status_label.config(text="Done!!!\nGenerated audio files are stored at <the default path>")
def button2clicked():
    CorrectAudio()
def CorrectAudio():
    filename = filedialog.askopenfilenames(defaultextension=".wav", filetypes=[("Wav Files", "*.wav")]) 
    if filename:
        status_label.config(text="Correcting pronunciation...")
        # Force the update of the UI
        window.update_idletasks()
        start_time = time.perf_counter() 
        Correct_audio(filename)
        end_time = time.perf_counter() 
        total_time = end_time - start_time 
        print(total_time) 
        status_label.config(text="Done!!!\nCorrected audio files are stored at <the default path>")
if __name__ == '__main__':
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