import os
def base10_to_baseN(num, base):
    if base > 191:
        raise ValueError("Base too large. Maximum base supported is 191.")
    printable_ascii_chars = [chr(i) for i in range(32, 127)]
    latin1_supplement_chars = [chr(i) for i in range(160, 256)]
    base_chars = printable_ascii_chars + latin1_supplement_chars
    if " " in base_chars:
        base_chars.remove(" ")
    if num == 0:
        return base_chars[0]
    baseN_str = ''
    while num > 0:
        remainder = num % base
        baseN_str = base_chars[remainder - 1] + baseN_str
        num = num // base
    return baseN_str
def baseN_to_base10(num_str, base):
    printable_ascii_chars = [chr(i) for i in range(32, 127)]
    latin1_supplement_chars = [chr(i) for i in range(160, 256)]
    base_chars = printable_ascii_chars + latin1_supplement_chars
    if " " in base_chars:
        base_chars.remove(" ")
    base10_num = 0
    for char in num_str:
        base10_num = base10_num * base + base_chars.index(char) + 1
    return base10_num
def handle_write(file_rw, words_file_path):
    with open(words_file_path, 'r', encoding='utf-8') as file:
        words = [word.strip() for word in file.readlines()]
    word_to_index = {word: i + 1 for i, word in enumerate(words)}
    
    while True:
        line_file = []
        line = input("Enter a line of text (or 'exit' to finish): ").strip()
        if line.lower() == "exit":
            break
        line_list = line.split(" ")
        
        new_words = []
        for word2 in line_list:
            if word2 in word_to_index:
                line_file.append(word2 + " ")
            else:
                new_words.append(word2)
                word_to_index[word2] = len(word_to_index) + 1
                line_file.append(word2 + " ")
        if new_words:
            with open(words_file_path, "a", encoding='utf-8') as file:
                for new_word in new_words:
                    file.write("\n"+new_word)
        
        if line_file:
            with open(f"{file_rw}.txt", "a", encoding='utf-8') as file:
                if os.stat(f"{file_rw}.txt").st_size > 0:
                    file.write("\n")
                file.writelines(line_file)
def handle_read(file_rw):
    with open(f"{file_rw}.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        print(line.strip())
def handle_compress(file_rw, words_file_path):
    with open(words_file_path, 'r', encoding='utf-8') as file:
        words = [word.strip() for word in file.readlines()]
    with open(f"{file_rw}.txt", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    word_to_index = {word: i + 1 for i, word in enumerate(words)}
    compressed_lines = []
    for line in lines:
        words_in_line = line.strip().split(" ")
        compressed_line = []
        for word in words_in_line:
            if word in word_to_index:
                word_index = word_to_index[word]
                compressed_word = base10_to_baseN(word_index, 191)
                compressed_line.append(compressed_word)
            else:
                compressed_line.append(word) 
        compressed_lines.append(' '.join(compressed_line))
    compressed_text = '\n'.join(compressed_lines)
    compressed_file_name = f"{file_rw}_compressed.txt"
    with open(compressed_file_name, "w", encoding='utf-8') as file:
        file.write(words_file_path + "\n")
        file.write(compressed_text)
def decode(file_rw):
    compressed_file_name = f"{file_rw}_compressed.txt"
    with open(compressed_file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    words_file_path = lines[0].strip()
    with open(words_file_path, 'r', encoding='utf-8') as file:
        words = [word.strip() for word in file.readlines()]
    index_to_word = {i + 1: word for i, word in enumerate(words)}
    compressed_content = lines[1:]
    decoded_lines = []
    for compressed_line in compressed_content:
        words_in_line = compressed_line.strip().split(" ")
        decoded_line = []
        for compressed_word in words_in_line:
            if compressed_word:
                word_index = baseN_to_base10(compressed_word, 191)
                if word_index in index_to_word:
                    decoded_line.append(index_to_word[word_index])
                else:
                    decoded_line.append(compressed_word)
        decoded_lines.append(' '.join(decoded_line))
    decoded_text = '\n'.join(decoded_lines)
    print("Decoded content:")
    print(decoded_text)
def main():
    file_folder=__file__.split("main.py")
    words_file_path = file_folder[0]+"words (1).txt"
    file_rw = input("What file are you reading/writing? ")
    file_rw=file_folder[0]+file_rw
    while True:
        op = input("Input operation (write, read, compress, decode, exit): ").lower()
        if op == "write":
            handle_write(file_rw, words_file_path)
        elif op == "read":
            handle_read(file_rw)
        elif op == "compress":
            handle_compress(file_rw, words_file_path)
        elif op == "decode":
            decode(file_rw)
        elif op == "exit":
            break
        else:
            print("Invalid operation. Please choose write, read, compress, decode, or exit.")
if __name__ == "__main__":
    main()