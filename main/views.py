from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, \
    CommentForm, BulletinForm, FileForm, BID_dataForm, BID_actionForm, InquiryForm, \
    Edit_BID_dataForm, Edit_BID_actionForm
from ..auth.forms import LoginForm

from .. import db
from ..models import User, Role, Permission, Auction, Action
from ..info_models import Article
from ..decorators import admin_required, permission_required
import os
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
import xlrd, xlwt


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


# @main.route('/user/<username>')
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     return render_template('user.html', user=user, posts=posts,
#                            pagination=pagination)


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


# @main.route('/post/<int:id>', methods=['GET', 'POST'])
# def post(id):
#     post = Post.query.get_or_404(id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment(body=form.body.data,
#                           post=post,
#                           author=current_user._get_current_object())
#         db.session.add(comment)
#         flash('Your comment has been published.')
#         return redirect(url_for('.post', id=post.id, page=-1))
#     page = request.args.get('page', 1, type=int)
#     if page == -1:
#         page = (post.comments.count() - 1) // \
#                current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
#     pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
#         page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('post.html', posts=[post], form=form,
#                            comments=comments, pagination=pagination)


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

@main.route('/uploaded', methods=['GET', 'POST'])
@login_required  #########要求登录
@permission_required(Permission.SEARCH)
def uploaded():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        if file:
            file.save(os.path.join(os.environ.get('upload'), filename))
            return render_template('uploaded.html')
        else:
            flash('失败：上传文件格式不对')
            return render_template('uploaded.html')
    else:
        return render_template('uploaded.html')


# 上传
@main.route('/file_upload', methods=['GET', 'POST'])
@login_required  #########要求登录
@permission_required(Permission.SEARCH)
def file_upload():
    form = FileForm()
    name = current_user.username
    print(os.environ.get('upload'))
    if request.method == 'POST':
        if form.validate_on_submit():
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']
            file4 = request.files['file4']
            print(file1.filename, name)
            filename1 = name + '-' + file1.filename
            filename2 = name + '-' + file2.filename
            filename3 = name + '-' + file3.filename
            filename4 = name + '-' + file4.filename
            if file1 or file2 or file3 or file4:
                file1.save(os.path.join(os.environ.get('upload'), filename1))
                file2.save(os.path.join(os.environ.get('upload'), filename2))
                file3.save(os.path.join(os.environ.get('upload'), filename3))
                file4.save(os.path.join(os.environ.get('upload'), filename4))
                flash('上传成功')
                return render_template('file_upload.html', form=form)
            else:
                flash('请选择文件')
                return render_template('file_upload.html', form=form)
    else:
        return render_template('file_upload.html', form=form)


##
@main.route('/info', methods=['GET'])
@login_required  #########要求登录
@permission_required(Permission.SEARCH)
def info():
    username = current_user.username
    user=User.query.filter_by(username=username).first()
    if user.username:
        actions=Action.query.filter_by(author=user).all()
    return render_template('info.html',actions=actions)


# 创建标书信息
@login_required
@main.route('/bid_data', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def bid_data():
    # 判断是否是管理员
    user = User.query.filter_by(username=current_user.username).first()
    form = BID_dataForm()
    if form.validate_on_submit():

        # id格式化
        # id_format = '0x%04x' % int(form.id.data, base=16)
        device = Auction(
            description=form.description.data,
            IDnumber=form.IDnumber.data,
            BIDnumber=form.BIDnumber.data,
            BIDpassword=form.BIDpassword.data,
            count=form.count.data,
            status=form.status.data
        )

        # 判断标书是否存在
        flag = True
        if Auction.query.filter_by(IDnumber=device.IDnumber).count() > 0:
            flash('该身份证已存在')
        else:
            db.session.add(device)
            flash(u"添加成功")
        return render_template('BID_data.html', user=user, form=form)

    return render_template('BID_data.html', user=user, form=form)


# 创建策略
@login_required
@main.route('/bid_action', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def bid_action():
    user = User.query.filter_by(username=current_user.username).first()
    form = BID_actionForm(user=user)

    if form.validate_on_submit():
        # id格式化
        # id_format = '0x%04x' % int(form.id.data, base=16)
        # print(Action.query.get(form.date.data))
        device = Action(
            diff=form.diff.data,
            refer_time=form.refer_time.data,
            bid_time=form.bid_time.data,
            delay_time=form.delay_time.data,
            ahead_price=form.ahead_price.data,
            date=form.date.data,
            auction=Auction.query.get(form.auction_use.data),
            author=User.query.get(form.action_user.data)
        )
        db.session.add(device)
        # auction=Action.query.get(form.auction_use.data),  用ID查找 query.get_or_404

        flash(u"添加成功")
        return render_template('BID_action.html', user=user, form=form)

    return render_template('BID_action.html', user=user, form=form)


###修改标书信息

@login_required
@main.route('/Edit_BID_data/<device_id>', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def Edit_BID_data(device_id):
    device = Auction.query.filter_by(id=device_id).first()

    # 判断是否是管理员
    if 1:  # current_user.can(Permission.PRODUCTION):
        user = User.query.filter_by(username=current_user.username).first()
        form = Edit_BID_dataForm(user=user)

        # 判断是否提交
        if form.validate_on_submit():
            temp = list(request.form)
            # 判断是否点击的是删除键
            if temp.count('delete') > 0:
                db.session.delete(device)
            else:
                device.description=form.description.data
                device.IDnumber=form.IDnumber.data
                device.BIDnumber=form.BIDnumber.data
                device.BIDpassword=form.BIDpassword.data
                device.count = form.count.data
                device.status = form.status.data
                # 判断标书是否存在
                flag = True
                if Auction.query.filter_by(IDnumber=device.IDnumber).count() > 0:
                    flash('该身份证已存在')
                else:
                    db.session.commit()
                    flash(u"修改成功")
                return render_template('edit_bid_data.html', form=form, user=user, device=device)

        # 默认显示
        form.description.data = device.description
        form.IDnumber.data = device.IDnumber
        form.BIDnumber.data = device.BIDnumber
        form.BIDpassword.data = device.BIDpassword
        return render_template('edit_bid_data.html', form=form, user=user, device=device)


@login_required
@main.route('/Edit_action_data/<device_id>', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def Edit_action_data(device_id):
    device = Action.query.filter_by(id=device_id).first()

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
                device.diff = form.diff.data
                device.refer_time = form.refer_time.data
                device.bid_time = form.bid_time.data
                device.delay_time = form.delay_time.data
                device.ahead_price = form.ahead_price.data
                device.date=form.date.data
                device.auction=Auction.query.get(form.auction_use.data)
                device.author=User.query.get(form.action_user.data)
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

        return render_template('edit_bid_action.html', form=form, user=user, device=device)


# 操作EXCEL
def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

        # 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引


def excel_table_byindex(file='file.xls', colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list  # 返回元素为字典的列表


allowed_extensions = ['xls', 'xlsx']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_extensions


@login_required
@main.route('/Create_auction', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def Create_auction():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        print(filename)
        # 判断文件名是否合规
        if file and allowed_file(filename):
            file.save(os.path.join(os.environ.get('upload'), filename))
        else:
            flash('上传的格式不对')
            return render_template('Create_auction.html')

            # 添加到数据库
        print(os.path.join(os.environ.get('upload'), filename))
        tables = excel_table_byindex(file=os.path.join(os.environ.get('upload'), filename))
        for row in tables:  ## 判断表格式是否对
            if '标书说明' not in row or \
                            '身份证号' not in row or \
                            '标书号' not in row or \
                            '标书密码' not in row:
                flash('失败:excel表格式不对')
                return render_template('Create_auction.html')
            try:
                device = Auction(
                    description=row['标书说明'],
                    IDnumber=row['身份证号'],
                    BIDnumber=int(row['标书号']),
                    BIDpassword=int(row['标书密码']),
                    expirydate=str(row['有效期截止时间']),
                    count=int(row['剩余次数']),
                    status=int(row['状态'])

                )
            except:
                flash('失败:excel表格式不对')
                return render_template('Create_auction.html')
            try:
                db.session.add(device)
                db.session.commit()
            except:
                db.session.rollback()
                flash('失败:excel表格式不对')
                return render_template('Create_auction.html')
        flash("添加策略成功")
        return render_template('Create_auction.html')
    else:
        return render_template('Create_auction.html')


@login_required
@main.route('/Create_action', methods=['GET', 'POST'])
@permission_required(Permission.EDIT)
def Create_action():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        # 判断文件名是否合规
        if file and allowed_file(filename):
            file.save(os.path.join(os.environ.get('upload'), filename))
        else:
            flash('上传的格式不对')
            return render_template('Create_action.html')
        # 添加到数据库
        tables = excel_table_byindex(file=os.path.join(os.environ.get('upload'), filename))
        for row in tables:  ## 判断表格式是否对
            if '加价时间' not in row or \
                            '加价幅度' not in row or \
                            '截止时间' not in row or \
                            '延迟时间' not in row or \
                            '提前价格' not in row or \
                            '日期' not in row or \
                            '标书' not in row or \
                            '拍手' not in row:
                flash('失败:excel表格式不对')
                return render_template('Create_action.html')
                ##### 判断手持机字段是否存在
            try:
                device = Action(
                    refer_time=float(row['加价时间']),
                    diff=int(row['加价幅度']),
                    bid_time=float(row['截止时间']),
                    delay_time=float(row['延迟时间']),
                    ahead_price=int(row['提前价格']),
                    date=row['日期'],
                    auction=Auction.query.filter_by(description=row['标书']).first(),
                    author=User.query.filter_by(username=row['拍手']).first()
                )

            except:
                flash('失败:excel表数据格式不对')
                return render_template('Create_action.html')
            try:
                db.session.add(device)
                db.session.commit()
            except:
                db.session.rollback()
                flash('失败:excel表数据格式不对')
                return render_template('Create_action.html')
        flash("添加策略成功")
        return render_template('Create_action.html')
    else:
        return render_template('Create_action.html')


# @login_required
# @main.route('/serch/actions/<name>/<date>/<int:auction_id>/<int:action_id>',methods=['GET'])
# @permission_required(Permission.EDIT)
# def seach_actions(name,auction_id,action_id):
#     pass
#
#
# @login_required
# @main.route('/serch/auctions/<name>/<date>/<int:auction_id>/<int:action_id>',methods=['GET'])
# @permission_required(Permission.EDIT)
# def seach_auctions(name,auction_id,action_id):
#     pass


@login_required
@main.route('/serch', methods=['GET'])
@permission_required(Permission.EDIT)
def seach():
    date_month = ["17年%d月" % i for i in range(8, 13)]
    date_month2 = ["18年%d月" % i for i in range(1, 13)]
    date_month.extend(date_month2)
    dates = date_month
    auctions = Auction.query.order_by(Auction.description).all()
    users = User.query.order_by(User.username).all()
    return render_template('serch_auction.html', dates=dates, auctions=auctions, users=users)


@login_required
@main.route('/serch_auctions', methods=['GET'])
@permission_required(Permission.EDIT)
def seach_auctions():
    date = request.args.get('date')
    auction = request.args.get('auction')
    action = request.args.get('username')
    if date == "all":
        actions = Action.query.all()
    else:
        actions = Action.query.filter_by(date=date).all()

    return render_template('auctions.html', actions=actions)


@login_required
@main.route('/serch_actions', methods=['GET'])
@permission_required(Permission.EDIT)
def seach_actions():
    date = request.args.get('date')
    auction = request.args.get('auction')
    action = request.args.get('username')
    if date == "all":
        actions = Action.query.all()
    else:
        actions = Action.query.filter_by(date=date).all()

    return render_template('actions.html', actions=actions)


# 查询功能创建
@login_required
@main.route('/Inquiry_data', methods=['GET'])
@permission_required(Permission.EDIT)
def Inquiry_auction():
    date_month = ["17年%d月" % i for i in range(8, 13)]
    date_month2 = ["18年%d月" % i for i in range(1, 13)]
    date_month.extend(date_month2)
    dates = date_month
    auctions = db.session.query(Auction).all()
    users = User.query.order_by(User.username).all()
    return render_template('serch_auction.html', dates=dates, auctions=auctions, users=users)


@login_required
@main.route('/Inquiry_action', methods=['GET'])
@permission_required(Permission.EDIT)
def Inquiry_action():
    date_month = ["17年%d月" % i for i in range(8, 13)]
    date_month2 = ["18年%d月" % i for i in range(1, 13)]
    date_month.extend(date_month2)
    dates = date_month
    auctions = Auction.query.order_by(Auction.description).all()
    users = User.query.order_by(User.username).all()
    actions = Action.query.order_by(Action.refer_time).all()
    return render_template('serch_action.html', dates=dates, auctions=auctions,
                           users=users, actions=actions)

@main.route('/rules', methods=['GET','POST'])
def rules():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login',next='/rules'))
    else:
        return render_template('/create/coursestudy.html')


@main.route('/coursestudy', methods=['GET','POST'])
def coursestudy():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login', next='/coursestudy'))
    else:
        return render_template('/create/coursestudy.html')

@main.route('/softwarestudy', methods=['GET','POST'])
def softwarestudy():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login', next='/softwarestudy'))
    else:
        return render_template('/create/coursestudy.html')


