from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, \
    CommentForm, BulletinForm,FileForm,BID_dataForm,BID_actionForm,InquiryForm,\
Edit_BID_dataForm,Edit_BID_actionForm

from .. import db
from ..models import User, Role, Permission,Auction_data,BID_action
from ..info_models import Article
from ..decorators import admin_required, permission_required
import os
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

    # return render_template('index.html',  posts=posts,
    #                        show_followed=show_followed, show_new=show_new, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)





@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)




####点击后设置cookie,触发界面判断
@main.route('/all')
@login_required  #########要求登录
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    resp.set_cookie('show_new', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/new')
@login_required  #########要求登录
def show_new():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_new', '1', max_age=30 * 24 * 60 * 60)
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp




'''
@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
'''

# 上传

@main.route('/uploaded',methods=['GET','POST'])
@login_required  #########要求登录
@permission_required(Permission.SEARCH)
def uploaded():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        if file:
            file.save(os.path.join('.\\upload', filename))
            return render_template('uploaded.html')
        else:
            flash('失败：上传文件格式不对')
            return render_template('uploaded.html')
    else:
        return render_template('uploaded.html')

# 上传
@main.route('/file_upload',methods=['GET','POST'])
@login_required  #########要求登录
@permission_required(Permission.SEARCH)
def file_upload():
    form=FileForm()
    name=current_user.name
    if request.method == 'POST':
        if form.validate_on_submit():
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']
            file4 = request.files['file4']
            filename1 = name+'-'+file1.filename
            filename2 = name+'-'+file2.filename
            filename3 = name+'-'+file3.filename
            filename4 = name+'-'+file4.filename
            if file1 or file2 or file3 or file4:
                file1.save(os.path.join('.\\upload\\first', filename1))
                file2.save(os.path.join('.\\upload\\final', filename2))
                file3.save(os.path.join('.\\upload\\result', filename3))
                file4.save(os.path.join('.\\upload\\video', filename4))
                flash('上传成功')
                return render_template('file_upload.html',form=form)
            else:
                flash('请选择文件')
                return render_template('file_upload.html',form=form)
    else:
        return render_template('file_upload.html',form=form)


##
@main.route('/info',methods=['GET'])
@login_required  #########要求登录
@permission_required(Permission.SEARCH)
def info():
    name=current_user.name

    return render_template('info.html')



#创建标书信息
@login_required
@main.route('/bid_data', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def bid_data():
    # 判断是否是管理员
    user = User.query.filter_by(username=current_user.username).first()
    form =BID_dataForm(user)

    if form.validate_on_submit():

        # id格式化
        #id_format = '0x%04x' % int(form.id.data, base=16)
        device = Auction_data(

            IDnumber=form.IDnumber.data,
            BIDnumber=form.BIDnumber.data,
            BIDpassword=form.BIDpassword.data,
            author=Auction_data.query.get(form.action_user.data)
        )

        #判断标书是否存在
        flag = True
        if Auction_data.query.filter_by(IDnumber=device.IDnumber).count() > 0:
            flash('该身份证已存在')
        else:
            db.session.add(device)
            flash(u"添加成功")
        return render_template('BID_data.html',user=user, form=form)

    return render_template('BID_data.html',user=user, form=form)

#创建策略
@login_required
@main.route('/bid_action', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def bid_action():
    # 判断是否是管理员
    user = User.query.filter_by(username=current_user.username).first()
    form =BID_actionForm(user=user)

    if form.validate_on_submit():
        # id格式化
        #id_format = '0x%04x' % int(form.id.data, base=16)
        device = BID_action(
            diff=BID_action.query.get(form.diff.data),
            refer_time=BID_action.query.get(form.refer_time.data),
            bid_time=BID_action.query.get(form.bid_time.data),
            delay_time=BID_action.query.get(form.delay_time.data),
            ahead_price=BID_action.query.get(form.ahead_price.data),
            author=BID_action.query.get(form.action_user.data)
        )
        db.session.add(device)

        flash(u"添加成功")
        return render_template('BID_action.html',user=user, form=form)

    return render_template('BID_action.html',user=user, form=form)


#查询功能创建
@login_required
@main.route('/Inquiry_data', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def Inquiry_data():
    form=InquiryForm()
    name=current_user.name
    auction_data = db.session.query(Auction_data).all()
    return render_template("Inquiry_data.html", form=form,action_data=auction_data)

@login_required
@main.route('/Inquiry_action', methods=['GET', 'POST'])
@permission_required(Permission.SEARCH)
def Inquiry_action():
    form=InquiryForm()
    name=current_user.name
    action_data = db.session.query(BID_action).all()


    if request.method == 'POST':
        pass
        if form.validate_on_submit():
            pass


    return render_template("Inquiry_action.html", form=form,action_data=action_data)


###修改标书信息

@login_required
@main.route('/Edit_BID_data/<device_id>', methods=['GET', 'POST'])
@permission_required(Permission.SEARCH)
def Edit_BID_data(device_id):
    device = Auction_data.query.filter_by(id=device_id).first()

    # 判断是否是管理员
    if  1:                     #current_user.can(Permission.PRODUCTION):
        user = User.query.filter_by(username=current_user.username).first()
        form = Edit_BID_dataForm(user=user)

        # 判断是否提交
        if form.validate_on_submit():
            temp = list(request.form)
            # 判断是否点击的是删除键
            if temp.count('delete') > 0:
                db.session.delete(device)
            else:
                device.IDnumber = form.IDnumber.data
                device.BIDnumber = form.BIDnumber.data
                device.BIDpassword = form.BIDpassword.data
                device.author = Auction_data.query.get(form.action_user.data)
                db.session.add(device)
                flash(u"修改成功")
                return render_template('edit_bid_data.html', form=form, user=user, device=device)

        # 默认显示
        form.IDnumber.data = device.IDnumber
        form.BIDnumber.data = device.BIDnumber
        form.BIDpassword.data = device.BIDpassword
        form.action_user.data = device.author
        return render_template('edit_bid_data.html', form=form,user=user, device=device)


@login_required
@main.route('/Edit_action_data/<device_id>', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def Edit_action_data(device_id):
    device = BID_action.query.filter_by(id=device_id).first()

    # 判断是否是管理员
    if 1:
        user = User.query.filter_by(username=current_user.username).first()
        form = Edit_BID_actionForm(user=user)
        # 判断是否提交
        if form.validate_on_submit():
            temp = list(request.form)
            # 判断是否点击的是删除键
            if temp.count('delete') > 0:
                db.session.delete(device)
            else:
                device = BID_action(
                    diff=BID_action.query.get(form.diff.data),
                    refer_time=BID_action.query.get(form.refer_time.data),
                    bid_time=BID_action.query.get(form.bid_time.data),
                    delay_time=BID_action.query.get(form.delay_time.data),
                    ahead_price=BID_action.query.get(form.ahead_price.data),
                    author=BID_action.query.get(form.action_user.data)
                )
                db.session.add(device)
                db.session.commit()
                flash(u"修改成功")
                return render_template('edit_bid_action.html', form=form, user=user, device=device)

        # 默认显示
        form.diff.data = device.diff
        form.refer_time.data = device.refer_time
        form.bid_time.data = device.bid_time
        form.delay_time.data = device.delay_time
        form.ahead_price.data = device.ahead_price
        form.action_user.data = device.author_id

        return render_template('edit_bid_action.html', form=form,user=user, device=device)


