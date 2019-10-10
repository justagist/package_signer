Convenience package for signing (adding comment text on top of) all files in a package using a Signature (file).

### Details

* Can specify arguments to fill information automatically based on each file in the package (see below)
* Currently supports signing on files written in python, cpp (and .h), c#, c, html, css, php, javascript, matlab, arduino (ino), shell script


### Setup

* Run `python setup.py install`

### Usage

`sign_package [-h] [--signature path_to_signature_txt_file] [--BLOCK | --LINE] [--verbose] [--exclude [list_of_files_to_exclude ...]] package_or_file_to_sign`

Positional arguments:
	* package_or_file_to_sign   Path to package or file that has to be signed.

Optional arguments:
  * --signature, -s 			Path to file containing signature.
  * --BLOCK               		Sign using 'BLOCK' style (signature will be written as block comment if available)
  * --LINE                		Sign using 'LINE' style (default)
  * --exclude, -x 				Space-separated files to be ignored during signing.

### Signature File

The signature file accepts keywords that will be replaced by induvidual information based on each file being signed

* Name of the file : &nbsp;&nbsp;&nbsp;--file_name--					
* Name of the immediate parent directory: &nbsp;&nbsp;&nbsp;--parent_folder_name--		
* Full path in the git repository (if not in git repo, uses parent folder name): &nbsp;&nbsp;&nbsp;--full_path_in_package--		
* Name of git repository (root directory) if in git repo, else uses parent folder name): &nbsp;&nbsp;&nbsp;--repo_name--					
* User name as defined in git config for the repo (If not found, space is left empty): &nbsp;&nbsp;&nbsp;--git_username--				
* Name of package (destination argument passed to the script): &nbsp;&nbsp;&nbsp;--package_name--				