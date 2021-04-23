from django.shortcuts import render

# Create your views here.
from django.contrib.auth import logout
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect
from django.contrib import messages
from hashlib import sha256
from .models import *

import json

def encryp_file_info(fid,uid):
    return sha256(('fid=%duid=%d'%(fid,uid)).encode()).hexdigest()

def index(request):
    #可以通过request.user_agent.is_mobile判断是否为移动端访问，从而使用不同模板
    #取session
    userId = request.session.get('userId')
    if userId != None:
        user = Users.objects.get(id=userId)
        username = user.uname
        account = user.uaccount
        userInfo = 'username: '+str(username)+'account: '+str(account)
        hasLogin = True
    else:
        userInfo = "I don't know you, maybe you can sign up?"
        hasLogin = False
    #这样直接返回一段文字事实上更简单
    return render(request, 'onefile/index.html', {
        'userInfo': userInfo, 'hasLogin': hasLogin
    })


def index1(request):
    #根目录跳转
    return redirect('/onefile/index')


#注册

def register(request):  # 注册页面点击注册
    if request.method == 'POST':
        #若使用方法为post，则表示在传数据，进行验证
        account = request.POST.get('account')
        password = request.POST.get('password')
        name = request.POST.get('username')

        users = Users.objects.all()
        sameAccount = False
        try:
            Users.objects.get(uaccount=account)
            """这里已增加一个返回账号已存在的错误"""
            messages.info(request, 'this account has existed!')
            return redirect('/onefile/register')

        finally:
            try:
                #填写数据到用户信息数据库
                user = Users.createUser(account, password, name)
                user.save(using='default')
            except:
                messages.info(request, 'invalid input!')
                return redirect('/onefile/register')
            else:
                #注册成功之后直接跳转到文件界面
                request.session['userId'] = user.id
                return redirect('/onefile/files')
    else:
        #否则返回html页面
        return render(request, "onefile/register.html")
#登录


def login(request):
    if request.method == 'POST':
        #处理表单
        userAccount = request.POST.get('account')
        userPassword = request.POST.get('password')
        users = Users.objects.all()
        validInput = False
        try:
            user = Users.objects.get(uaccount=userAccount)
            if userPassword == user.upassword:
                validInput = True
                request.session['userId'] = user.id
        finally:
            if(validInput):
                return redirect('/onefile/files')
            else:
                messages.info(request, 'account and password donot match!')
                return redirect('/onefile/login')
    else:
        #返回页面
        return render(request, "onefile/login.html")

#文件页面


def files(request):
    userID = request.session.get('userId')
    if userID == None:
        return redirect('/onfile/index')
    else:
        user = Users.objects.get(id=userID)
        uFiles = json.loads(user.ufiles)
        print('current user: ',userID)
        print('his files:')
        print(uFiles)
        #ufiles格式为：[fid1,fid2]
        if len(uFiles) == 0:
            return render(request, 'onefile/files.html', {
                'empflag':True,'files': None})
        else:
            filenames = []
            filesizes = []
            fidencrys = []
            for fid in uFiles:
                fileobj = Files.objects.get(id=fid)
                filename = fileobj.filename
                filesize = fileobj.filesize
                int_filesize = int(filesize)
                if int_filesize < 1024:
                    filesize = str(int(int_filesize/1)) + 'B'
                elif int_filesize <1024**2:
                    filesize = str(int(int_filesize/1024)) + 'KB'
                elif int_filesize <1024**3:
                    filesize = str(int(int_filesize/1024**2)) + 'MB'
                else:
                    filesize = str(int(int_filesize/1024**3)) + 'GB'
                filenames.append(filename)
                filesizes.append(filesize)
                fidencry = encryp_file_info(fid,userID)
                fidencrys.append(fidencry)
            files = zip(filenames,filesizes,fidencrys)
            print('got these:')
            print(filenames,filesizes,fidencrys)
            return render(request, 'onefile/files.html', {
                'empflag':False,'files': files})


def upload(request):
    userID = request.session.get('userId')
    if userID == None:
        return redirect('/onfile/index')
    else:
        return redirect('/onefile/index')

def download(request):
    userID = request.session.get('userId')
    if userID == None:
        return redirect('/onfile/index')
    else:
        #获取此用户所拥有的所有文件
        user = Users.objects.get(id=userID)
        uFiles = json.loads(user.ufiles)
        files = {}
        for fid in uFiles:
            fileobj = Files.objects.get(id=fid)
            filepath = fileobj.filepath
            filename = fileobj.filename
            key = encryp_file_info(fid,userID)
            files[key] = {'path':filepath,'name':filename}
        file_demanded = request.GET['file']
        #若不存在此文件
        if file_demanded not in files.keys():
            messages.info(request, 'This file does not exist!')
            return redirect('/onefile/files')
        else:
            filepath = files[file_demanded]['path']
            try:
                file = open(filepath,'rb')
            except:
                messages.info(request, 'This file is not invalid!')
                return redirect('/onefile/files')
            response =FileResponse(file)
            response['Content-Type']='application/octet-stream'
            response['Content-Disposition']='attachment;filename="%s"'%files[file_demanded]['name']
            return response

def quit(request):
    #清除session
    logout(request)  # 方式1
    # request.session.clear()  #方式2
    # request.session.flush()  #方式3
    return redirect('/onefile/index')
