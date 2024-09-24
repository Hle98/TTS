from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import Label
import time
import csv
import asyncio
from SpeechStudio import *


class MainWindow:
    def __init__(self,root):
        self.root = root
        self.root.title("Speech Studio")
        self.generate_speech_btn = tk.Button(self.root,text="Start Generating Speech",command=self.GenerateSpeech)
        self.generate_speech_btn.place(x=100,y=100)
        self.correct_pronunciation_btn = tk.Button(self.root,text="Correct Pronunciation",command=self.CorrectAudio)
        self.correct_pronunciation_btn.place(x=500,y=100)
    # def button1clicked():
    #     GenerateSpeech()
    def GenerateSpeech(self):
        filename = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]) 
        if filename:
            self.root.status_label = tk.Label(self.root, text="Generating audio...")
            # Force the update of the UI
            self.root.update_idletasks()
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
            self.root.status_label.config(text="Done!!!\nGenerated audio files are stored at <the default path>")
    # def button2clicked():
    #     CorrectAudio()
    def CorrectAudio(self):
        filename = filedialog.askopenfilenames(defaultextension=".wav", filetypes=[("Wav Files", "*.wav")]) 
        if filename:
           # status_label.config(text="Correcting pronunciation...")
            # Force the update of the UI
            self.root.update_idletasks()
            start_time = time.perf_counter() 
            Correct_audio(filename)
            end_time = time.perf_counter() 
            total_time = end_time - start_time 
            print(total_time) 
            #status_label.config(text="Done!!!\nCorrected audio files are stored at <the default path>")
if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
    