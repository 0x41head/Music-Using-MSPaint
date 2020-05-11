from PIL import Image
import pytesseract
import librosa
import numpy as np
import sounddevice as sd

                    
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

### image file to scan
img = Image.open("samplepl.png") 
####


bpm_img = img.crop((2,104,233,202))

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



xpos=[315,504,693,875,1073,1265,1455,1643]
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
                    
          
          print(note[x])
#I'm a scatman
#print (note)

dur=float((60/int(bpm))*16)
sil,sr = librosa.load("silence.wav", duration=dur, sr=44100)
mix,sr = librosa.load("silence.wav", duration=dur*8, sr=44100)
for y in range(0, len(ypos)):
          music=np.array([])
          if (note[y]=="blank"):
               continue
          else:
               sp, sr = librosa.load(note[y],duration =dur, sr=44100)
               for x in range(0,len(xpos)):
                    r,g,b,a=img.getpixel((xpos[x],ypos[y]))
                    temp=np.array([])
                    if b!=255 & r!=255 & g!=255:
                         temp= sp

                    else:
                         temp=sil
                    
                    music = np.concatenate((music,temp))
                    #print(music.size)

          mix=mix+music

                    
##fianl mix                    
librosa.output.write_wav("mix.wav", mix, sr=44100)

                    
          


          
          
