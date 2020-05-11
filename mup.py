from PIL import Image
import pytesseract
import librosa
import numpy as np
import sounddevice as sd
nut=['B','A#','A','G#','G','F#','F','E','D#','D','C#','C']
nut=nut[::-1]
nut2=[]
for x in range(0,11):
          for a in range(0,len(nut)):
                    nut2.append(nut[a]+str(x))
                    
#print(note)
                    
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = Image.open("lead.png") 
bpm_img = img.crop((2,104,233,202))
sample_img= img.crop((1,1,1767,102))
notes_1= img.crop((5,205,231,256))
notes_2= img.crop((5,262,231,314))
notes_3= img.crop((5,320,231,371))
notes_4= img.crop((5,381,231,432))
notes_5= img.crop((5,438,231,490))
notes_6= img.crop((5,496,231,547))
notes_7= img.crop((5,555,231,606))
notes_8= img.crop((5,612,231,664))
notes_9= img.crop((5,670,231,721))
notes_10= img.crop((5,726,231,761))


bpm = pytesseract.image_to_string(bpm_img, lang='eng')
beat_1= (60/int(bpm))
sample = pytesseract.image_to_string(sample_img, lang='eng')


xpos=[258,315,370,417,456,504,551,606,654,693,741,783,835,875,924,974,1023,
      1073,1120,1165,1216,1265,1317,1361,1407,1455,1502,1546,1601,1643,1694,1744]
ypos=[228,288,350,405,465,521,580,637,696,744]
note=[]
notes1 = pytesseract.image_to_string(notes_1, lang='eng')
note.append(notes1)
notes2 = pytesseract.image_to_string(notes_2, lang='eng')
note.append(notes2)
notes3 = pytesseract.image_to_string(notes_3, lang='eng')
note.append(notes3)
notes4 = pytesseract.image_to_string(notes_4, lang='eng')
note.append(notes4)
notes5 = pytesseract.image_to_string(notes_5, lang='eng')
note.append(notes5)
notes6 = pytesseract.image_to_string(notes_6, lang='eng')
note.append(notes6)
notes7 = pytesseract.image_to_string(notes_7, lang='eng')
note.append(notes7)
notes8 = pytesseract.image_to_string(notes_8, lang='eng')
note.append(notes8)
notes9 = pytesseract.image_to_string(notes_9, lang='eng')
note.append(notes9)
notes10 = pytesseract.image_to_string(notes_10, lang='eng')
note.append(notes10)
for x in range(0,len(note)):
          if note[x]=='':
                    note[x]='blank'
          else:
                    note[x]=note[x].upper()
          note[x]=note[x].replace(' ','')
          note[x]=note[x].replace('S','5')
          note[x]=note[x].replace('H','#')
          #print(note[x])
#I'm a scatman
#print (note)
prefinal=[]
temp=0
for x in range(0, len(xpos)):
          temp=0
          for y in range(0,len(ypos)):
                    r,g,b,a=img.getpixel((xpos[x],ypos[y]))
                    if b!=255 & r!=255 & g!=255:
                              #print("lol")
                              temp=1
                              prefinal.append([note[y],r,g,b])
                              break
          if(temp==0):
                    prefinal.append(["sleep",0,0,0])
          
final=[]
for x in range(0, len(prefinal)):
          if x!=0:
                    if(prefinal[x-1]==prefinal[x]):
                              final[len(final)-1][1]=final[len(final)-1][1]+(1)
                    else:
                              final.append([prefinal[x][0],1])
          else:
                    final.append([prefinal[x][0],1])
                    
                    
#print(final)

dur=float((60/int(bpm))*16)
print(dur)
y, sr = librosa.load(sample,duration =dur, sr=44100)
sil,sr = librosa.load("silence.wav", duration=dur, sr=44100)
#print(y.size)
S = librosa.stft(y)
rs= librosa.get_duration(S=S,sr=44100)
#print(rs)
if(rs<dur):
          rem,sr=librosa.load("silence.wav", duration=(dur-rs), sr=44100)
          y= np.concatenate((y,rem))

S= librosa.stft(y)
print(librosa.get_duration(S=S,sr=44100))
music = np.array([])
for x in range(0,len(final)):
          if(final[x][0]=="sleep"):
                    temp = sil[:round((sil.size/32)*final[x][1])]
          elif(final[x][0]=="blank"):
                    temp = y[:round((y.size/32)*final[x][1])]
          else:
                    pc = nut2.index(final[x][0])-nut2.index('C5')
                    temp1 = y[:round((y.size/32)*final[x][1])]
                    temp = librosa.effects.pitch_shift(temp1, sr=44100, n_steps=pc)
          #print(temp)
          music = np.concatenate((music,temp))

#music = music[:y.size]
#print(music)
#print(music.size)
S= librosa.stft(music)
tmo= (librosa.get_duration(S=S,sr=44100))
save_name="ld.wav"
librosa.output.write_wav(save_name, music, sr)
off= tmo-dur
if off>0 :
     timecheck,sr = librosa.load(save_name, offset=off, sr=44100)
else:
     timecheck,sr = librosa.load(save_name,duration=dur,sr=44100)
librosa.output.write_wav(save_name, timecheck, sr)
                    
          


          
          
