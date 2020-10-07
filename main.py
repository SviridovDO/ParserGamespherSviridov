import argparse
import os
import re
from tqdm import tqdm
import time


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', required=True)
    parser.add_argument('-r', required=True)
    parser.add_argument('-rf')
    args = parser.parse_args()
    return args


def files_path(args):
    if os.path.isfile(args.f):
        return [args.f]
    elif os.path.isdir(args.f):
        dirlist = os.listdir(path=args.f)
        if not dirlist:
            raise Exception('Folder is empty')
        else:
            r = re.compile(args.rf)
            return [args.f + '/' + f for f in os.listdir(path=args.f) if
                    os.path.isfile(args.f + '/' + f) and r.match(f)]
    else:
        raise Exception('Invalid path')


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def filter_lines(file_path, regexp, lines):
    print(f'File path: {file_path}')
    time.sleep(0.05)
    result = [file_path + '; ' + line + '\n' for line in tqdm(lines) if re.match(regexp, line)]
    write_file(result)
    return result


def write_file(lines):
    filename = 'output.log'
    with open(filename, 'a') as f:
        f.writelines(lines)


if __name__ == "__main__":
    args = read_args()
    files_path = files_path(args)
    count_files = len(files_path)
    count_files_now = 0
    for file_path in files_path:
        count_files_now += 1
        print(f'Reading {file_path} {count_files_now}/{count_files} files')
        lines = read_file(file_path).split('\n')
        regexp = args.r
        filter_lines(file_path, regexp, lines)