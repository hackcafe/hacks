def webcam_shot(filename, interval, photo_limit):
    from zipfile import ZipFile
    import cv2
    import time
    import os
    cap = cv2.VideoCapture(0)
    files = []
    counter = 1
    
    while counter < photo_limit + 1:
        ret, frame = cap.read()
        name = filename + str(counter) + '.jpg'
        cv2.imwrite(name, frame)
        files.append(name)
        time.sleep(interval)
        counter += 1
        
    with ZipFile(filename + '.zip','w') as zip1: 
        # writing each file one by one 
        for file in files: 
            zip1.write(file)
            os.remove(file)