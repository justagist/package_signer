import os, subprocess
from package_signer.config import EXTENSION_COMMENT_SYNTAX

signature_keywords = {'file_name':'--file_name--',
                      'parent_folder_name':'--parent_folder_name--',
                      'full_path_in_package':'--full_path_in_package--',
                      'repo_name':'--repo_name--',
                      'git_username':'--git_username--',
                      'package_name':'--package_name--'}

SIGNFILE_COMMENT_CHAR = '#!'


def in_git_path(file):

    if subprocess.call(["git", "branch"], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w'), cwd = '/'.join(file.split('/')[:-1])) != 0:
        return False
    else:
        return True


class PackageSignatureGenerator:

    def __init__(self, signature_file, destination = None, style = "LINE", verbose = False, files_to_ignore = None):

        if style != "BLOCK" and style != "LINE":
            raise ValueError("Unknown Signature Style: %s"%style)

        self._verbose = verbose

        self._unsigned_files = [os.path.abspath(file) for file in files_to_ignore if os.path.exists(file) ] if files_to_ignore is not None else []

        print (self._unsigned_files)

        if not os.path.exists(signature_file) or not os.path.isfile(signature_file):
            raise IOError("Signature file '%s' does not exis or is invalid"%signature_file)

        self._original_txt = self._read_signature_file(signature_file)


        if self._verbose:
            print ("\nOriginal Signature Text:\n-----BEGIN-----\n%s\n-----END-----\n")

        if os.path.exists(destination):
            destination = os.path.abspath(destination)
        else:
            raise IOError("Destination '%s' does not exist."%destination)

        if os.path.isdir(destination):

            self._package_path = destination

            self._package_name = os.path.abspath(self._package_path).split('/')[-1]

            self._files_to_sign = self._crawl_package(self._package_path)
        else:
            self._package_path = None
            self._package_name = None
            self._files_to_sign = [destination]

        self._signature_style = 0 if style == "LINE" else 1


    @property
    def files_to_sign(self):
        return self._files_to_sign
    

    def _get_file_info(self, file):
        path_split = file.split('/')
        parent = path_split[-2]
        info = {'git_username':'','repo':parent, 'file_name':path_split[-1], 'parent':parent, 'full_path':parent,'package':self._package_name if self._package_name is not None else parent, 'extension':file.split('.')[-1]}

        if in_git_path(file):
            proc = subprocess.Popen(["git", "config", "user.name"], stdout=subprocess.PIPE, cwd = '/'.join(path_split[:-1]))
            out, err = proc.communicate()
            info['git_username'] = out.decode("utf-8").strip()

            proc = subprocess.Popen(["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, cwd = '/'.join(path_split[:-1]))
            out, err = proc.communicate()
            path_to_package = out.decode("utf-8").strip()
            info['repo'] = path_to_package.split('/')[-1]
            info['full_path'] = info['repo'] + file.split(path_to_package)[-1] 

        return info


    def _crawl_package(self, path):
        fname = []
        for root,d_names,f_names in os.walk(path):
            if '/.git/' in root or root[-5:] == '/.git':
                continue
            for f in f_names:
                if '.' not in f:
                    self._unsigned_files.append(os.path.join(root, f))
                    continue
                if f.split('.')[-1] not in EXTENSION_COMMENT_SYNTAX:
                    self._unsigned_files.append(os.path.join(root, f))
                    continue
                if os.path.join(root, f) in self._unsigned_files:
                    continue
                fname.append(os.path.join(root, f))

        return fname

    def _generate_signature_for_file(self,file):

        file_info = self._get_file_info(file)

        signature = self._original_txt

        signature = signature.replace(signature_keywords['file_name'],file_info['file_name'])
        signature = signature.replace(signature_keywords['parent_folder_name'],file_info['parent'])
        signature = signature.replace(signature_keywords['full_path_in_package'],file_info['full_path'])
        signature = signature.replace(signature_keywords['repo_name'],file_info['repo'])
        signature = signature.replace(signature_keywords['git_username'],file_info['git_username'])
        signature = signature.replace(signature_keywords['package_name'],file_info['package'])

        temp_sign_style =  self._signature_style if EXTENSION_COMMENT_SYNTAX[file_info['extension']][self._signature_style] is not None else int(not self._signature_style)

        comment_syntax = EXTENSION_COMMENT_SYNTAX[file_info['extension']][temp_sign_style]

        if temp_sign_style == 1:
            signature = "%s\n%s\n%s"%(comment_syntax[0],signature,comment_syntax[1])

        else:
            signature = "\n".join(["%s %s %s"%(comment_syntax[0],line,comment_syntax[1]) for line in signature.split('\n')])

        return "%s\n\n"%signature

    def sign_file(self, file):
        sign = self._generate_signature_for_file(file)
        if self._verbose:
            print("\n======\tSigning file: %s\n"%file)
            print(sign)
            print("\n") 
        else:
            print("Signing file: %s"%file)

        line_num = 0
        with open(file, 'r+') as fh:
            lines = fh.readlines()
            for line in lines:
                line_num += 1
                if line.strip() == '' or line.startswith('#!'):
                    continue
                else:
                    break
            else:
                print('\t\n( WARNING: Signing in Empty File )\n')

            fh.seek(0)
            lines.insert(line_num - 1, sign)
            fh.writelines(lines)
        if self._verbose:
            print("=================\n")


    def sign_package(self):

        if self._package_path is None:
            assert len(self._files_to_sign) == 1

        for file in self._files_to_sign:
            self.sign_file(file)

        if self._package_path is not None:
            print ("\nIgnored %d file(s)!\n%s\n"%(len(self._unsigned_files)," ".join(["\t%s\n"%file.split(self._package_path)[-1] for file in self._unsigned_files])))
            print ("\nSigned %d file(s)!\n"%len(self._files_to_sign))


    def _read_signature_file(self, signature_file):

        sign_file = open(signature_file,"r")
        original_txt = sign_file.readlines()

        sign_file.close()

        final_txt = ''

        split_line_list = []
        i = 0

        for line in original_txt:
            i+=1
            if SIGNFILE_COMMENT_CHAR in line:
                if line.startswith(SIGNFILE_COMMENT_CHAR):
                    continue
                commented_line = line.split(SIGNFILE_COMMENT_CHAR)
                line = commented_line[0]+'\n'

            line = line.rstrip() + '\n'
            splitline = line.split(' ')

            final_txt += " ".join(splitline)
            split_line_list.append(splitline)

        return final_txt[:-1] if final_txt[-1]=='\n' else final_txt