from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import Article, Comment
from .forms import ArticleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from functools import wraps

# Create your views here.

def user_is_article_author(function):
    def wrap(request, *args, **kwargs):
        article_id = kwargs.get('id')
        article = get_object_or_404(Article, id = article_id)

        if request.user.is_authenticated and request.user == article.author:
            return function(request, *args, **kwargs)
        else:
            messages.info(request, "Bu islem için yetkiniz yok.")
            return redirect("/articles/dashboard")
    return wrap

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)

    return render(request, "dashboard.html", {"articles": articles})

@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()

        messages.success(request, "Makale Basariyla Eklendi")
        return redirect("article:dashboard")
    else:
        return render(request, "addarticle.html", {"form": form})

def detail(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all()

    return render(request, "detail.html", {"article": article, "comments": comments})

@login_required(login_url = "user:login")
@user_is_article_author
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    
    if form.is_valid():
        article = form.save(commit = False)
        article.author = request.user
        article.save()

        messages.success(request, "Makale Basariyla Guncellendi")
        return redirect("article:dashboard")
    else:
        return render(request, "update.html", {"form": form})

@login_required(login_url = "user:login")
@user_is_article_author
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()

    messages.success(request, "Makale Basariyla Silindi")
    return redirect("article:dashboard")

def articles(request):
    keyword = request.GET.get("keyword")
    
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
    else:
        articles = Article.objects.all()
    
    return render(request, "articles.html", {"articles": articles})

def addComment(request, id):
    article = get_object_or_404(Article, id = id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        
        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()

    return redirect(reverse("article:detail", kwargs = {"id": id}))