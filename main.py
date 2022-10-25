import numpy as np
import time
from Init import Init
from Gui import Gui
import cv2

# # Print('black projector')
# noProjectionSurfaceWindow()
startTime = time.time()
init = Init()
gui = Gui()
gui.show()
current_calibration_threshold = gui.calibration_threshold

while (True):
    runningTime = int(time.time() - startTime)
    gui.update()
    # Print("running")
    if current_calibration_threshold != gui.calibration_threshold:
        init.initialized = False
        current_calibration_threshold = gui.calibration_threshold
        startTime = time.time()

    if not init.initialized:
        # Print("init")
        init.run(runningTime, gui)
    else:
        # Print("canvas")
        canvas = init.canvas
        canvas.play()

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Destroy all the windows
cv2.destroyWindow('frame')
