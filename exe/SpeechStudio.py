import azure.cognitiveservices.speech as speechsdk
import os
import csv
import time
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

async def TextToSpeech(name):
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name='en-US-EricNeural'
    speech_config.speech_synthesis_language = "en-US" 
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    for i in range(0,len(name)):
        speech_synthesis_result = speech_synthesizer.speak_text_async(name[i][0]).get()
        stream = speechsdk.AudioDataStream(speech_synthesis_result)
        stream.save_to_wav_file("D:\\Test-TTS\\wrong\\"+name[i][1])
        if speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")


# def CorrectPronunciation(audio):
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
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(name_dict)
def CorrectPronunciation(audio):    
    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
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
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        speech_recognizer.recognized.connect(handle_final_result)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)
        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)
        result = ["".join(filter(None, all_results))]
        filename = audio[i].split('/')[-1]
        name_dict.append([result[0],filename])
    WriteTextToFile(name_dict)
    return name_dict