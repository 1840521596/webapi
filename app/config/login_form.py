#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    accountNumber = StringField('accountNumber',
                                validators=[DataRequired('accountNumber is null')],
                                render_kw={'rows': 20,"autocomplete":"off",
                                           'placeholder': u'用户名'})
    password = PasswordField('password', validators=[DataRequired('password is null')],
                             render_kw={'rows': 20, "autocomplete": "off",
                                        'placeholder': u'密码'})