def extract_hackfns():
    import os
    modulefiles = [modfile.split('.')[0] for modfile in os.listdir('hacks') if modfile.endswith('.py')]
    print(modulefiles)

    import hacks
    hack_funcs = {}

    for modulefile in modulefiles:
        __import__('hacks.' + modulefile)
        module = getattr(hacks, modulefile)
        func = getattr(module, module.__dir__()[-1])
        hack_funcs[modulefile] = func

    return hack_funcs