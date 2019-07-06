def duplicate(num_copies=1000):
    import os
    from shutil import copyfile
    
    counter = 0
    
    while counter < num_copies:
        copyfile(os.getcwd() + '/' + __file__, os.getcwd() + '/' + str(counter) + '-' + __file__)
        counter += 1