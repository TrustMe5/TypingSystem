# coding=utf-8
import re
from flask import Flask,render_template,session,redirect,url_for,flash,json,jsonify
from wtforms import Form, BooleanField,TextAreaField, IntegerField,TextField,HiddenField, PasswordField, validators,ValidationError,SelectField
from flask.ext.wtf import Form
from flask.ext.login import logout_user,login_required
from flask.ext.sqlalchemy import * 
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask import request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import sys
from flask.ext.mail import Mail
reload(sys)
sys.setdefaultencoding('utf8')
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from .. import db
from ..models import User,Writing_article,practice_result,context_list,context_result,context_show
from .forms import LoginForm, RegisterForm,NameForm,addarticleForm,Result_Form,ModifyPwdForm,ChangePersonalPwd,contextresult_Form,AddContextForm

@auth.route('/articlelist/<articlename>',methods=['GET','POST'])
def showcontent(articlename):                                               #用户练习界面
    result=db.session.query(Writing_article).filter_by(name=articlename).first()
    articlecontent=result.content
    articlecontent=articlecontent.split(" ")
    content=[]
    length=len(articlecontent)
    for i in range(0,length,15):                                   # 每行显示15个单词
        content.append(" ".join(articlecontent[i:i+15]))
    name=result.name
    rank=result.rank
    result_form=Result_Form()
    if result_form.validate_on_submit():
        student_number=User.query.filter_by(name=result_form.username.data).first().student_number
        classes=User.query.filter_by(name=result_form.username.data).first().classes
        typingSpeed=result_form.speed.data[0:len(result_form.speed.data)-3]            # typingSpeed为打字速度
        typingSpeed=int(float(typingSpeed))
        if typingSpeed>=200:
            level='优秀，成绩不错哦！'
        elif typingSpeed>=100 and typingSpeed<200:
            level='良好，向更快挑战！'
        else:
            level='不及格，加强训练！'
        inset=practice_result(username=result_form.username.data, articlename=result_form.articlename.data, write_speed=result_form.speed.data,right_rate=result_form.rightrate.data,rank=result_form.rank.data,submitTime=result_form.submitTime.data,writenum=result_form.writenum.data,classes=classes,student_number=student_number,level=level)
        db.session.add(inset)
        db.session.commit()
        whichuser=User.query.filter_by(name=result_form.username.data).first()             #每次练习结束后都会更新User表内的个人平时练习成绩
        whichuser.onlineTime=whichuser.onlineTime+long(result_form.timeduring.data)
        whichuser.numofSubmit=(whichuser.numofSubmit)+1
        speeddata=result_form.speed.data
        whichuser.averageSpeed=(whichuser.averageSpeed+int(float(speeddata[0:len(speeddata)-3])))/2
        whichuser.recentsubmitTime=result_form.submitTime.data
        db.session.commit()
        return redirect('/auth/practiceresultlist')
    return render_template('showcontent.html',name=name,rank=rank,content=content,result_form=result_form,writer=session.get('name'))



@auth.route('/contextcontentshow/<articlename>',methods=['GET','POST'])
def contextcontentshow(articlename):                                        #比赛界面
    result=db.session.query(Writing_article).filter_by(name=articlename).first()
    articlecontent=result.content
    articlecontent=articlecontent.split(" ")
    content=[]
    length=len(articlecontent)
    for i in range(0,length,15):
        content.append(" ".join(articlecontent[i:i+15]))
    name=result.name
    rank=result.rank
    result_form=contextresult_Form()
    if result_form.validate_on_submit():
        ThisContextEndTime=context_list.query.filter_by(id=session.get('context_id')).first().end_time
        checkuser=context_result.query.filter(context_result.contextId==session.get('context_id'),context_result.username==result_form.username.data).first()
        if checkuser:
            redirect('/contextlist')
            flash('您已经参加过此次比赛，成绩将不会被记录')
        elif int(filter(str.isalnum,str(ThisContextEndTime)))<int(filter(str.isalnum,str(result_form.submitTime.data))):
            redirect('/contextlist')
            flash('该比赛已经结束！')
        else:
            student_number=User.query.filter_by(name=result_form.username.data).first().student_number
            classes=User.query.filter_by(name=result_form.username.data).first().classes
            typingSpeed=int(result_form.score.data)/int(session.get('timelimit'))               # typingSpeed为每分钟打对的字母的个数
            if typingSpeed>=200:
                level='优秀，成绩不错哦！'
            elif typingSpeed>=100 and typingSpeed<200:
                level='良好，向更快挑战！'
            else:
                level='不及格，加强训练！'
            inset=context_result(username=result_form.username.data,contextId=session.get('context_id'), write_speed=result_form.speed.data,right_rate=result_form.rightrate.data,rank=result_form.rank.data,submitTime=result_form.submitTime.data,writenum=result_form.writenum.data,articlename=result_form.articlename.data,score=result_form.score.data,classes=classes,student_number=student_number,level=level)
            db.session.add(inset)
            db.session.commit()
            context_id=session.get('context_id')
            return redirect('/auth/contextresultshow/context_id='+context_id)
    return render_template('contextcontentshow.html',name=name,rank=rank,content=content,result_form=result_form,timelimit=session.get('timelimit'),writer=session.get('name'))
    

@auth.route('/articlelist',methods=['GET'])
def articlelist():                              #练习文章列表界面
    totalarticlelistpage=len(Writing_article.query.filter(Writing_article.id!=0).all())/50+1
    pagecontent=Writing_article.query.filter(Writing_article.id>0,Writing_article.id<50).all()
    name=session.get('name')
    return render_template('articlelist.html',totalpagenum=totalarticlelistpage,result=pagecontent,writer=name)


@auth.route('/articlelist/page=<page_num>',methods=['GET'])
def articlelistonpage(page_num):                   #练习文章分页显示
    totalarticlelistpage=len(Writing_article.query.filter(Writing_article.id!=0).all())/50+1
    pagecontent=Writing_article.query.filter(Writing_article.id>=(int(page_num)-1)*50,Writing_article.id<(int(page_num)*50)).all()
    writer=session.get('name')
    return render_template('articlelist.html',totalpagenum=totalarticlelistpage,result=pagecontent,writer=writer)



@auth.route('/practiceresultlist',methods=['GET'])
def practiceresultlist():                        #显示用户练习成绩（首页）
    totalpracticeresultpage=len(practice_result.query.filter(practice_result.id!=0).all())/50+1
    practicenum=len(practice_result.query.filter(practice_result.id!=0).all())
    pagecontent=practice_result.query.filter(practice_result.id<=practicenum,practice_result.id>practicenum-50).all()
    pagecontent=sorted(pagecontent, key=lambda practice: practice.id,reverse=True) 
    return render_template('practiceresultlist.html',result=pagecontent,currentpagenum=1,totalpagenum=totalpracticeresultpage,writer=session.get('name'))


@auth.route('/practiceresultlist/page=<page_num>',methods=['GET'])
def practiceresultlistonpage(page_num):                                    #分页显示用户练习成绩
    totalpracticeresultpage=len(practice_result.query.filter(practice_result.id!=0).all())/50+1
    practicenum=len(practice_result.query.filter(practice_result.id!=0).all())
    pagecontent=practice_result.query.filter(practice_result.id<=practicenum-(int(page_num)-1)*50,practice_result.id>practicenum-int(page_num)*50).all()
    pagecontent=sorted(pagecontent, key=lambda practice: practice.id,reverse=True) 
    return render_template('practiceresultlist.html',result=pagecontent,currentpagenum=page_num,totalpagenum=totalpracticeresultpage,writer=session.get('name'))


@auth.route('/dailypracticeranklist/page=<page_num>',methods=['GET'])               #用户日常练习情况排名
def dailypracticeranklist(page_num):
    pagecontent=User.query.filter(User.admin!=1).all()
    classlist=[]
    for i in range(len(pagecontent)):
        classlist.append(pagecontent[i].classes)
    allclasslist=set(classlist)
    totalpagenum=len(pagecontent)/50+1
    pagecontent=sorted(pagecontent,key=lambda user:(user.onlineTime,user.averageSpeed),reverse=True)
    onepagecontent=pagecontent[(int(page_num)-1)*50:int(page_num)*50]
    return render_template('dailypracticeranklist.html',currentpagenum=page_num,totalpagenum=totalpagenum,onepagecontent=onepagecontent,allclasslist=allclasslist,writer=session.get('name'))


@auth.route('/dailypracticeresultshowByclass/class=<classname>',methods=['GET'])             #显示某个班级的练习情况
def dailypracticeresultshowByclass(classname):
    pagecontent=User.query.filter_by(classes=classname).all()
    pagecontent=sorted(pagecontent,key=lambda user:(user.onlineTime,user.averageSpeed),reverse=True)
    return render_template('dailypracticeresultshowByclass.html',classname=classname,pagecontent=pagecontent,writer=session.get('name'))


@auth.route('/contextlist',methods=['GET'])
def contextlist():                                #所有比赛列表界面（首页）
    totalcontextlistpage=len(context_list.query.filter(context_list.id!=0).all())/50+1
    contextnum=len(context_list.query.filter(context_list.id!=0).all())
    pagecontent=context_list.query.filter(context_list.id<=contextnum,context_list.id>contextnum-50).all()
    pagecontent=sorted(pagecontent, key=lambda context: context.id,reverse=True) 
    return render_template('contextlist.html',result=pagecontent,totalpagenum=totalcontextlistpage,writer=session.get('name'))


@auth.route('/contextlist/page=<page_num>',methods=['GET'])
def contextlistonpage(page_num):                     # 分页显示所有比赛
    totalcontextlistpage=len(context_list.query.filter(context_list.id!=0).all())/50+1
    contextnum=len(context_list.query.filter(context_list.id!=0).all())
    pagecontent=context_list.query.filter(context_list.id<=contextnum-(int(page_num)-1)*50,context_list.id>contextnum-(int(page_num)*50)).all()
    pagecontent=sorted(pagecontent, key=lambda context: context.id,reverse=True) 
    return render_template('contextlist.html',result=pagecontent,totalpagenum=totalcontextlistpage,writer=session.get('name'))
    


@auth.route('/context_show/context_id=<contextId>',methods=['GET'])
def show_context(contextId):                              #显示具体某个比赛的信息
    result=context_show.query.filter_by(context_id=contextId).all()
    contextname=context_list.query.filter_by(id=contextId).first().contextname
    session['context_id']=contextId
    session['timelimit']=result[0].timelimit
    writer=session.get('name')
    return render_template('context_show.html',result=result,contextname=contextname,context_id=session.get('context_id'),writer=writer)



@auth.route('/contextresultshow/context_id=<contextId>',methods=['GET','POST'])
def contextresult_show(contextId):                       #显示某个比赛的成绩
    result=context_result.query.filter_by(contextId=contextId).all()
    result=sorted(result, key=lambda student: student.score,reverse=True) 
    contextname=context_list.query.filter_by(id=contextId).first().contextname
    return render_template('contextresultshow.html',result=result,contextname=contextname,context_id=contextId,writer=session.get('name'))



@auth.route('/admin',methods=['GET','POST'])
def admin():                                          #管理员登陆界面
    loginform=LoginForm()
    if loginform.validate_on_submit():
        user=User.query.filter_by(name=loginform.name.data).first()
        if user is not None and check_password_hash(user.password,loginform.password.data) and user.admin:
            session['admin']='admin'
            session['name']='admin'
            isadmin=session.get('admin')
            return redirect('/auth/adminhome')
        else:
            flash("用户名或者密码错误！")
            return redirect('/auth/admin')
    return render_template('admin.html',loginform=loginform)

@auth.route('/addarticle',methods=['GET','POST'])
def addarticle():                                  #管理员添加文章界面
    addarticleform=addarticleForm()
    if addarticleform.validate_on_submit():
        inset=Writing_article(name=addarticleform.articlename.data,rank=addarticleform.rank.data,content=addarticleform.content.data)
        db.session.add(inset)
        db.session.commit()
        flash('添加成功！')
        return redirect('/auth/addarticle')
    return render_template('addarticle.html',addarticleform=addarticleform,isadmin=session.get('admin'))


@auth.route('/addcontext',methods=['GET','POST'])
def addcontext():                                 #管理员添加比赛界面
    addcontextform=AddContextForm()
    result=Writing_article.query.filter(Writing_article.id!=0).all()
    numcontext=context_list.query.filter(context_list.id!=0).all()
    if addcontextform.validate_on_submit():
        inserttocontext_list=context_list(contextname=addcontextform.contextname.data,start_time=addcontextform.start_time.data,end_time=addcontextform.end_time.data)
        db.session.add(inserttocontext_list)
        db.session.commit()
        inserttocontext_show=context_show(context_id=addcontextform.context_id.data,articlename=addcontextform.articlename.data,timelimit=addcontextform.timelimit.data)
        db.session.add(inserttocontext_show)
        db.session.commit()
        flash('添加比赛成功！')
        return redirect('/auth/addcontext')
    return render_template('addcontext.html',result=result,context_id=len(numcontext)+1,addcontextform=addcontextform,isadmin=session.get('admin'))


@auth.route('/adminhome',methods=['GET','POST'])
def adminhome():                               #管理员主页界面
    isadmin=session.get('admin')
    modifypwdform=ModifyPwdForm()
    if modifypwdform.validate_on_submit():
        user=User.query.filter_by(name=modifypwdform.username.data,student_number=modifypwdform.student_number.data).first()
        if user is None:
            flash('查不到该用户！请核实用户名和学号！')
        elif modifypwdform.newpassword.data!=modifypwdform.confirmpassword.data:
            flash('两次输入密码不相同！')
        else:
            user.password=generate_password_hash(modifypwdform.newpassword.data)
            db.session.commit()
            flash('修改密码成功！')
    return render_template('adminhome.html',isadmin=isadmin,modifypwdform=modifypwdform)


@auth.route('/',methods=['GET','POST'])
@auth.route('/index',methods=['GET','POST'])
def index():                            #打字系统首页
    return render_template('index.html',writer=session.get('name')) 


@auth.route('/register',methods=['GET','POST'])
def register():                     #用户注册界面
    registerform=RegisterForm()
    if registerform.validate_on_submit():
        if User.query.filter_by(name=registerform.name.data).first():
            flash("The username %s is already exist !"%registerform.name.data)
            return redirect(url_for('register'))
        elif User.query.filter_by(student_number=registerform.student_number.data).first():
            flash("The student_number is already exist !")
            return redirect(url_for('register'))
        else:
            inset=User(classes=registerform.year.data+registerform.major.data+registerform.grade.data+"班",student_number=registerform.student_number.data,name=registerform.name.data,password=generate_password_hash(registerform.password.data),admin=0,onlineTime=0,numofSubmit=0,recentsubmitTime='Never Submittied',averageSpeed=0)
            db.session.add(inset)                         #注册时通过generate_password_hash方法把密码hash下再存入数据库
            db.session.commit()
            flash('注册成功！请登录')
            return redirect('/auth/login')
    return render_template('register.html',register=registerform)



@auth.route('/login',methods=['GET','POST'])
def login():                               #用户登陆界面
    loginform=LoginForm()
    if loginform.validate_on_submit():
        if session.get('admin') is not None:                  #如果之前admin登录过，现在用户登录时要清除session['admin']
            session['admin']=None
        user=User.query.filter_by(name=loginform.name.data).first()
        if user is not None and check_password_hash(user.password,loginform.password.data):
           session['name']=loginform.name.data
           flash("welcome! %s"%session.get('name'))
           session['password']=loginform.password.data
           login_user(user)
           return redirect('/auth/index')
        flash('用户名或密码错误！')
        return redirect('/auth/login')
    return render_template('login.html',loginform=loginform)


@auth.route('/modifypwd/user=<username>',methods=['GET','POST'])
def modifypwd(username):                                             #用户更改密码界面
    if username!=session.get('name'):             #防止用户直接在地址栏里输入，去改别人的密码
        return redirect('/auth')
    else:
        form=ChangePersonalPwd()
        user=User.query.filter_by(name=username).first()
        if form.validate_on_submit():
           if user is not None and check_password_hash(user.password,form.oldpassword.data):
               if form.newpassword.data!=form.confirmpassword.data:
                  flash('两次输入密码不一致！')
               else:
                  user.password=generate_password_hash(form.newpassword.data)
                  db.session.commit()
                  flash('改密成功！')
                  return redirect('/auth')
           else:
               flash('旧密码输入错误！请核对后修改')
    return render_template('modifypwd.html',form=form,writer=session.get('name'))

@auth.route('/homepage/user=<username>',methods=['GET','POST'])
def homepage(username):                                         #个人信息界面
    result=User.query.filter_by(name=username).first()
    dailypractice=practice_result.query.filter_by(username=username).all()
    return render_template('homepage.html',result=result,dailypractice=dailypractice,writer=session.get('name'))

@auth.route('/logout')
def logout():
    session['name']=None
    session['password']=None
    session['admin']=None
    logout_user()
    return redirect('/auth')




