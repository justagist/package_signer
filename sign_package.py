#! /usr/bin/env python3

import os, subprocess
import argparse
import git

file_types = {'py':['#',"'''"],'c':[],'cpp':[],'h':[],'sh':[],'bash':[],'html':[],'css':[],'js':[],'php':[]}

ignore_list = ['pyc', 'md', 'txt', 'gitignore', 'json']


class Signature:

    def __init__(self, split_line_list, metadata):

        self.data = split_line_list
        try:
            self.author_words = metadata['author_words']
        except KeyError:
            self.author_words = []
        try:
            self.repo_name_words = metadata['repo_name_words']
        except KeyError:
            self.repo_name_words = []
        try:
            self.file_name_words = metadata['file_name_words']
        except KeyError:
            self.file_name_words = []
        try:
            self.folder_name_words = metadata['folder_name_words']
        except KeyError:
            self.folder_name_words = []

def in_git_path(file):

    if subprocess.call(["git", "branch"], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w')) != 0:
        return False
    else:
        return True


def crawl_package(path):

    fname = []
    for root,d_names,f_names in os.walk(path):
        for f in f_names:
            if f.split('.')[-1] in ignore_list:
                continue
            fname.append(os.path.join(root, f))

    return fname


def sign_package(signature, style = "LINE"):
    pass

def get_signature(signature_file, package_path = "./"):

    sign_file = open(signature_file,"r")
    original_txt = sign_file.readlines()

    sign_file.close()

    final_txt = ''
    line_num = 0

    split_line_list = []
    metadata = {'folder_name_words':[],'repo_name_words':[],'file_name_words':[],'author_words':[]}
    for line in original_txt:

        splitline = line.split()
        if len(splitline) > 1:
            if splitline[0] == '!--' and splitline[-1] == "--!":
                continue

        for word_num in range(len(splitline)):
            if splitline[word_num] == '--repo_author--':
                metadata['author_words'].append([line_num,word_num])
                splitline[word_num] = "< Name of the git repo author will appear here >"

            elif splitline[word_num] == '--parent_folder_name--':
                metadata['folder_name_words'].append([line_num,word_num])
                splitline[word_num] = "< The parent folder name of each file will appear here >"

            elif splitline[word_num] == '--repo_name--':
                metadata['repo_name_words'].append([line_num,word_num])
                splitline[word_num] = "< Name of the git repo (if found) will appear here. If not found, will use parent folder name. >"

            elif splitline[word_num] == '--file_name--':
                metadata['file_name_words'].append([line_num,word_num])
                splitline[word_num] = "< Name of the file will appear here. >"

        final_txt += "\n%s"%" ".join(splitline)
        split_line_list.append(splitline)
        line_num += 1


    print ("\nSignature content:\n\n--BEGIN--\n%s\n--END--\n"%final_txt)


    return Signature( split_line_list = split_line_list, metadata = metadata)



    # pass



if __name__ == '__main__':

    

    parser = argparse.ArgumentParser(description="Add signature lines in all files of a package.")
    # parser.add_argument('--destination_folder', metavar='-D', action = "store", help='Path to the root of the package to sign')
    parser.add_argument('destination', help = "Path to package that has to be signed.")
    parser.add_argument('--signature', '-s', help = "Path to file containing signature.", default = "signature.txt")

    style_group = parser.add_mutually_exclusive_group()

    style_group.add_argument('--BLOCK', action = "store_true", help = "Sign using 'BLOCK' style")
    style_group.add_argument('--LINE', action = "store_true", help = "Sign using 'LINE' style (default)")

    args = parser.parse_args()

    # print (args.BLOCK)

    style = 'LINE'
    if args.BLOCK:
        style = "BLOCK"

    print ("HERE\n")
    # print (args.destination)
    repo = git.Repo("./test", search_parent_directories = True)
    print (repo.__dict__)

    signature = get_signature(args.signature, args.destination)




    # print(file_types)