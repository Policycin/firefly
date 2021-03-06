from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, FileField
from flask_wtf import FlaskForm
from wtforms.validators import Required, Length, Email, DataRequired, ValidationError
from pymongo import MongoClient
from ..models import verify_password
from app import app
from config import DevelopmentConfig

condev=DevelopmentConfig()
mongoIP=condev.MONGOIP
mongoPort=condev.MONGOPORT
db=MongoClient(mongoIP,port=mongoPort)
db = db.FireFly

class LoginForm(FlaskForm):
    account = StringField(
        label='账号',
        validators=[
            DataRequired("请输入账号")
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号！',
            'required': 'required'
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'required': 'required'
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat',

        }
    )
    remember_me = BooleanField('保持登录')

    def validate_account(self, filed):
        account = filed.data
        admin = db.Admin.find_one({'username': account})
        if not admin:
            raise ValidationError("账号不存在")


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired("请输入旧密码")
        ],
        description="旧密码",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入旧密码',
            'required': 'required'
        }
    )
    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired("请输入新密码")
        ],
        description="新密码",
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入新密码',
            'required': 'required'
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',
        }
    )

    def validate_old_pwd(self, field):
        pwd = field.data
        from flask import session
        name = session['admin']
        admin = db.Admin.find_one({'username': name})
        if not verify_password(admin.get('password'), pwd):
            raise ValidationError("旧密码错误")


class TagForm(FlaskForm):
    name = StringField(
        label='标签名称',
        validators=[
            DataRequired("请输入标签名称")
        ],
        description="标签名称",
        render_kw={
            'class': "form-control",
            'id': 'input_name',
            'placeholder': '请输入标签名称！'
        }

    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',

        }
    )


class SoureFileForm(FlaskForm):
    indexNum = StringField(
        label='索引号',
        validators=[
            DataRequired('请输入索引号')
        ],
        description='索引号',
        render_kw={
            'class': "form-control", 'placeholder': "请输入索引号！"
        }
    )
    fileType = StringField(
        label='主题分类',
        validators=[
            DataRequired('请输入主题分类')
        ],
        description='主题分类',
        render_kw={
            'class': "form-control", 'placeholder': "请输入主题分类！"
        }
    )
    publisher = StringField(
        label='发布机构',
        validators=[
            DataRequired('请输入发布机构')
        ],
        description='发布机构',
        render_kw={
            'class': "form-control", 'placeholder': "请输入发布机构！"
        }
    )
    createTime = StringField(
        label='生成时间',
        validators=[
            DataRequired('请选择生成时间')
        ],
        description='生成时间',
        render_kw={
            'class': "form-control", 'placeholder': "请选择生成时间！", "id": "input_release_time"
        }
    )
    title = StringField(
        label='标题',
        validators=[
            DataRequired('请输入标题')
        ],
        description='标题',
        render_kw={
            'class': "form-control", 'placeholder': "请输入标题！"
        }
    )
    fileNo = StringField(
        label='发文字号',
        validators=[
            DataRequired('请输入发文字号')
        ],
        description='发文字号',
        render_kw={
            'class': "form-control", 'placeholder': "请输入发文字号！"
        }
    )
    publishDate = StringField(
        label='发布时间',
        validators=[
            DataRequired('请选择发布时间')
        ],
        description='发布时间',
        render_kw={
            'class': "form-control", 'placeholder': "请选择发布时间！", "id": "input_release_time2"
        }
    )
    addtime = StringField(
        label='添加时间',
        validators=[
            DataRequired('请选择添加时间')
        ],
        description='添加时间',
        render_kw={
            'class': "form-control", 'placeholder': "请选择添加时间！", "id": "input_release_time3"
        }
    )
    tags = db.Tag.find().sort("_id", -1)
    tagc = []
    for v in range(tags.count()):
        tagc.append((tags[v].get("name"), tags[v].get("name")))
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired('请选择标签')
        ],
        description='标签',
        coerce=str,
        choices=tagc,
        render_kw={
            "class": "form-control", "placeholder": "请选择标签分类"
        }
    )
    # path = FileField(
    #     label="本地文件",
    #     validators=[
    #         DataRequired('上传文件')
    #     ],
    #     description="本地文件"
    # )
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired('请输入内容')
        ],
        description='内容',
        render_kw={
            'class': "form-control", 'rows': "10", 'id': "input_info"
        }
    )
    url = StringField(
        label='原文链接',
        validators=[
            DataRequired('请输入原文链接')
        ],
        description='原文链接',
        render_kw={
            'class': "form-control", 'placeholder': "请输入原文链接！"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',

        }
    )


class CmpFileForm(FlaskForm):
    indexNum = StringField(
        label='索引号',
        validators=[
            DataRequired('请输入索引号！')
        ],
        description='索引号',
        render_kw={
            'class': "form-control", 'placeholder': "请输入索引号！"
        }
    )
    classfication = StringField(
        label='主题分类',
        validators=[
            DataRequired('请输入主题分类！')
        ],
        description='主题分类',
        render_kw={
            'class': "form-control", 'placeholder': "请输入主题分类！"
        }
    )
    publisher = StringField(
        label='发布机构',
        validators=[
            DataRequired('请输入发布机构！')
        ],
        description='发布机构',
        render_kw={
            'class': "form-control", 'placeholder': "请输入发布机构！"
        }
    )
    fileCreateTime = StringField(
        label='生成时间',
        validators=[
            DataRequired('请选择生成时间！')
        ],
        description='生成时间',
        render_kw={
            'class': "form-control", 'placeholder': "请选择生成时间！", "id": "input_release_time"
        }
    )
    fileName = StringField(
        label='标题',
        validators=[
            DataRequired('请输入标题！')
        ],
        description='标题',
        render_kw={
            'class': "form-control", 'placeholder': "请输入标题！"
        }
    )
    fileNo = StringField(
        label='发文字号',
        validators=[
            DataRequired('请输入发文字号！')
        ],
        description='发文字号',
        render_kw={
            'class': "form-control", 'placeholder': "请输入发文字号！"
        }
    )
    publishDate = StringField(
        label='发布日期',
        validators=[
            DataRequired('请选择发布日期！')
        ],
        description='发布日期',
        render_kw={
            'class': "form-control", 'placeholder': "请选择发布日期！", "id": "input_release_time2"
        }
    )
    addtime = StringField(
        label='添加时间',
        validators=[
            DataRequired('请选择添加时间！')
        ],
        description='添加时间',
        render_kw={
            'class': "form-control", 'placeholder': "请选择添加时间！", "id": "input_release_time3"
        }
    )
    tags = db.Tag.find().sort("_id", -1)
    tagc = []
    for v in range(tags.count()):
        tagc.append((tags[v].get("name"), tags[v].get("name")))
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired('请选择标签！')
        ],
        description='标签',
        coerce=str,
        choices=tagc,
        render_kw={
            "class": "form-control", "placeholder": "请选择标签分类！"
        }
    )
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired('请输入正文！')
        ],
        description='内容',
        render_kw={
            'class': "form-control", 'rows': "10", 'id': "input_info"
        }
    )
    fileWebsiteUrl = StringField(
        label='原文链接',
        validators=[
            DataRequired('请输入原文链接！')
        ],
        description='原文链接',
        render_kw={
            'class': "form-control", 'placeholder': "请输入原文链接！"
        }
    )
    abolitionDate=StringField(
        label='废止日期',
        validators=[
            DataRequired("请选择废止日期！")
        ],
        description='废止日期',
        render_kw={
            'class': "form-control", 'placeholder': "请选择添加时间！", "id": "input_release_time4"
        }
    )
    fileLocalUrl=StringField(
        label='本地路径',
        validators=[
            DataRequired("请输入本地路径！")
        ],
        description='本地路径',
        render_kw={
            'class': "form-control", 'placeholder': "请输入本地路径！"
        }
    )
    fromDate=StringField(
        label='生效日期',
        validators=[
            DataRequired("请选择生效日期！")
        ],
        description='生效日期',
        render_kw={
            'class': "form-control", 'placeholder': "请选择添加时间！", "id": "input_release_time5"
        }
    )
    keyword=StringField(
        label='关键词',
        validators=[
            DataRequired("请输入关键词！")
        ],
        description='关键词',
        render_kw={
            'class': "form-control", 'placeholder': "请输入关键词！"
        }
    )
    publisherCityName=StringField(
        label='城市名称',
        validators=[
            DataRequired("请输入城市名称！")
        ],
        description='城市名称',
        render_kw={
            'class': "form-control", 'placeholder': "请输入城市名称！"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',

        }
    )


class NoticeForm(FlaskForm):
    content = StringField(
        label='公告',
        validators=[
            DataRequired("请输入公告信息")
        ],
        description="公告",
        render_kw={
            'class': "form-control",
            'id': 'input_name',
            'placeholder': '请输入公告信息！'
        }

    )
    cho=[('是','是'),('否','否')]
    activation = SelectField(
        label="是否生效",
        validators=[
            DataRequired('请选择是否生效')
        ],
        description='是否生效',
        coerce=str,
        choices=cho,
        render_kw={
            "class": "form-control", "placeholder": "请选择标签分类"
        }
    )
    # addtime = StringField(
    #     label='添加时间',
    #     validators=[
    #         DataRequired('请选择添加时间')
    #     ],
    #     description='添加时间',
    #     render_kw={
    #         'class': "form-control", 'placeholder': "请选择添加时间！", "id": "input_release_time3"
    #     }
    # )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',

        }
    )
sourefile=[("请选择国发文号","请选择国发文号")]
sourefilelist=db.SoureFile.find({})
for v in sourefilelist:
    sourefile.append((v['fileNo'],v['fileNo']))
class CalForm(FlaskForm):
    # soureFilename=StringField()
    # soureFileNo=SelectField(
    #     label="国发文号",
    #     validators=[
    #         DataRequired('请选择国发文号！')
    #     ],
    #     description='国发文号',
    #     coerce=str,
    #     choices=sourefile,
    #     render_kw={
    #         "class": "form-control", "placeholder": "请选择国发文号！"
    #     }
    #
    # )
    cmpfilename=StringField(
        label='文件标题',
        validators=[
            DataRequired("111")
        ],
        description='文件标题',
        render_kw={
            'class': "form-control", 'placeholder': "请输入标题！"
        }
    )
    # cmpfileNo=StringField(
    #     label='发文文号',
    #     validators=[
    #         DataRequired("222")
    #     ],
    #     description='发文文号',
    #     render_kw={
    #         'class': "form-control", 'placeholder': "请输入发文文号！"
    #     }
    # )
    # publisherCityName=StringField(
    #     label='城市名称',
    #     validators=[
    #         DataRequired("333")
    #     ],
    #     description='城市名称',
    #     render_kw={
    #         'class': "form-control", 'placeholder': "请输入城市名称！"
    #     }
    # )
    # publishtime1=StringField(
    #     label='开始日期',
    #     validators=[
    #         DataRequired("444")
    #     ],
    #     description='开始日期',
    #     render_kw={
    #         'class': "form-control", 'placeholder': "请选择开始日期！", "id": "input_release_time1"
    #     }
    # )
    # publishtime2=StringField(
    #     label='结束日期',
    #     validators=[
    #         DataRequired("555")
    #     ],
    #     description='结束日期',
    #     render_kw={
    #         'class': "form-control", 'placeholder': "请选择结束时间！", "id": "input_release_time2"
    #     }
    # )
    submit = SubmitField(
        '下一步',
        render_kw={
            'class': 'btn btn-primary',
        }
    )
    # reset = SubmitField(
    #     '重置',
    #     render_kw={
    #         'class': 'btn btn-primary',
    #         'type':'reset'
    #     }
    # )

