#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
import os
import json
import GitOperations
#from gitBackend import *
from flask import Flask,render_template,redirect, url_for, request,session,escape
#from tkinter.test.runtktests import this_dir_path

app = Flask(__name__)

@app.route('/')
def hello():
    # We have to take this from Fusion Home ?     
    gitOp = GitOperations.GitOperations()
    gitOp.getCommits(gitOp.repo_path)
    d = gitOp.GetGitfiles(gitOp.fusion_home)
    print(d)
    return render_template('try.html', x=d)
    #return json.dumps(path_to_dict(path));

def recursionForDirectoty(dir_path):
    for root, subdirs, files in os.walk(dir_path):
        print(subdirs)

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"        
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir\
(path)]
    else:
        d['type'] = "file"
    return d

if __name__ == "__main__":
   #app.run(threaded=True,ssl_context=('cert.pem', 'key.pem'))
   app.run(threaded=True, debug=True, host="0.0.0.0", port="443")


