
import numpy as np
import time
from Init import Init





# print('black projector')
# noProjectionSurfaceWindow()
startTime = time.time()
init = Init()

while (True):
    runningTime = int(time.time() - startTime)

    if not init.initialized:
        init.run(runningTime)


    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyWindow('frame')
