#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

import git
import os
from Api.MysqlApi import DbOpt


try:
    import ConfigParser as conf
except ImportError as e:
    import configparser as conf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = conf.ConfigParser()
config.read(os.path.join(BASE_DIR, 'conf/autoconfig.ini'))




class GitOpt:
    def __init__(self,gitAdd,branch,codeName):
        self.gitAdd = gitAdd
        self.codeDir = config.get('code','dir')+codeName
        self.branchName = branch

    def clone(self):
        try:
            git.Repo.clone_from(self.gitAdd,to_path=os.path.join(self.codeDir),branch="master")
            return 0
        except Exception as err:
            return str(err)
    @property
    def repo(self):
        return git.Repo(os.path.join(self.codeDir))

    def activebranch(self):
        try:
            return self.repo.active_branch
        except Exception as err:
            return str(err)


    def createhead(self,branchname):
        self.repo.create_head(branchname)


    def checkout(self,branchname):
        self.repo.git.checkout(branchname)


    def remotepull(self,branchname):
        self.remote = self.repo.remote()
        return self.remote.pull(branchname)


    def remotepush(self,branchname):
        self.remote = self.repo.remote()
        self.remote.push(branchname)


    def createtag(self,tagname,tagmess):
        self.repo.create_tag(tagname,message=tagmess)

if __name__=="__main__":
    git_add = 'ssh://git@192.168.1.228:7999/yun/test.git'
    branch = "master"
    dbcon = DbOpt().con()
    cur = dbcon.cursor()
    cur.execute('select git_name from gitinfo where git_ssh="ssh://git@192.168.1.228:7999/yun/test.git"')
    for data in cur.fetchall():
        codedir = data[0]
        repo = GitOpt(git_add,branch,codedir)
        print(repo.codeDir)
        # repo = git.Repo('/data/code/test')
        print(repo.repo.git.branch('-r').split())


        # localCommit = repo.repo.head.reference.commit
        # repo.remotepull("master")
        # remoteCommit = repo.repo.head.reference.commit
        # print(localCommit,remoteCommit)
        # if localCommit != remoteCommit:
        #     print("项目有更新")
        # else:
        #     print("项目没有更新")


    #a = repo.clone()
    #repo = GitApi(git_add, branch, 'test')
    #a = repo.activebranch()
    #print(a)
    #repo.createhead("release/121")
    #repo.checkout("master")
    #repo.checkout("master")
    #repo.remotepull("master")
    #a = repo.activebranch()
    #print(a)
    #repo.createhead('v.0.1')
    #repo.createtag('v.0.1','v.0.1')
    #repo.remotepush('v.0.1')


