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
from flask.ext.moment import Moment
from werkzeug.security import generate_password_hash, check_password_hash
#from . import login_manager
from datetime import datetime
#import MySQLdb
import sys
from flask.ext.mail import Mail
#from flask.ext.mysql import MySQL
reload(sys)
sys.setdefaultencoding('utf8')
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class NameForm(Form):
      name=StringField('用户名：',validators=[Required()])
      password=PasswordField('密码：',validators=[Required()])
      submit=SubmitField('提交')

class RegisterForm(Form):
      year=SelectField('年级：',choices=[('2013','2013'),('2014','2014'),('2015','2015'),('2016','2016')])
      major=SelectField('专业：',choices=[('计算机科学与技术','计算机科学与技术'),('软件工程','软件工程'),('通信工程','通信工程')])
      grade=SelectField('班号：',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')])
      student_number=IntegerField('学号：',validators=[Required()])
      name=StringField('用户名：',validators=[Required()])
      password=PasswordField('密码：',validators=[Required()])
      submit=SubmitField('提交')


class  LoginForm(Form):
      name=StringField("用户名",validators=[Required()])
      password=PasswordField("密码",validators=[Required()])
      submit=SubmitField('登录')


class addarticleForm(Form):                                   #添加文章的表单
      articlename=StringField('文章名字',validators=[Required()])
      rank=StringField('文章等级',validators=[Required()])
      content=TextAreaField('内容：',validators=[Required()])
      submit=SubmitField('提交')


class Result_Form(Form):                                    #获取用户练习成绩的表单
      username=HiddenField()
      articlename=HiddenField()
      speed=HiddenField()
      rightrate=HiddenField()
      rank=HiddenField()
      submitTime=HiddenField()
      writenum=HiddenField()
      timeduring=HiddenField()
      submit=SubmitField('提交')

class ModifyPwdForm(Form):                            #该表格用于admin修改用户密码
      username=StringField('用户名',validators=[Required()])
      student_number=IntegerField('学号',validators=[Required()])
      newpassword=PasswordField('新密码',validators=[Required()])
      confirmpassword=PasswordField('再次输入密码：',validators=[Required()])
      submit=SubmitField('提交')


class ChangePersonalPwd(Form):                                  #用户自己修改密码的表单
      oldpassword=PasswordField('旧密码：',validators=[Required()])
      newpassword=PasswordField('新密码：',validators=[Required()])
      confirmpassword=PasswordField('再次输入新密码：',validators=[Required()])
      submit=SubmitField('提交')

    
class contextresult_Form(Form):                                    #提交用户比赛成绩的表单
      username=HiddenField()
      articlename=HiddenField()
      speed=HiddenField()
      rightrate=HiddenField()
      rank=HiddenField()
      submitTime=HiddenField()
      writenum=HiddenField()
      score=HiddenField()
      submit=SubmitField('提交')

class AddContextForm(Form):
      context_id=IntegerField('比赛ID',validators=[Required()])
      contextname=StringField('比赛名字：',validators=[Required()])
      timelimit=IntegerField('比赛时长：',validators=[Required()])
      start_time=HiddenField()
      end_time=HiddenField()
      articlename=HiddenField()
      submit=SubmitField('提交')
