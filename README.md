# projectionmapper
An attempt to project video on moving objects using a webcam, opencv and ofcourse a beamer.


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

