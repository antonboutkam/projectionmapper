import cv2
import numpy as np
import time

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2048)


def projectionSurfaceWindow():
    whiteWinName = 'whiteWindow'
    whiteImage = np.zeros([768, 1024, 1], dtype=np.uint8)
    whiteImage.fill(255)
    cv2.startWindowThread()
    cv2.namedWindow(whiteWinName, flags=cv2.WINDOW_GUI_NORMAL)
    cv2.moveWindow(whiteWinName, 3841, 0)

    cv2.imshow(whiteWinName, whiteImage)
    cv2.setWindowProperty(whiteWinName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def noProjectionSurfaceWindow():
    whiteWinName = 'whiteWindow'
    blackImage = np.zeros([768, 1024, 1], dtype=np.uint8)
    blackImage.fill(1)
    cv2.imshow(whiteWinName, blackImage)


# print('black projector')
# noProjectionSurfaceWindow()
startTime = time.time()

while (True):

    runningTime = int(time.time() - startTime)
    ret, frame = vid.read()
    print("runnign time " + str(runningTime))
    if runningTime < 5:
        print('turn on projector')
        projectionSurfaceWindow()
        print('take frame lit picture')
        frameLit = cv2.resize(frame, (800, 800), interpolation=cv2.INTER_AREA)
    elif runningTime < 8:
        noProjectionSurfaceWindow()
        print('take frame normal picture')
        frameNormal = cv2.resize(frame, (800, 800), interpolation=cv2.INTER_AREA)
    else:
        grayNormal = cv2.cvtColor(frameNormal, cv2.COLOR_BGR2GRAY)
        grayLit = cv2.cvtColor(frameLit, cv2.COLOR_BGR2GRAY)
        cv2.imshow('normal', frameNormal)
        cv2.imshow('lit', frameLit)
        # cv2.imshow('grayNormal', grayNormal)
        # cv2.imshow('grayLit', grayLit)
        diff = cv2.absdiff(grayNormal, grayLit)
        cv2.imshow("Diff", diff)
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        cv2.imshow("Threshold", thresh)
        kernel = np.ones((5, 5), np.uint8)
        dilate = cv2.dilate(thresh, kernel, iterations=2)
        cv2.imshow("Dilate", dilate)
        contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyWindow('frame')
