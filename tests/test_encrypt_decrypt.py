import pytest
import os
import random
import sys

os.chdir('tests')

from ver import encryptFile, decryptFile

testdata = [
    ('files/input1', 'files/key1', 'files/out1'),
    ('files/input2', 'files/key2', 'files/out2'),
    ('files/input3.jpg', 'files/key3', 'files/out3'),
]


def teardown():
    if os.path.exists("key_test"):
        os.remove("key_test")
    if os.path.exists("out_test"):
        os.remove("out_test")
    if os.path.exists("input_test"):
        os.remove("input_test")


@pytest.mark.parametrize("input,key,output", testdata)
def test_encrypt(input, key, output):
    random.seed(1)
    encryptFile(input, 'key_test', 'out_test')
    with open(key, 'rb') as key_check, open('key_test', 'rb') as key_test:
        assert key_test.read() == key_check.read()

    with open(output, 'rb') as key_check, open('out_test', 'rb') as key_test:
        assert key_test.read() == key_check.read()


@pytest.mark.parametrize("input,key,output", testdata)
def test_decrypt(input, key, output):
    decryptFile(output, key, 'input_test')
    with open(input, 'rb') as input_check, open('input_test', 'rb') as input_test:
        assert input_test.read() == input_check.read()