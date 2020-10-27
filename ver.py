import os
import random
import sys
from time import time
import click


def encryptFile(input_file, key, output):
    output = \
        output if os.path.isfile(output) else os.path.join(output, os.path.basename(input_file)) + '.dec'
    key = key if os.path.isfile(key) else os.path.join(key, os.path.basename(input_file) + '.dec.key')
    with open(input_file, 'rb') as inf, open(key, 'wb') as keyf, open(output, 'wb') as outf:
        byte_in = inf.read(1)
        while byte_in:
            new_key = random.randint(0, 255)
            keyf.write(bytes([new_key]))
            new_byte = bytes([ord(byte_in) ^ new_key])
            outf.write(new_byte)
            byte_in = inf.read(1)


def decryptFile(input_file, key, output_file):
    output_file = output_file if os.path.isfile(output_file) else os.path.join(output_file,
                                                                       os.path.basename(input_file).split('.dec')[0])
    key = key if os.path.isfile(key) \
        else os.path.join(key, os.path.basename(input_file) + '.key')

    with open(input_file, 'rb') as inf, open(key, 'rb') as keyf, open(output_file, 'wb') as outf:
        byte_in = inf.read(1)
        while byte_in:
            new_key = keyf.read(1)
            new_byte = bytes([ord(new_key) ^ ord(byte_in)])
            outf.write(new_byte)
            byte_in = inf.read(1)


@click.group()
def process():
    pass


@click.command()
@click.option("-s", "--seed", type=click.INT)
@click.option("-i", "--input", "fileinput", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option("-o", "--output", type=click.Path(file_okay=True, dir_okay=True))
@click.option("-k", "--key", type=click.Path(file_okay=True, dir_okay=True))
def encode(seed, fileinput, output, key):
    if os.path.isfile(fileinput):  # decrypt one file
        if not key:
            key = os.path.dirname(fileinput)
        if not output:
            output = os.path.dirname(fileinput)
        # output = \
        #     output if os.path.isfile(output) else os.path.join(output, os.path.basename(fileinput)) + '.dec'
        # key = key if os.path.isfile(key) else os.path.join(key, os.path.basename(fileinput) + '.dec.key')

        encryptFile(fileinput, key, output)
    else:
        if not key:
            key = fileinput
        if not output:
            output = fileinput
        if not os.path.isfile(key) and not os.path.isfile(output):  # decrypt many files
            if not os.path.isdir(key):
                os.mkdir(key)
            if not os.path.isdir(output):
                os.mkdir(output)
            for file in os.listdir(fileinput):
                if os.path.isfile(os.path.join(fileinput, file)):
                    encryptFile(os.path.join(fileinput, file), key, output)
                else:
                    print(file, 'is dir - skip')


@click.command()
@click.option("-i", "--input", "fileinput", type=click.Path(exists=True, file_okay=True), required=True)
@click.option("-k", "--key", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option("-o", "--output", type=click.Path(dir_okay=True, file_okay=True))
def decode(fileinput, key, output):
    # in - file:
    #   key - file
    #       out - file or dir
    #   key - dir:
    #       key = key + in.file
    #       out - file or dir
    # in - dir:
    #   key - dir:
    #       out - dir
    # else: error

    if os.path.isfile(fileinput):  # decrypt one file
        if not key:
            key = os.path.dirname(fileinput)
        if not output:
            output = os.path.dirname(fileinput)

        decryptFile(fileinput, key, output)

    else:
        if not os.path.exists(output):
            os.mkdir(output)
        if not key:
            key = fileinput
        if not output:
            output = fileinput
        if not os.path.isfile(key) and not os.path.isfile(output):  # decrypt many files
            for file in os.listdir(fileinput):
                if os.path.isfile(os.path.join(fileinput, file)):
                    decryptFile(os.path.join(fileinput, file), key, output)
                else:
                    print(file, 'is dir - skip')


process.add_command(encode)
process.add_command(decode)

# print('''
#                     oooooo     oooo
#                     `888.     .8'
#                      `888.   .8'    .ooooo.  oooo d8b ooo. .oo.    .oooo.   ooo. .oo.  .oo.
#                       `888. .8'    d88' `88b `888""8P `888P"Y88b  `P  )88b  `888P"Y88bP"Y88b
#                        `888.8'     888ooo888  888      888   888   .oP"888   888   888   888
#                         `888'      888    .o  888      888   888  d8(  888   888   888   888
#                          `8'       `Y8bod8P' d888b    o888o o888o `Y888""8o o888o o888o o888o
#
#
#         ''')

if __name__ == "__main__":
    process()
