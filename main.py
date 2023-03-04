from tkinter import *
import cv2

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



root = Tk()

root.title('helper')
root.geometry('400x600')
root.resizable(width=False, height=False)
root.iconbitmap("icon\icon.ico")

canvas = Canvas(root, height=300,width=250)
canvas.pack()

frame = Frame(root)
frame.place(relx=0,rely=0.3,relheight=0.7, relwidth=1)
title = Label(frame, text="Нажмите на кнопку ", font=("Arial",20))
title.pack()
btn = Button(frame, text='Кнопка',bg='gray',width=15, height=3,font=("Arial",20))
btn.pack(pady=50)

root.mainloop()


