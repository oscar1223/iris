###
# Class that returns the hash of a given file
# ###

import hashlib

# Method that returns the hash of an image

def hash_generate(imagen):
    hash = hashlib.sha1()
    with open(imagen, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash.update(byte_block)
    return hash.hexdigest()
