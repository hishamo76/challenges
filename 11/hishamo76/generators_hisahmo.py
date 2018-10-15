""" generate a dictionary counter"""
from collections import defaultdict
import operator
import re
import os
import fnmatch


def gen_cat(filehandles):
    for fh in filehandles:
        for item in fh:
            yield item


def gen_grep(pattern, lines):
    c_pattern = re.compile(pattern)
    for line in lines:
        if c_pattern.search(line):
            yield line


def gen_find(pattern, dir):
    for path, listOfDir, listOfFiles in os.walk(dir):
        for name in fnmatch.filter(listOfFiles, pattern):
            yield os.path.join(os.path.abspath(path), name)


def gen_dict(line):
    import_dict = defaultdict(int)
    for item in line:
        newline = re.sub("import", '', item).strip()
        import_dict[newline] += 1
    return import_dict


def gen_open(files):
    for file in files:
        with open(file, encoding='utf-8') as fh:
            yield fh


if __name__ == "__main__":
    pyfiles = gen_find("*.py", "..\\..\\")
    pyfiles_handles = gen_open(pyfiles)
    pylines = gen_cat(pyfiles_handles)
    import_lines = gen_grep("^import", pylines)
    d = gen_dict(import_lines)

    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    for k, v in sorted_d:
        print(k, v)
