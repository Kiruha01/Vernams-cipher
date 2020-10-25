import random
from time import time
import click


@click.group()
def process():
    pass


@click.command()
@click.option("-s", "--seed", type=click.INT)
@click.option("-i", "--input", "fileinput", type=click.Path(exists=True, file_okay=True), required=True)
@click.option("-o", "--output", type=click.Path(file_okay=True))
def encode(seed, fileinput, output):
    inp = open(fileinput, 'rb')
    out = open(output if output else fileinput+".dec", 'wb')
    outkey = open(output + '.key' if output else fileinput + '.dec.key', 'wb')
    byte_in = inp.read(1)
    while byte_in:
        key = random.randint(0, 256)
        outkey.write(chr(key).encode())
        new_char = chr(ord(byte_in) ^ key).encode()
        out.write(new_char)
        byte_in = inp.read(1)

    outkey.close()
    out.close()
    inp.close()


@click.command()
@click.option("-i", "--input", "fileinput", type=click.Path(exists=True, file_okay=True), required=True)
@click.option("-k", "--key", type=click.Path(exists=True, file_okay=True))
def decode(fileinput, key):
    inp = open(fileinput, "rb")
    in_key = open(key if key else fileinput + '.key', 'rb')
    out = open(fileinput.split(".dec")[0], "wb")
    byte_in = inp.read(1)
    while byte_in:
        key = in_key.read(1)
        new_char = chr(ord(key) ^ ord(byte_in)).encode()
        out.write(new_char)
        byte_in = inp.read(1)

    out.close()
    inp.close()
    in_key.close()


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
