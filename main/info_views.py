from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, \
    CommentForm, BulletinForm, FileForm, BID_dataForm, BID_actionForm, InquiryForm, \
    Edit_BID_dataForm, Edit_BID_actionForm
from .info_forms import PostForm,Bid_articleForm
from .. import db
from ..models import User, Role, Permission,  Auction, Action,Yanzhengma
from ..info_models import Article
from ..decorators import admin_required, permission_required
import os
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        article = Article(

            title=form.title.data,
            body=form.body.data,
        )
        db.session.add(article)
        flash('The article has been created.')
        return render_template('edit_post.html', form=form)
    return render_template('edit_post.html', form=form)


# @main.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit(id):
#     post = Post.query.get_or_404(id)
#     if current_user != post.author and \
#             not current_user.can(Permission.ADMINISTER):
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.body = form.body.data
#         db.session.add(post)
#         flash('The post has been updated.')
#         return redirect(url_for('post', id=post.id))
#     form.body.data = post.body
#     return render_template('edit_post.html', form=form)

@main.route('/article/<title>')
def article(title):
    user = Article.query.filter_by(title=title).first()
    if user is None:
        abort(404)
    posts = article.order_by(Article.timestamp.desc()).all()
    return render_template('article.html', user=user, posts=posts)

# @main.route('/news/<title>')
# def news(title):
#     user = Article.query.filter_by(title=title).first()
#     if user is None:
#         abort(404)
#     posts = article.order_by(Article.timestamp.desc()).all()
#     return render_template('article.html', user=user, posts=posts)

@main.route('/CreateBid_article')
def CreateBid_article():
    form=Bid_articleForm()
    return render_template("CreateBid_article.html",form=form)

@main.route('/Moni')
def Moni():
    yan="code/yan0.jpg"
    answer=1356
    return render_template("Moni.html",yan=yan,answer=answer)

@main.route('/yanzhengma/<id>',methods=['GET'])
def yanzhengma(id):
    yanzhengma=Yanzhengma.query.get(id)
    yan=yanzhengma.picture
    return render_template("yanzhengma.html",yan=yan)
import json
from flask import jsonify
@main.route('/answer/<id>',methods=['GET'])
def answer(id):
    yanzhengma=Yanzhengma.query.get(id)
    answer=yanzhengma.answer
    answer=str(int(float(answer)))
    question=yanzhengma.question
    return jsonify(question = question,answer=answer)

@main.route('/yanzhengma_refresh',methods=['GET'])
def yanzhengma_refresh():
    yan='img/moni_fresh.png'
    return render_template("yanzhengma.html",yan=yan)

@main.route('/Practice',methods=['GET'])
def Practice():
    return render_template("Practice.html")