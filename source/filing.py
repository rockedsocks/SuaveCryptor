## This is really meant for organization lol


def save(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
    except:
        with open(file_path, 'wb') as file:
            file.write(text)


def read(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            return ''.join(content) # readlines returns a list, it must be concatated to a string
    except UnicodeDecodeError: # When file is a byte file
        with open(file_path, 'rb') as file:
            return file.read()
