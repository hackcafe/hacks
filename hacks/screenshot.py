def screenshot(filename, interval, num_pics):
    from zipfile import ZipFile 
    import time
    import pyautogui
    import os
    counter = 0
    filenames = []
    
    while counter < num_pics:
        name = filename + str(counter + 1) + ".jpg"
        filenames.append(name)
        pyautogui.screenshot(name)
        time.sleep(interval)
        counter += 1
        
    # zip and send in email
    with ZipFile(filename + '.zip','w') as zip1: 
        # writing each file one by one 
        for file in filenames: 
            zip1.write(file)
            os.remove(file)