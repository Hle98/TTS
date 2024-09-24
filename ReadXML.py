from bs4 import BeautifulSoup
import csv
 
def WriteTextToFile(name_dict):
    # field names
    fields = ['Text', 'File Name']

    # name of csv file
    filename = "D:\Test-TTS\\PR.csv"

    # writing to csv file
    with open(filename, 'w',encoding="utf8",newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(name_dict)

with open("D:\Test-TTS\PPD20240917\AUDIO_LIST_SP.XML", mode='r',encoding="utf8") as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag 
# `unique`
b_audio = Bs_data.find_all('Audio')
names = []
for audio in b_audio:
    audioCode = audio.find('AudioCode').text+"_sp"
    text = audio.find('SP').text
    if text.startswith('*'):
        text = text + " endorsed candidate"
        text = text.replace('*',"")
    names.append([text,audioCode])
WriteTextToFile(name_dict=names)