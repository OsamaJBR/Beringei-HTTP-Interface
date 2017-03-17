from subprocess import Popen, PIPE
import subprocess
import logging
import collections
import sys
import time
import os
# Logger
logger = logging.getLogger(__name__)
# current working directory
here = os.path.dirname(__file__)

class Beringei():
    def __init__(self,config):
        self.PATH=config.get('beringei','bin_path')
        self.GET_bin='%sberingei_get' %self.PATH
        self.PUT_bin='%sberingei_put' %self.PATH
        self.CONFIG_file=config.get('beringei','config_file')
    
    def clean_key(self,key):
        if any(char in key for char in ['%','$','?','#',';',',','\\',' ']): return False
        return True
        
    def get_key(self,KEY,OPTIONS='',sort=False,asc=True):
        if not self.clean_key(KEY.strip()): return False
        command='%s %s -beringei_configuration_path %s %s' %(self.GET_bin,OPTIONS,self.CONFIG_file,KEY)
        process = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        stdout, stderr = process.communicate()
        if stderr :
            logger.error('Getting key %s failed : command=%s key=%s error=%s',KEY,command,KEY,stderr)
            return False
        data={}
        for line in stdout.split('\n'):
            if len(line) <= 0 : continue
            line_data=line.split()
            data[int(line_data[2])]=line_data[1]
        if not sort : return data
        else : 
            if asc : return sorted(data.items())
            else : return sorted(data.items(),reverse=True)

    def put_key(self,KEY,VALUE,OPTIONS=''):
        if not self.clean_key(KEY.strip()) or \
           not self.clean_key(VALUE.strip()): return False
        command='%s %s -beringei_configuration_path %s %s %s' %(self.PUT_bin,OPTIONS,self.CONFIG_file,KEY,VALUE)
        process = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0 : 
            logger.error('Putting key %s failed : command=%s key=%s value=%s error=%s',KEY,command,KEY,VALUE,stderr)
            return False
        return True