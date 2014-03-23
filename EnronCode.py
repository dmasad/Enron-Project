'''
ENRON CORPUS READER

Code for reading through the Enron Corpus and extracting useful data for 
analysis.
'''

import os

def get_all_files(path):
    '''
    Recursively find all files below the given path.
    
    Iterate over all objects in path. Open all sub-directories and call self, and
    return a list of all non-directory file paths.
    '''
    paths = []
    subdirs = [] 
    for name in os.listdir(path):
        name = os.path.join(path, name)
        if os.path.isdir(name):
            subdirs.append(name)
        else:
            paths.append(name)
            
    for subdir in subdirs:
        paths += get_all_files(subdir)
    return paths



def starts_with(line, text):
    '''
    Helper function to check whether the line starts with the given text.

    Args:
        line: Some line to check
        text: The string to check whether it is at the very beginning 
            of the line.
    '''
    n = len(text)
    if len(line) >= n and line[:n] == text:
        return True
    else:
        return False


def get_header(text):
    '''
    Extract the header information from an Enron email.

    Iterate through the email line by line, reading the start of each line and
    using it to figure out the current state. Should be robust to multi-line 
    To:, Cc: and Bcc: fields.

    TODO: Parse date, 

    '''
    lines = text.split("\n")
    state = "START"
    message = {}
    for line in lines:
        #if line[:5] == "Date:":
        if starts_with(line, "Date:"):
            message["Date"] = line.split(":", 1)[1]
        elif starts_with(line, "From:"):
            message["From"] = line.split(":", 1)[1] 
        elif starts_with(line, "To:"):
            state = "To"
            message["To"] = line.split(":", 1)[1]
        elif starts_with(line, "Cc:"):
            state = "Cc"
            message["Cc"] = line.split(":", 1)[1]
        elif starts_with(line, "Bcc:"):
            state = "Bcc"
            message["Bcc"] = line.split(":", 1)[1]
        # State terminators:
        elif starts_with(line, "Subject:"):
            state = "Subject"
        elif starts_with(line, "X-From:"):
            break
        elif starts_with(line, "Mime-Version:"):
            state="Mime-Version"
        # Begin instructions for multi-line field handling:
        elif state in ["To", "Cc", "Bcc"]:
            message[state] += line
    return message