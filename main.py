
import numpy as np
import time
from Init import Init
from Projector import Projector
import cv2




# print('black projector')
# noProjectionSurfaceWindow()
startTime = time.time()
init = Init()

while (True):
    runningTime = int(time.time() - startTime)

    if not init.initialized:
        init.run(runningTime)
    else:
        projector = Projector()
        projector.white()

        frame = init.canvas.capture()
        width, height = frame.shape[:2]
        frame2 = frame.resize(width*3, height * 3)
        cv2.imshow("New frame 1", frame2)

        cv2.imshow("New frame 2", frame)


    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyWindow('frame')
