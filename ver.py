import os
import random
import click


def encryptFile(input_file, key, output):
    print('encrypting', input_file, end='...')
    with open(input_file, 'rb') as inf, open(key, 'wb') as keyf, open(output, 'wb') as outf:
        byte_in = inf.read(1)
        while byte_in:
            new_key = random.randint(0, 255)
            keyf.write(bytes([new_key]))
            new_byte = bytes([ord(byte_in) ^ new_key])
            outf.write(new_byte)
            byte_in = inf.read(1)
    print('done')


def decryptFile(input_file, key, output_file):
    print('decrypting', input_file, end='...')
    with open(input_file, 'rb') as inf, open(key, 'rb') as keyf, open(output_file, 'wb') as outf:
        byte_in = inf.read(1)
        while byte_in:
            new_key = keyf.read(1)
            new_byte = bytes([ord(new_key) ^ ord(byte_in)])
            outf.write(new_byte)
            byte_in = inf.read(1)
    print('done')


@click.group()
def process():
    """Encrypting and decrypting files via Vernam`s algorithm.
    Using XOR operation with each bytes.

    After encrypting you will get encrypted file *.dec and key
    *.dec.key. Key is a secure information.

    To decrypt you should give decrypted and key files."""
    pass


@click.command()
@click.option("-s", "--seed", type=click.INT, help="Seed of random")
@click.option("-i", "--input", "fileinput", type=click.Path(exists=True, file_okay=True, dir_okay=True),
              help="Source of input files. File or folder")
@click.option("-o", "--output", type=click.Path(file_okay=True, dir_okay=True), help="Destination of output file. File "
                                                                                     "or folder (if input is folder - "
                                                                                     "folder only!) ")
@click.option("-k", "--key", type=click.Path(file_okay=True, dir_okay=True),
              help="Destination of key files. File or folder (if input is folder - folder only!)")
def encrypt(seed, fileinput, output, key):
    """
    Encrypting files
    """
    random.seed(seed)
    if os.path.isfile(fileinput):  # and not folders:  # work with one file
        if not output:
            output = fileinput + '.dec'
        elif os.path.isdir(output):
            output = os.path.join(output, os.path.basename(fileinput) + '.dec')
        if not key:
            key = output + '.key'
        elif os.path.isdir(key):
            key = os.path.join(key, os.path.basename(output) + '.key')
        try:
            encryptFile(fileinput, key, output)
        except FileNotFoundError as e:
            print('error!')
            print(e, 'skipping..')

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
                    try:
                        encryptFile(os.path.join(fileinput, file), os.path.join(key, file + '.dec.key'),
                                    os.path.join(output, file + '.dec'))
                    except FileNotFoundError as e:
                        print('error!')
                        print(e, 'skipping..')
                else:
                    print(file, 'is dir - SKIP')


@click.command()
@click.option("-i", "--input", "fileinput", type=click.Path(exists=True, file_okay=True), required=True,
              help="Source of input encrypted filed. File of folder")
@click.option("-k", "--key", type=click.Path(exists=True, file_okay=True, dir_okay=True),
              help="Source of keys. File or folder (if input is folder - folder only!)")
@click.option("-o", "--output", type=click.Path(dir_okay=True, file_okay=True),
              help="Destination of output decrypted files. File of folder (if input is folder - folder only!)")
def decrypt(fileinput, key, output):
    """
    Decrypt files
    """
    if os.path.isfile(fileinput):
        if not key:
            key = fileinput + '.key'
        elif os.path.isdir(key):
            key = os.path.join(key, fileinput + '.key')
        if not output:
            output = fileinput.split('.dec')[0]
        elif os.path.isdir(output):
            output = os.path.join(output, fileinput.split('.dec')[0])
        try:
            decryptFile(fileinput, key, output)
        except FileNotFoundError as e:
            print('error!')
            print(e, 'skipping..')

    else:
        if not key:
            key = fileinput
        if not output:
            output = fileinput
        if not os.path.exists(output):
            os.mkdir(output)
        if not os.path.isfile(key) and not os.path.isfile(output):  # decrypt many files
            files = os.listdir(fileinput)
            for file in files:
                if os.path.isfile(os.path.join(fileinput, file)):
                    key_file = os.path.join(key, file + '.key')
                    output_file = os.path.join(output, file.split('.dec')[0])
                    try:
                        decryptFile(os.path.join(fileinput, file), key_file, output_file)
                    except FileNotFoundError as e:
                        print('error!')
                        print(e, 'skipping..')
                else:
                    print(file, 'is dir - SKIP')


process.add_command(encrypt)
process.add_command(decrypt)

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
