from bs4 import BeautifulSoup
 
 
# Reading the data inside the xml
# file to a variable under the name 
# data
with open("C:\\Users\\Huy\\Downloads\\AUDIO_LIST_EN.XML", mode='r',encoding="utf8") as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag 
# `unique`
b_audio = Bs_data.find_all('Audio')
name_dict = []
for audio in b_audio:
    audioCode = audio.find('AudioCode').text
    text = audio.find('EN').text
    if text.startswith('*'):
        text = text + " endorsed candidate"
        text = text.replace('*',"")
    name_dict.append([text,audioCode])
# Using find() to extract attributes 
# of the first instance of the tag
b_name = Bs_data.find('child', {'name':'Frank'})
 
print(b_name)
 
# Extracting the data stored in a
# specific attribute of the 
# `child` tag
value = b_name.get('test')
 
print(value)