import os
file_folder=__file__.split("main.py")
words_file_path = file_folder[0]+"words (1).txt"
file_rw = input("What file are you reading/writing? ")
file_rw=file_folder[0]+file_rw
op=input("input operation write, read, edit, and exit. ")
if op.lower()=="write":
    with open(words_file_path) as file:
        words=[word.strip() for word in file.readlines()]
    word_to_index = {word: i + 1 for i, word in enumerate(words)}
    while True:
        line_file = []
        line=input("Enter a line of text: ").strip()
        line_list=line.split(" ")
        for word in line_list:
            if word in word_to_index:
                size=hex(word_to_index[word]).split("0x")[1] 
                line_file.append(size + " ")
            else:
                line_file.append(word + " ")
        if line_file:
                    with open(f"{file_rw}.txt", "a") as file: 
                        if os.stat(f"{file_rw}.txt").st_size > 0:
                            file.write("\n")
                        file.writelines (line_file)
if op.lower()=="read":
    i=0
    with open(f"{file_rw}.txt") as file:
        lines=file.readlines()
    while True:
        while len(lines)>i:
            print(lines[i].strip())
            i+=1
        else:
            exit()
if op.lower()=="exit":
    exit()