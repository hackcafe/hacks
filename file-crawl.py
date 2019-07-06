def file_crawl():
    import os
    for (dirpath, dirnames, filenames) in os.walk('/'):
        for file in filenames:
            file = dirpath + file
            while True:
                response = input(f"Read(r), Modify(m), Delete(d), Pass(p), or Quit(q)? {file}: ")
                if response == 'r':
                    try:
                        current_file = open(file, 'r')
                        print(current_file.read())
                        current_file.close()
                    except Exception as e:
                        print("[-] File Error: " + str(e))
                elif response == 'm':
                    current_file = open(file, 'w')
                    modify_text = input("Input new text: ")
                    current_file.write(modify_text)
                    current_file.close()
                elif response == 'd':
                    os.remove(file)
                    break
                elif response == 'p':
                    break
                elif response == 'q':
                    return
                else:
                    print("[-] Invalid input, please try again")