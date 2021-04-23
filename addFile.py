import sqlite3
import os
from stdiomask import getpass
import json


class AddFile():
    def __init__(self):
        self.db = sqlite3.connect(database='db.sqlite3')
        self.db_cursor = self.db.cursor()
        get_user_cmd = 'SELECT UACCOUNT FROM USERS;'
        self.db_cursor.execute(get_user_cmd)
        self.current_users = []
        for uaccount in self.db_cursor.fetchall():
            self.current_users.append(uaccount[0])

    def add_one_file(self,filename,filepath,belong):
        #获取文件大小信息
        try:
            filesize = os.path.getsize(filepath)
            filesize = str(filesize)
        except:
            print('filepath not correct!')
            print('consider using absolute path?')
            return -1
        #数据库操作
        #若选择的用户不存在
        if belong not in self.current_users:
            print('cannot find account %s'%belong)
            new_user = input('would you like to create a new user (Y/n)?')
            if new_user == 'y' or new_user == 'Y':
                #创建新用户
                #设置account
                account_valid = False
                while(not account_valid):
                    uaccount = input('the account you input previously is %s, please input a new account or leave blank to use the old one:'%belong)
                    if uaccount.isspace() or uaccount == '':
                        uaccount = belong
                    #检查是否重名：
                    if uaccount in self.current_users:
                        print('this account has existed, please use another string')
                    else:
                        account_valid = True
                #设置name
                uname = input('please input the username:')
                while(uname.isspace() or uname == ''):
                    uname = input('please input the username:')
                #设置密码
                pwd_valid = False
                while(not pwd_valid):
                    upwd = getpass('please input the password:')
                    upwd_twice = getpass('please input the password again:')
                    if upwd != upwd_twice:
                        print('the two passwords do not match! try it again.')
                    elif upwd.isspace() or upwd == '':
                        print('invalid password!')
                    else:
                        pwd_valid = True
                #设置用户文件（初始为空）
                ufiles = json.dumps([])
                #写入数据库
                insert_user_cmd = 'INSERT INTO USERS(uaccount,upassword, uname, ufiles)VALUES("%s","%s","%s","%s");'%(uaccount,upwd,uname,ufiles)
                self.db_cursor.execute(insert_user_cmd)
                self.db.commit()
            else:
                #重新输入用户
                account_valid = False
                while(account_valid):
                    uaccount = input('please input a new account')
                    if uaccount not in self.current_users:
                        print('this account does not exist!')
                    else:
                        account_valid = True
            #更新所有用户名单，这里事实上可以使用append
            belong = uaccount
            self.current_users.append(belong)
        #检查好账户后，写入文件信息到用户和文件数据库
        #插入file
        insert_file_cmd = 'INSERT INTO FILES(filename, filesize, filepath, belong)VALUES("%s","%s","%s","%s");'%(filename,filesize,filepath,belong)
        self.db_cursor.execute(insert_file_cmd)
        self.db.commit()
        #获取最新文件（即刚插入的文件）的id
        get_fid_cmd = 'SELECT ID FROM FILES;'
        self.db_cursor.execute(get_fid_cmd)
        fid_list = self.db_cursor.fetchall()
        #返回的结果格式为：[(1,), (2,), (3,), (4,)]
        latest_id = fid_list[0][0]
        for fid in fid_list:
            if fid[0] > latest_id:
                latest_id = fid[0]
        #设置ufiles:
        get_ufiles_cmd = 'SELECT UFILES FROM USERS WHERE UACCOUNT = "%s";'%belong
        self.db_cursor.execute(get_ufiles_cmd)
        ufiles = self.db_cursor.fetchall()[0][0]
        ufiles = json.loads(ufiles)
        #添加新的id
        ufiles.append(latest_id)
        new_ufiles = json.dumps(ufiles)
        #更新ufiles
        update_uf_cmd = 'UPDATE USERS SET UFILES = "%s" WHERE UACCOUNT = "%s";'%(new_ufiles,belong)
        self.db_cursor.execute(update_uf_cmd)
        self.db.commit()
        #完成操作
        print('onefile completed!')
        return 0

print('ready to add files...')    
AddF = AddFile()
while(True):
    mode = int(input('input 1 to add one file, 2 to add n files, and 3 to quit.'))
    if mode == 1:
        filename = input('input filename:')
        while(filename.isspace() or filename==''):
            filename = input('input filename:')
        filepath = input('input filepath:')
        while(filepath.isspace() or filepath==''):
            filepath = input('input filepath:')
        belong = input('input owner:')
        while(belong.isspace() or belong==''):
            belong = input('input owner:')
        AddF.add_one_file(filename,filepath,belong)
    elif mode == 2:
        load_by_file = input('Do you want to add files using a config file (Y/n)? \nP.S. sample.config is a sample.')
        if load_by_file == 'y' or load_by_file == 'Y':
            filename = input('input config file name:')
            try:
                with open(filename,'r') as configfile:
                    lines = configfile.readlines()
                    for line in lines:
                        if line[0] == '#':
                            #comment
                            pass
                        elif line.isspace() or line=='':
                            #empty
                            pass
                        else:
                            filename,filepath,belong = line.split(' ')
                            if belong[-1] == '\n':
                                belong = belong[:-1]
                            print('"%s","%s","%s",'%(filename,filepath,belong))
                            AddF.add_one_file(filename,filepath,belong)
                    configfile.close()
            except:
                print('config file is invalid, please check it')
        else:
            n = int(input('how many files you want to add? '))
            for i in range(n):
                filename = input('input filename:')
                while(filename.isspace() or filename==''):
                    filename = input('input filename:')
                filepath = input('input filepath:')
                while(filepath.isspace() or filepath==''):
                    filepath = input('input filepath:')
                belong = input('input owner:')
                while(belong.isspace() or belong==''):
                    belong = input('input owner:')
            print('loaded %d files'%n)
            print('all completed!')
    else:
        print('Bye')
        break
