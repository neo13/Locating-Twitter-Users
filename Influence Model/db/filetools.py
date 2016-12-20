DATA_FOLDER = "../data/"


def get_file_path(filename):
    return DATA_FOLDER + filename


#this function reads the "filename" file from the data folder
#returns a list object containing all the tweets or users in the file
def parse_file(filename):
    import json
    f = open(get_file_path(filename))
    res = json.load(f)
    f.close()
    return res