'''
Created on Jul 30, 2019

@author: nambidiv
'''
import os
import git 
import fnmatch
import time
import collections, functools, operator 

class GitOperations: 
    #git log --after="2019-07-30" --before="2019-08-03" --oneline
    #command = ['git status']
    def __init__(self):
        # this we have to set from Environment Variable #os.environ["FUSION_HOME"]
        self.fusion_home = "C:/MYHP/CRM/Omni/omni/fusion/test/rest-tests/src/main/java/com/hp/ci/mgmt/" 
        #self.fusion_home = "C:/MYHP/services" 
        self.repo_path = "C:/MYHP/CRM/Omni/omni/"
        self.date_after = '2019-08-14'
        self.commitFile = []
        
#         self.commitFile = [{'name': 'C:/MYHP/services/compliance/BackupSecurityComplianceChecker.java', 'Date': '2019-08-13', 'count': 2}, {'name': 'C:/MYHP/services/compliance/BackupSecurityComplianceErrorKey.java', 'Date': '2019-08-13', 'count': 2},
#                             {'name': 'C:/MYHP/services/compliance/BackupSecurityComplianceEvent.java', 'Date': '2019-08-13', 'count': 2}, {'name': 'C:/MYHP/services/impl/BackupActionType.java', 'Date': '2019-08-14', 'count': 1},
#                             {'name': 'C:/MYHP/services/impl/BackupTrackerImpl.java', 'Date': '2019-08-14', 'count': 1},
#                             {'name': 'C:/MYHP/services/BackupConfigScheduler.java', 'Date': '2019-08-13', 'count': 3}]
        self.first = True    
  
    def search(self, name):
        for f in self.commitFile:
            if f['name'] == name:
                return self.commitFile.index(f)
        return -1
    def searchDirOrFile(self, name, isDir=True):
        for f in self.commitFile:
            if isDir:
                #dir_name= os.path.dirname(name)
                #searchDir = self.repo_path + os.path.dirname(f['name'])
                searchDir = os.path.dirname(f['name'])
                if searchDir.startswith(name):
                    return f['count']
            else:                
                searchFile = os.path.basename(f['name'])
                if name == searchFile:
                    return f['count']
        return 0 
    def getCommits(self, repo_path):
        repo = git.Repo(repo_path)
        # get all commits reachable from "HEAD"
        commits = list(repo.iter_commits('HEAD'))
        
        for commit in commits:
            commit_date = time.strftime('%Y-%m-%d', time.localtime(commit.committed_date))
            if self.date_after <= commit_date: 
                for file, stats in commit.stats.files.items():                                      
                    tempDict = {}
                    isExists = self.search(file)
                    if isExists >= 0: 
                        self.commitFile[isExists]['count'] = self.commitFile[isExists]['count'] + 1                        
                    else:
                        tempDict['name'] = file
                        tempDict['Date'] = commit_date
                        tempDict['count'] =  stats['lines']  
                        self.commitFile.append(tempDict)
            else:
                break                    
    def GetGitfiles(self, fusion_home):        
        for root, dirs, files in os.walk(fusion_home):            
            git_content = []
            rate_dir = 0
            rate = 0  
            for dir in dirs:
                # Excluding below directories as those are not required.  
                # Pending: We have to eclude /src/main/hp/ci/mgmt etc. Have to see how  
                if not(fnmatch.fnmatch(dir,'*.settings')) and not(fnmatch.fnmatch(dir,'*target')) and not(fnmatch.fnmatch(dir,'*-ws')): #and not(fnmatch.fnmatch(dir,'*src')) and not(fnmatch.fnmatch(dir,'*main')) and not(fnmatch.fnmatch(dir,'hp')) and not(fnmatch.fnmatch(dir,'ci')) and not(fnmatch.fnmatch(dir,'mgmt')):
                    full_path = os.path.join(fusion_home, dir).replace('\\','/')
                    find_children = os.path.join(full_path)
                    rate_dir+= self.searchDirOrFile(full_path)
                    git_content.append(self.GetGitfiles(find_children))                    
            for f in files:
                if not(fnmatch.fnmatch(f,'*.class')) and not(fnmatch.fnmatch(f,'*.jar')) and not(fnmatch.fnmatch(f,'*.txt')) and not(fnmatch.fnmatch(f,'*.lst')) and not(fnmatch.fnmatch(f,'*.sh')):
                    rate = self.searchDirOrFile(f,False)
                    rate_dir+=rate
                    git_content.append({'name': f, 'rate': rate, 'value': 1, 'children': ''})                        
            return {'name': os.path.basename(root), 'rate': rate_dir/1000, 'value': len(files), 'children': git_content}
if __name__ == '__main__':
    gitOp = GitOperations()
    gitOp.getCommits(gitOp.repo_path)
    #gitOp.sumListDict()
    print(gitOp.commitFile)    
    x = gitOp.GetGitfiles(gitOp.fusion_home)
    print(x)
