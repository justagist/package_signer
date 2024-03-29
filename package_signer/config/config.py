
#  
#     @author: JustaGist 
#     @package: package_signer 
#     	Easily sign all files in a package using file-specific information. 
#  
#     @file: config.py 
#  

import os
base_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2])

# =====================================================================================================
# =====================================================================================================

'''
	This is the config file that can be modified by user to include more file types and comment syntax. 
	THE PACKAGE HAS TO BE REINSTALLED AFTER MAKING EDITS HERE!!

'''
							# EXTENSION     	SINGLE-LINE COMMENT         MULTI-LINE COMMENT

EXTENSION_COMMENT_SYNTAX = { 
                              'py' :        [   ['#','']        ,           ["'''","'''"]       ],
                              'c' :         [   ['//','']       ,           ['/*','*/']         ],
                              'cpp' :       [   ['//','']       ,           ['/*','*/']         ],
                              'h' :         [   ['//','']       ,           ['/*','*/']         ],
                              'sh' :        [   ['#','']       ,              None             ],
                              'bash' :      [   ['#','']       ,              None             ],
                              'html' :      [   ['<!--','-->']  ,           ['<!--','-->']      ],
                              'css' :       [   ['/*','*/']     ,           ['/*','*/']         ],
                              'js' :        [   ['//','']       ,           ['/*','*/']         ],
                              'php' :       [   ['//','']       ,           ['/*','*/']         ],
                              'ino' :       [   ['//','']       ,           ['/*','*/']         ],
                              'm' :         [   ['%','']        ,           ['%{','%}']         ],
                              }



# =====================================================================================================
# =====================================================================================================

