#!/usr/bin/env python3
# Generate a dict file by source and destinate files 

import sys
if __name__ == '__main__':
    argc = len(sys.argv)
    print('Generate dict')
    if argc < 4:
        exit(0)
    src = sys.argv[1]
    dest = sys.argv[2]
    result = sys.argv[3]

    print('Source file:', src)
    print('Destinate file:', dest)
    print('Reslut file:', result)
    with open(src) as fsrc:
        src_words = fsrc.read().split('\n')
    with open(dest) as fdest:
        dest_words = fdest.read().split('\n')
    merge = list(zip(src_words, dest_words))
    result_words = list(map(
        lambda x:(x[0].strip() + ', ' + x[1].strip()), merge))
    with open(result, 'w+') as fresult:
        fresult.write('\n'.join(result_words))
        print('Generate dict successfully.')

