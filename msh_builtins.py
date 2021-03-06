## Python3.5
## Builtin Programs

version = "1.4.1"

import os as _msh_os
import readline as _msh_readline
import sys as _msh_sys
from glob import glob as _glob

## Initial Exit Status
status = 0

## History Config
histfile = "{}/.msh_history".format(_msh_os.environ["HOME"])
_msh_readline.set_history_length(1000)

## Commands And Functions
def msh_cd(param):
          if len(param) == 1:
                    _msh_os.chdir(_msh_os.environ["HOME"])
                    return 0
          else:
                    _path = param[1]
                    
                    if param[1] == "-":
                              print(_msh_os.getcwd())
                              return 0
                    else:
                              try:
                                        _msh_os.chdir(_path)
                                        return 0
                              except Exception as e:
                                        print("cd: error:", e.args[1] + ":", _path)
                                        return e.errno

## Add Parameters To a Command
alias = {"ls"    :  "--color=auto",
         "grep"  :  "--color=auto"}

def _msh_exec(param):
          for addParam in alias:
                    if param[0] == addParam:
                              param.append(alias[addParam])
                              break

          pid = _msh_os.fork()

          if pid == 0:
                    try: _msh_os.execvp(param[0], param)
                    except Exception as e:
                              print("matrixsh: error:", e.args[1] + ":", param[0])
                              exit(e.errno)
          elif pid < 0: print("*** Fork Error")
          else: return _msh_os.waitpid(pid, 0)[1]

def msh_exit(ignore):
          _msh_readline.write_history_file(histfile)
          exit(0)

## List Of Programs
programlist = {"cd"    :  msh_cd,
               "exit"  :  msh_exit}

## To run complete when TAB key is pressed
_msh_readline.parse_and_bind("TAB: complete")

## Matrix Shell Completer
def msh_completer(text, state):
          options, matches = [], []
          
          ## Files Completions
          for files in _glob(text + "*"): options.append(files)
          
          ## Programs Completions
          for progsDirectory in _msh_os.environ["PATH"].split(":"):
                    for programs in _glob(progsDirectory + "/*"): options.append(_msh_os.path.basename(programs))
          
          ## Builtin Programs Completions
          for builtins in programlist: options.append(builtins)
          
          if text:
                    for chars in options:
                              if chars[:len(text)] == text: matches += [chars]
          
          return matches[state]

## Default Prompt
prompt = "> "

def msh_display_completions(L_buffer, matches, N_matches):
          print()
          
          ## Set files colors
          basename = _msh_os.path.basename
          for item in range(len(matches)):
                    try:
                              file_type = _msh_os.stat(matches[item], follow_symlinks=False).st_mode
                              if    file_type == 16877  :  matches[item] = "\033[1;34m" + basename(matches[item]) + "\033[00m"
                              elif  file_type == 41471  :  matches[item] = "\033[1;36m" + basename(matches[item]) + "\033[00m"
                              elif  file_type == 33261  :  matches[item] = "\033[1;32m" + basename(matches[item]) + "\033[00m"
                              else                      :  matches[item] = "\033[1;00m" + basename(matches[item]) + "\033[00m"
                    except FileNotFoundError            :  matches[item] = "\033[1;00m" + basename(matches[item]) + "\033[00m"
                    ## BUG: it'll never return a string with \ or without \
                    matches[item] = matches[item].replace(" ", "\\ ")
          
          ## Separate in columns
          match, elem, line = [[]], 0, 0
          while elem < len(matches):
                    match[line] += [matches[elem]]
                    
                    if len(match[line]) == 5:
                              match += [[]]
                              line += 1
                    
                    elem += 1
          
          ## Print Columns
          column = max(len(word) for sub_list in match for word in sub_list) + 2
          for lists in match: print(" ".join(word.ljust(column) for word in lists))
          
          ## Prompt
          print(prompt + _msh_readline.get_line_buffer(), end="")
