from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from .forms import LoginForm, TagForm, PwdForm,SoureFileForm , CmpFileForm,NoticeForm
from pymongo import MongoClient, DESCENDING
from ..models import verify_password
from flask_login import login_user, logout_user, login_required, current_user
import os, datetime, uuid
from urllib.parse import urlencode, quote, unquote
from bson.objectid import ObjectId
from functools import wraps


db = MongoClient('127.0.0.1', port=27017)
db = db.FireFly

@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data
# 登陆装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = db.Admin.find_one({"username": data['account']})
        print(admin)
        if admin is not None and verify_password(admin.get('password'), data['pwd']):
            session['admin'] = data['account']
            return redirect(url_for('admin.index'))
        elif not verify_password(admin.get('password'), data['pwd']):
            flash("密码错误!", 'err')
            return redirect(url_for('admin.login'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
def logout():
    session.pop('admin', None)
    # session.pop('admin_id', None)
    session.clear()
    return redirect(url_for('admin.login'))


@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = db.Admin.find_one({'username': session['admin']})
        from werkzeug.security import generate_password_hash
        newadmin = admin
        newpwd = generate_password_hash(data['new_pwd'])
        db.Admin.update(admin, {'$set': {'password': newpwd}})
        flash("密码修改成功", 'ok')
        redirect(request.args.get('next') or url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)

#标签管理
@admin.route('/tag/add/', methods=["GET", "POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = db.Tag.find_one({'name': data['name']})
        if tag:
            flash("该标签已存在", 'err')
            return redirect(url_for('admin.tag_add'))
        tag = {
            'name': data['name'].replace(" ","").strip(),
            'addtime': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.Tag.insert(tag)
        flash("添加成功", 'ok')

        # tag = db.Tag.find().sort('_id', -1)
        # count = tag.count()
        # paper_obj = Pagination(request.args.get("page", 1), count, request.path, request.args, per_page_count=10)
        # html = paper_obj.page_html()
        # param = []
        # for v in range(count):
        #     param.append([tag[v].get("_id"), tag[v].get("name"), tag[v].get("addtime")])
        # index_list = param[paper_obj.start:paper_obj.end]
        return redirect(url_for('admin.tag_list', page=1))
    return render_template("admin/tag_add.html", form=form)


@admin.route('/tag/list/<int:page>', methods=["GET"])
@admin_login_req
def tag_list(page=None):
    if page == None:
        page = 1
    # 跳转列表页
    tag = db.Tag.find().sort('_id', -1)
    count = tag.count()
    paper_obj = Pagination(request.args.get("page", page), count, request.path, request.args, per_page_count=10)
    html = paper_obj.page_html()
    param = []
    for v in range(count):
        param.append([v + 1, tag[v].get("_id"), tag[v].get("name"), tag[v].get("addtime")])
    index_list = param[paper_obj.start:paper_obj.end]
    return render_template("admin/tag_list.html", index_list=index_list, html=html)


@admin.route('/tag/del/<id>/', methods=["GET"])
@admin_login_req
def tag_del(id=None):
    db.Tag.remove({'_id': ObjectId(id)})
    flash("标签删除成功", 'ok')
    # 跳转列表页
    # tag = db.Tag.find().sort('_id', -1)
    # count = tag.count()
    # paper_obj = Pagination(request.args.get("page", 1), count, request.path, request.args, per_page_count=10)
    # html = paper_obj.page_html()
    # param = []
    # for v in range(count):
    #     param.append([tag[v].get("_id"), tag[v].get("name"), tag[v].get("addtime")])
    # index_list = param[paper_obj.start:paper_obj.end]
    return redirect(url_for('admin.tag_list',page=1))


@admin.route('/tag/edit/<id>/', methods=["GET", "POST"])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = db.Tag.find_one({'_id': ObjectId(id)})
    if form.validate_on_submit():
        data = form.data
        # tag_count = Tag.query.filter_by(name=data['name']).count()
        tag_count = db.Tag.find_one({'name': data['name']})
        if tag_count and tag['name'] != data['name']:
            flash("该标签已存在", 'err')
            return redirect(url_for('admin.tag_edit', id=id))
        newtag = data['name']
        db.Tag.update(tag, {'$set': {'name': newtag}})
        flash("更新成功", 'ok')
        return redirect(url_for('admin.tag_edit', id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)

#源文件管理
@admin.route('/sourefile/add/',methods=['GET','POST'])
def sourefile_add():
    form=SoureFileForm()
    if form.validate_on_submit():
        data=form.data
        sourefile = db.SoureFile.find_one({'title': data['title']} or {'indexNum':data['indexNum']}
                                          or {'fileNo':data['fileNo']})
        if sourefile:
            flash("该源文件已存在", 'err')
            return redirect(url_for('admin.sourefile_add'))
        sourefile={
            'indexNum':data['indexNum'].replace(" ","").strip(),
            'fileType':data['fileType'].replace(" ","").strip(),
            'publisher':data['publisher'].replace(" ","").strip(),
            'createTime':data['createTime'].replace(" ","").strip(),
            'title':data['title'].replace(" ","").strip(),
            'fileNo':data['fileNo'].replace(" ","").strip(),
            'publishDate':data['publishDate'].replace(" ","").strip(),
            'addtime':datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            # 'path':r"\\",
            'content':data['content'].replace(" ","").strip(),
            'tag':data['tag_id'].replace(" ","").strip(),
            'url':data['url'].replace(" ","").strip()
        }
        db.SoureFile.insert(sourefile)
        flash("添加成功", 'ok')
        return redirect(url_for('admin.sourefile_list',page=1))
    return render_template('admin/sourefile_add.html',form=form)


@admin.route('/sourefile/list/<int:page>/')
def sourefile_list(page=None):
    if page==None:
        page=1
    # 跳转列表页
    sourefile = db.SoureFile.find().sort('_id', -1)
    count = sourefile.count()
    paper_obj = Pagination(request.args.get("page", page), count, request.path, request.args, per_page_count=10)
    html = paper_obj.page_html()
    param = []
    for v in range(count):
        param.append([v + 1, sourefile[v].get("_id"),sourefile[v].get('indexNum'),sourefile[v].get("title"), sourefile[v].get("publisher"),
                      sourefile[v].get("tag"),
                      sourefile[v].get("publishDate"),
                      sourefile[v].get("url")
                      ])
    index_list = param[paper_obj.start:paper_obj.end]
    return render_template('admin/sourefile_list.html',index_list=index_list,html=html)

@admin.route('/sourefile/del/<id>/',methods=['GET'])
def sourefile_del(id=None):
    db.SoureFile.remove({'_id': ObjectId(id)})
    flash("标签删除成功", 'del')
    return redirect(url_for('admin.sourefile_list',page=1))

@admin.route('/sourefile/edit/<id>/',methods=['GET','POST'])
def sourefile_edit(id=None):
    form=SoureFileForm()
    sourefile = db.SoureFile.find_one({'_id':ObjectId(id)})
    if request.method=='GET':
        form.tag_id.data=sourefile['tag']
        form.content.data=sourefile['content']

    if form.validate_on_submit():
        data=form.data
        sourefilecur=db.SoureFile.find_one({'title': data['title']} or {'indexNum':data['indexNum']}
                                          or {'fileNo':data['fileNo']})
        if sourefilecur and (sourefile['title']!=data['title'] or sourefile['indexNum']!=data['indexNum'] or sourefile['fileNo']!=data['fileNo']):
            flash('该源文件已存在','err')
            return redirect(url_for('admin.sourefile_edit',id=id))
        newsourefile={
            'indexNum': data['indexNum'].replace(" ","").strip(),
            'fileType': data['fileType'].replace(" ","").strip(),
            'publisher': data['publisher'].replace(" ","").strip(),
            'createTime': data['createTime'].replace(" ","").strip(),
            'title': data['title'].replace(" ","").strip(),
            'fileNo': data['fileNo'].replace(" ","").strip(),
            'publishDate': data['publishDate'].replace(" ","").strip(),
            'addtime': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            # 'path':r"\\",
            'content': data['content'].replace(" ", "").strip(),
            'tag': data['tag_id'].replace(" ","").strip(),
            'url': data['url'].replace(" ","").strip()
        }
        db.SoureFile.update(sourefile,{"$set": newsourefile})
        flash('更新成功','ok')
        return redirect(url_for('admin.sourefile_edit',id=id))
    return render_template('admin/sourefile_edit.html',form=form,sourefile=sourefile)



@admin.route('/cmpfile/add/',methods=['GET','POST'])
def cmpfile_add():
    form=CmpFileForm()
    if form.validate_on_submit():
        data=form.data
        sourefile = db.CmpFile.find_one({'fileName': data['fileName']} or {'indexNum':data['indexNum']}
                                          or {'fileNo':data['fileNo']})
        if sourefile:
            flash("该标签已存在", 'err')
            return redirect(url_for('admin.cmpfile_add'))
        cmpfile={
            'indexNum':data['indexNum'].replace(" ","").strip(),
            'classfication':data['classfication'].replace(" ","").strip(),
            'publisher':data['publisher'].replace(" ","").strip(),
            'fileCreateTime':data['fileCreateTime'],
            'fileName':data['fileName'].replace(" ","").strip(),
            'fileNo':data['fileNo'].replace(" ","").strip(),
            'publishDate':data['publishDate'],
            'addtime':datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'content':data['content'].replace(" ","").strip(),
            'tag':data['tag_id'],
            'fileWebsiteUrl':data['fileWebsiteUrl'].replace(" ","").strip(),
            'abolitionDate':data['abolitionDate'],
            'fileLocalUrl':data['fileLocalUrl'].replace(" ","").strip(),
            'fromDate':data['fromDate'],
            'keyword':data['keyword'].replace(" ","").strip(),
            'publisherCityName':data['publisherCityName'].replace(" ","").strip()
        }
        db.CmpFile.insert(cmpfile)
        flash("添加成功", 'ok')
        return redirect(url_for('admin.cmpfile_list',page=1))
    return render_template('admin/cmpfile_add.html',form=form)

@admin.route('/cmpfile/list/<int:page>')
def cmpfile_list(page=None):
    if page==None:
        page=1
    # 跳转列表页
    cmpfile = db.CmpFile.find().sort('_id', -1)
    count = cmpfile.count()
    paper_obj = Pagination(request.args.get("page", page), count, request.path, request.args, per_page_count=10)
    html = paper_obj.page_html()
    param = []
    for v in range(count):
        param.append([v + 1, cmpfile[v].get("_id"),cmpfile[v].get('fileName'),cmpfile[v].get("publisher"), cmpfile[v].get("publishDate"),
                      cmpfile[v].get("publisherCityName"),
                      cmpfile[v].get("tag"),
                      cmpfile[v].get("fileWebsiteUrl"),
                      ])
    index_list = param[paper_obj.start:paper_obj.end]
    return render_template('admin/cmpfile_list.html',index_list=index_list,html=html)

@admin.route('/cmpfile/del/<id>',methods=['GET'])
def cmpfile_del(id=None):
    db.CmpFile.remove({'_id': ObjectId(id)})
    flash("标签删除成功", 'del')
    return redirect(url_for('admin.cmpfile_list',page=1))

@admin.route('/cmpfile/edit/<id>',methods=['GET','POST'])
def cmpfile_edit(id=None):
    form=CmpFileForm()
    cmpfile=db.CmpFile.find_one({'_id':ObjectId(id)})
    if request.method=='GET':
        form.tag_id.data=cmpfile['tag']
        form.content.data=cmpfile['content']

    if form.validate_on_submit():
        data = form.data
        cmpfilecur = db.SoureFile.find_one({'fileName': data['fileName']} or {'indexNum':data['indexNum']}
                                          or {'fileNo':data['fileNo']})
        if cmpfilecur and (
                cmpfile['fileName'] != data['fileName'] or cmpfile['indexNum'] != data['indexNum'] or cmpfile[
            'fileNo'] != data['fileNo']):
            flash('该源文件已存在', 'err')
            return redirect(url_for('admin.cmpfile_edit', id=id))
        newcmpfile={
            'indexNum':data['indexNum'].replace(" ","").strip(),
            'classfication':data['classfication'].replace(" ","").strip(),
            'publisher':data['publisher'].replace(" ","").strip(),
            'fileCreateTime':data['fileCreateTime'],
            'fileName':data['fileName'].replace(" ","").strip(),
            'fileNo':data['fileNo'].replace(" ","").strip(),
            'publishDate':data['publishDate'],
            'addtime':datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'content':data['content'].replace(" ","").strip(),
            'tag':data['tag_id'].replace(" ","").strip(),
            'fileWebsiteUrl':data['fileWebsiteUrl'].replace(" ","").strip(),
            'abolitionDate':data['abolitionDate'],
            'fileLocalUrl':data['fileLocalUrl'].replace(" ","").strip(),
            'fromDate':data['fromDate'],
            'keyword':data['keyword'].replace(" ","").strip(),
            'publisherCityName':data['publisherCityName'].replace(" ","").strip()
        }
        db.CmpFile.update(cmpfile, {"$set": newcmpfile})
        flash('更新成功', 'ok')
        return redirect(url_for('admin.cmpfile_edit', id=id))
    return render_template('admin/cmpfile_edit.html',form=form,cmpfile=cmpfile)



#公告管理
@admin.route('/notice/list/<int:page>')
def notice_list(page=None):
    if page==None:
        page=1
    notice = db.Notice.find().sort('_id', -1)
    count = notice.count()
    paper_obj = Pagination(request.args.get("page", page), count, request.path, request.args, per_page_count=10)
    html = paper_obj.page_html()
    param = []
    for v in range(count):
        param.append([v + 1, notice[v].get("_id"), notice[v].get("content"),notice[v].get("activation"),notice[v].get("optuser"),notice[v].get("addtime")])
    index_list = param[paper_obj.start:paper_obj.end]
    return render_template("admin/notice_list.html", index_list=index_list, html=html)
@admin.route('/notice/add/',methods=['GET','POST'])
def notice_add():
    form = NoticeForm()
    if form.validate_on_submit():
        data = form.data
        notice = {
            'content': data['content'].replace(" ","").strip(),
            'addtime': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'optuser': session['admin'],
            'activation': data['activation']
        }
        db.Notice.insert(notice)
        flash("添加成功", 'ok')
        return redirect(url_for('admin.notice_list', page=1))
    return render_template('admin/notice_add.html',form=form)

@admin.route('/notice/del/<id>',methods=['GET'])
def notice_del(id=None):
    db.Notice.remove({"_id": ObjectId(id)})
    flash("公告删除成功",'del')
    return redirect(url_for('admin.notice_list',page=1))
@admin.route('/notice/edit/<id>',methods=['GET','POST'])
def notice_edit(id=None):
    form=NoticeForm()
    notice=db.Notice.find_one({"_id":ObjectId(id)})
    if request.method=='GET':
        form.activation.data=notice['activation']
    if form.validate_on_submit():
        data = form.data
        newnotice = {
            'content':data['content'],
            'activation':data['activation']
        }

        db.Notice.update(notice, {'$set': newnotice})
        flash("更新成功", 'ok')
        return redirect(url_for('admin.notice_edit', id=id))
    return render_template("admin/notice_edit.html", form=form, notice=notice)



















class Pagination(object):
    """
    自定义分页
    """
    def __init__(self, current_page, total_count, base_url, params, per_page_count=10, max_pager_count=11):
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        if current_page <= 0:
            current_page = 1
        self.current_page = current_page
        # 数据总条数
        self.total_count = total_count

        # 每页显示10条数据
        self.per_page_count = per_page_count

        # 页面上应该显示的最大页码
        max_page_num, div = divmod(total_count, per_page_count)
        if div:
            max_page_num += 1
        self.max_page_num = max_page_num

        # 页面上默认显示11个页码（当前页在中间）
        self.max_pager_count = max_pager_count
        self.half_max_pager_count = int((max_pager_count - 1) / 2)

        # URL前缀
        self.base_url = base_url

        # request.GET
        import copy
        params = copy.deepcopy(params)
        # params._mutable = True
        get_dict = params.to_dict()
        # 包含当前列表页面所有的搜/索条件
        # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
        # self.params[page] = 8
        # self.params.urlencode()
        # source=2&status=2&gender=2&consultant=1&page=8
        # href="/hosts/?source=2&status=2&gender=2&consultant=1&page=8"
        # href="%s?%s" %(self.base_url,self.params.urlencode())
        self.params = get_dict

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    def page_html(self):
        # 如果总页数 <= 11
        if self.max_page_num <= self.max_pager_count:
            pager_start = 1
            pager_end = self.max_page_num
        # 如果总页数 > 11
        else:
            # 如果当前页 <= 5
            if self.current_page <= self.half_max_pager_count:
                pager_start = 1
                pager_end = self.max_pager_count
            else:
                # 当前页 + 5 > 总页码
                if (self.current_page + self.half_max_pager_count) > self.max_page_num:
                    pager_end = self.max_page_num
                    pager_start = self.max_page_num - self.max_pager_count + 1  # 倒这数11个
                else:
                    pager_start = self.current_page - self.half_max_pager_count
                    pager_end = self.current_page + self.half_max_pager_count

        page_html_list = []
        # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
        # 首页
        self.params['page'] = 1
        first_page = '<li><a href="%s?%s">首页</a></li>' % (self.base_url, urlencode(self.params),)
        page_html_list.append(first_page)
        # 上一页
        self.params["page"] = self.current_page - 1
        if self.params["page"] < 1:
            pervious_page = '<li class="disabled"><a href="%s?%s" aria-label="Previous">上一页</span></a></li>' % (
                self.base_url, urlencode(self.params))
        else:
            pervious_page = '<li><a href = "%s?%s" aria-label = "Previous" >上一页</span></a></li>' % (
                self.base_url, urlencode(self.params))
        page_html_list.append(pervious_page)
        # 中间页码
        for i in range(pager_start, pager_end + 1):
            self.params['page'] = i
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?%s">%s</a></li>' % (self.base_url, urlencode(self.params), i,)
            else:
                temp = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, urlencode(self.params), i,)
            page_html_list.append(temp)

        # 下一页
        self.params["page"] = self.current_page + 1
        if self.params["page"] > self.max_page_num:
            self.params["page"] = self.current_page
            next_page = '<li class="disabled"><a href = "%s?%s" aria-label = "Next">下一页</span></a></li >' % (
                self.base_url, urlencode(self.params))
        else:
            next_page = '<li><a href = "%s?%s" aria-label = "Next">下一页</span></a></li>' % (
                self.base_url, urlencode(self.params))
        page_html_list.append(next_page)

        # 尾页
        self.params['page'] = self.max_page_num
        last_page = '<li><a href="%s?%s">尾页</a></li>' % (self.base_url, urlencode(self.params),)
        page_html_list.append(last_page)

        return ''.join(page_html_list)



