import numpy as np
import time
from Init import Init
from Gui import Gui
from Projector import Projector
import cv2

# # Print('black projector')
# noProjectionSurfaceWindow()
startTime = time.time()
init = Init()
gui = Gui()
gui.show()
current_calibration_threshold = gui.calibration_threshold
current_calibration_luminosity = gui.calibration_luminosity
projector = Projector()
restart_init = False

while (True):
    runningTime = int(time.time() - startTime)
    gui.update()
    # Print("running")
    if gui.calibration_recalibrate:
        print('Restart initialization')
        init.initialized = False
        current_calibration_threshold = gui.calibration_threshold
        startTime = time.time()

    if not init.initialized:
        init.run(runningTime, gui, projector)
    else:
        canvas = init.canvas
        canvas.play(projector)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Destroy all the windows
cv2.destroyWindow('frame')
