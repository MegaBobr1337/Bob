import speech_recognition as sr
import gtts
import webbrowser
import urllib
import os
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import pygame
import cv2



pygame.init()

speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[1].id)

path = os.path.dirname(os.path.abspath(__file__))

# commands
opts = {
    'name': ('lillian', 'lilly', 'li', 'lili', 'lily'),
    'user_command': ('tell', 'say', 'show', 'how many', 'how', 'search'),
    'cmds': {
        'ctime': ('time', 'what time', 'the time'),
        'paint': ('paint', 'draw', 'art'),
        'google': ('find', 'google search', 'google'),
        'youtube': ('video', 'youtube', 'music'),
        'camera':("camera")
    }
}


# Write voice
def command():
    r = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='en-EN').lower()
        # text = r.recognize_google(audio, language='fr-FR').lower()
        print('[log] Recognized: ' + text)

    except sr.UnknownValueError:
        print('[log] Voice not recognized!')
    except sr.RequestError as e:
        print('[log] Unknown error, check the internet!')
    except:
        text = command()
    return text


# Convert text to speech
# method 1
def text_to_speech(text):
    tts = gtts.gTTS(text)
    speech_path = os.path.join((path + '/speech.mp4'))
    tts.save(speech_path)
    pygame.mixer.music.load('speech.mp4')
    pygame.mixer.music.play()


# Convert text to speech
# method 2
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(text):
    if text.startswith(opts['name']):
        cmd = text

        for x in opts['name']:
            cmd = cmd.replace(x, "").strip()

        for x in opts['user_command']:
            cmd = cmd.replace(x, "").strip()

        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Time  ' + str(now.hour) + ':' + str(now.minute))

    elif cmd == 'paint':
        os.system("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Paint")

    elif cmd == 'google':
        cmd = cmd.replace('google', "").strip()
        speak('The Google content has been opened for you')
        google_search(cmd)

    elif cmd == 'youtube':
        cmd = cmd.replace('youtube', "").strip()
        speak('The Youtube has been opened for you')
        youtube_search(cmd)

    elif cmd == 'camera':
        camera()


    else:
        print('Not recognized! Repeat, please!')


def google_search(text):
    tes = urllib.parse.quote_plus(text)
    url = 'https://www.google.com/search?q='
    webbrowser.open(url + tes, new=2)


def youtube_search(text):
    tes = urllib.parse.quote_plus(text)
    url = 'https://www.youtube.com/results?search_query='
    webbrowser.open(url + tes, new=2)






def camera():
    def haar_detection(image):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # start detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 242, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (229, 244, 65), 2)
        # end detection

        return img


    if __name__ == '__main__':
        cap = cv2.VideoCapture(0)

        while (cap.isOpened()):
            ret, img = cap.read()
            img = haar_detection(img)
            cv2.imshow('Video', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    execute_cmd(command())


