import zipfile
import argparse
from itertools import product
import time

parser = argparse.ArgumentParser(description='CompressedCrack v1.0.1 by ThanhMinh', epilog='Use the -h for help')
parser.add_argument('-i', '--input', help='Insert the file path of compressed file', required=True)
parser.add_argument('rules', nargs='*', help='<min> <max> <character>')

# Const Character
CHARACTER = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/"


class Handler:
    def __init__(self, input, rules):
        self.rules = rules
        self.location = input
        if len(rules) == 0:
            self.character = CHARACTER
            self.rules = False
        elif len(rules) == 3:
            if rules[1] < rules[0]:
                print("Range error")
                parser.exit()
            self.startLength = int(rules[0])
            self.maxLength = int(rules[1])
            self.character = rules[2]
            self.rules = True
        else:
            print("wrong rules number: <min> <max> <character> ")
            parser.exit()
        self.done = False

        self.zipfile = zipfile.ZipFile(self.location)
        self.todo()

    def todo(self):
        self.start_time = time.clock()
        print('Cracking...')
        if not self.rules:
            length = 1
            while True:
                self.creatpwd(length)
                if self.done:
                    return
                length += 1
        else:
            for length in range(self.startLength, self.maxLength + 1):
                self.creatpwd(length)
                if self.done:
                    return
            if not self.done:
                print('Cannot find password with this rules')
                return

    def creatpwd(self, length):
        listpass = product(self.character, repeat=length)
        for Pass in listpass:
            trypass = ''.join(Pass)
            self.unzip(trypass)
            if self.done:
                return

    def unzip(self, password):
        try:
            trypass = password.encode()
            print(trypass)
            self.zipfile.extractall(pwd=trypass)
            print('Complete')
            print('Time:', time.clock() - self.start_time, 's')
            print('Password:', password)
            self.done = True
        except:
            pass


def main():
    args = parser.parse_args()
    Handler(args.input, args.rules)


if __name__ == '__main__':
    main()
