import azure.cognitiveservices.speech as speechsdk
import os
import csv
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np 
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

# async def TextToSpeech(name):
#     audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
#     speech_config.speech_synthesis_voice_name='en-US-TonyNeural'
#     speech_config.speech_synthesis_language = "en-US" 
#     speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

#     for i in range(0,len(name)):
#         speech_synthesis_result = speech_synthesizer.speak_text_async(name[i][0]).get()
#         stream = speechsdk.AudioDataStream(speech_synthesis_result)
#         stream.save_to_wav_file("D:\\Test-TTS\\Audio\\"+"candidate_"+name[i][1]+"_en.wav")
#         if speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
#             cancellation_details = speech_synthesis_result.cancellation_details
#             print("Speech synthesis canceled: {}".format(cancellation_details.reason))
#             if cancellation_details.reason == speechsdk.CancellationReason.Error:
#                 if cancellation_details.error_details:
#                     print("Error details: {}".format(cancellation_details.error_details))
#                     print("Did you set the speech resource key and region values?")

def createSSML(text):
    # <say-as interpret-as="name">{}</say-as>
    # <lexicon uri="https://lexicon2024.blob.core.windows.net/lexicon/lexicon.xml"/>
    # xml:lang="es-ES"
    ssml = '''<?xml version="1.0" encoding="UTF-8"?>
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="en-US-AndrewMultilingualNeural">
            <prosody rate="+0%">
                <lexicon uri="https://lexicon2024.blob.core.windows.net/lexicon/lexicon.xml"/>
                {}
            </prosody>
        </voice>
    </speak>'''.format(text)
    return ssml

def TextToSpeech(name):
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff8Khz8BitMonoMULaw) 
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    name_dict = []
    for i in range(0,len(name)):
        ssml_string = createSSML(name[i][0])
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()
        stream = speechsdk.AudioDataStream(result)
        stream.save_to_wav_file("G:\Shared drives\IVS Docs\Test Aculab\8Khz8BitMonoMULaw\Voice-Andrew\instructions\\"+name[i][1]+".wav")
        name_dict.append(name[i][0],name[i][1])
        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
    WriteTextToFile(name_dict)
                


# def SpeechToText(audio):
#     speech_config.speech_recognition_language="en-US"
#     name_dict = []
#     for i in range(0,len(audio)):
#         audio_config = speechsdk.audio.AudioConfig(filename=audio[i])
#         speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
#         speech_recognition_result = speech_recognizer.recognize_once_async().get()
#         filename = audio[i].split('\\')[-1]
#         parts = filename.split('_')
#         code = f"{parts[1]}_{parts[2]}"
#         name_dict.append([speech_recognition_result.text,code])
#     return name_dict


def WriteTextToFile(name_dict):
    # field names
    fields = ['Text', 'File Name']

    # name of csv file
    filename = "D:\Test-TTS\Text.csv"

    # writing to csv file
    with open(filename, 'w',encoding="utf8",newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(name_dict)
def SpeechToText(audio):    
    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        # print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
    def handle_final_result(evt):
        all_results.append(evt.result.text)

    name_dict = []
    for i in range(0,len(audio)):
        done = False
        all_results = []
        audio_config = speechsdk.audio.AudioConfig(filename=audio[i])
        try:
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            speech_recognizer.recognized.connect(handle_final_result)
            speech_recognizer.session_stopped.connect(stop_cb)
            speech_recognizer.canceled.connect(stop_cb)
            # Start continuous speech recognition
            speech_recognizer.start_continuous_recognition()
            # if result.reason == speechsdk.ResultReason.Canceled:
            #     cancellation_details = result.cancellation_details
            #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
            #         if cancellation_details.error_details:
            #             print("Error details: {}".format(cancellation_details.error_details))
            #             print("Did you set the speech resource key and region values?")
            while not done:
                time.sleep(.5)
        except:
            print("Cannot open the audio file",audio[i])
        result = ["".join(filter(None, all_results))]
        print(result)
        filename = audio[i].split('/')[-1]
        name_dict.append([result[0],filename])
    # WriteTextToFile(name_dict)
    return name_dict

def Start_Correcting(audio_arr):
    with ProcessPoolExecutor() as executor:
        # Run audio_to_text for each chunk
        future_to_audio = {executor.submit(SpeechToText, chunk): chunk for chunk in audio_arr}
        
        # Process each completed task as soon as it finishes
        for future in as_completed(future_to_audio):
            text_chunk = future.result()
            # Run text-to-speech in the background
            executor.submit(TextToSpeech, text_chunk)
def GetNames(filepath):
    with open(filepath,encoding="utf8") as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        candidates = list(csvReader)
        candidates.pop(0)
        # candidates_array = np.array(candidates)
        return candidates
    
def Start_TTS(audio_arr):
    # num_processes = mp.cpu_count() 
    # chunk_size = int(audio_arr.shape[0] / num_processes) 
    # chunks = [audio_arr[i:i + chunk_size] for i in range(0, audio_arr.shape[0], chunk_size)] 
  
    # pool = mp.Pool(processes=num_processes) 
    # results = pool.map(TextToSpeech, audio_arr) 
    return(TextToSpeech(audio_arr))

def Correct_audio(audio_arr):
    # num_processes = 8
    # length = len(audio_arr)
    # chunk_size = int(len(audio_arr)/num_processes)
    # chunks = [audio_arr[i:i + chunk_size] for i in range(0, length, chunk_size)] 
  
    # pool = mp.Pool(processes=num_processes) 
    # results = pool.map(Start_Correcting, chunks) 

    text_chunks=[]

    with ProcessPoolExecutor(max_workers=8) as executor:
        # Run audio_to_text for each chunk
        future_to_audio = {executor.submit(SpeechToText, [chunk]): chunk for chunk in audio_arr}
        
        # Process each completed task as soon as it finishes
        for future in as_completed(future_to_audio):
            text_chunk = future.result()
            # text_chunks.append(text_chunk[0])
            # Run text-to-speech in the background
            executor.submit(TextToSpeech, text_chunk)
