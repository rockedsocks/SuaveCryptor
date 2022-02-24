## This is really meant for organization lol


def save(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)


def read(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    return ''.join(content) # readlines returns a list, it must be concatated to a string
