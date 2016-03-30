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
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin
from . import db, login_manager

class User(UserMixin,db.Model):                                           #对应数据库中的user表，user表存储用户个人信息
      id=db.Column(db.Integer,primary_key=True)
      classes=db.Column(db.String(80))
      student_number=db.Column(db.Integer)
      name=db.Column(db.String(80))
      password=db.Column(db.String(32))
      admin=db.Column(db.Boolean)
      onlineTime=db.Column(db.Integer)
      numofSubmit=db.Column(db.Integer)
      recentsubmitTime=db.Column(db.String(32))
      averageSpeed=db.Column(db.Integer)
      def __init__(self,classes,student_number,name,password,admin,onlineTime,numofSubmit,recentsubmitTime,averageSpeed):
          self.classes=classes
          self.student_number=student_number
          self.name=name
          self.password=password
          self.admin=admin
          self.onlineTime=onlineTime
          self.numofSubmit=numofSubmit
          self.recentsubmitTime=recentsubmitTime
          self.averageSpeed=averageSpeed
    

class Writing_article(db.Model):                                                #对应mysql中writing_article表，该表存储文章
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    rank=db.Column(db.Integer)
    content=db.Column(db.String(2040))
    def __init__(self,name,rank,content):
        self.name=name
        self.rank=rank
        self.content=content


class practice_result(db.Model):                                             #对应practice_result表，该表存储用户平时练习成绩
    id=db.Column(db.Integer,primary_key=True)
    classes=db.Column(db.String(80))
    student_number=db.Column(db.Integer)
    username=db.Column(db.String(50))
    articlename=db.Column(db.String(100))
    write_speed=db.Column(db.String(50))
    right_rate=db.Column(db.String(50))
    rank=db.Column(db.Integer)
    submitTime=db.Column(db.String(50))
    writenum=db.Column(db.Integer)
    level=db.Column(db.String(50))
    def __init__(self,classes,student_number,username,articlename,write_speed,right_rate,rank,submitTime,writenum,level):
        self.classes=classes
        self.student_number=student_number
        self.username=username
        self.articlename=articlename
        self.write_speed=write_speed
        self.right_rate=right_rate
        self.rank=rank
        self.submitTime=submitTime
        self.writenum=writenum
        self.level=level

class context_list(db.Model):                                           #对应context_list表，该表用于存储所有比赛（开始时间、结束时间、文章名字等）的信息
    id=db.Column(db.Integer,primary_key=True)
    contextname=db.Column(db.String(500))      
    start_time=db.Column(db.String(50))
    end_time=db.Column(db.String(50))
    def __init__(self,contextname,start_time,end_time):
        self.contextname=contextname
        self.start_time=start_time
        self.end_time=end_time
    
class context_result(db.Model):                                       #对应context_resutl表，该表用于存储比赛的结果
    id=db.Column(db.Integer,primary_key=True)
    classes=db.Column(db.String(80))
    student_number=db.Column(db.Integer)
    username=db.Column(db.String(50))
    contextId=db.Column(db.Integer)
    write_speed=db.Column(db.String(50))
    right_rate=db.Column(db.String(50))
    rank=db.Column(db.Integer)
    submitTime=db.Column(db.String(50))
    writenum=db.Column(db.Integer)
    articlename=db.Column(db.String(100))
    score=db.Column(db.Integer())
    level=db.Column(db.String(50))
    def __init__(self,classes,student_number,username,contextId,write_speed,right_rate,rank,submitTime,writenum,articlename,score,level):
        self.classes=classes
        self.student_number=student_number
        self.username=username
        self.contextId=contextId
        self.write_speed=write_speed
        self.right_rate=right_rate
        self.rank=rank
        self.submitTime=submitTime
        self.writenum=writenum
        self.articlename=articlename
        self.score=score
        self.level=level


class context_show(db.Model):                                     #对应context_show表，该表用于存储具体某个比赛的信息（比赛时长、比赛中的文章名字）                                     
    id=db.Column(db.Integer,primary_key=True)
    context_id=db.Column(db.Integer)
    articlename=db.Column(db.String(50))
    timelimit=db.Column(db.Integer)
    def __init__(self,context_id,articlename,timelimit):
        self.context_id=context_id
        self.articlename=articlename
        self.timelimit=timelimit


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
