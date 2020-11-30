from django.shortcuts import render, redirect
from .models import Post, PostComment
from .form import NewPostForm
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    posts = Post.objects.order_by("-date")
    content = {'posts': posts}
    return render(request, 'Blog/home.html', content)


def about(request):
    content = {'id': 'hello'}
    return render(request, 'Blog/about.html', content)


def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            img = form.cleaned_data['image']
            content = form.cleaned_data['content']
            new = Post.objects.create(title=title, content=content, author=request.user, image=img)
            messages.success(request, f"Your new post has successfully posted.")
            return redirect('blog-home')
    else:
        form = NewPostForm()
        return render(request, 'Blog/new_post.html', {'form': form})


def detail_post(request, id):
    post = Post.objects.get(id=id)
    comments = PostComment.objects.filter(post=post, parent=None)
    replies = PostComment.objects.filter(post=post).exclude(parent=None)
    replydict = {}
    for reply in replies:
        if reply.parent.id not in replydict.keys():
            replydict[reply.parent.id] = [reply.comment]
        else:
            replydict[reply.parent.id].append(reply.comment)
    return render(request, 'Blog/detail_post.html', {'post': post, 'comments': comments, 'replydict': replydict})


def post_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get('post_id')
        post = Post.objects.filter(id=post_id).first()
        parent = request.POST.get('parent')
        if parent == '':
            create_comment = PostComment(comment=comment, user=user, post=post)
            messages.success(request, f'your comment is successfully added.')
        else:
            parent = PostComment.objects.get(id=parent)
            create_comment = PostComment(comment=comment, user=user, post=post, parent=parent)
            messages.success(request, f'your reply is successfully added.')
        create_comment.save()
        return redirect('detail_post', post_id)


def user_post(request, author_id):
    posts = Post.objects.filter(author_id=author_id).order_by("-date")
    context = {'posts': posts}
    return render(request, 'Blog/user_posts.html', context)


def update_post(request, id):
    if request.method == "POST":
        post_update_form = NewPostForm(request.POST, request.FILES, instance=Post.objects.get(id=id))
        if post_update_form.is_valid():
            post_update_form.save()
            messages.success(request, f"Changes has been applied")
            return redirect('blog-home')
    else:
        post_update_form = NewPostForm(instance=Post.objects.get(id=id))
    return render(request, 'Blog/update_post.html', {'post_update_form': post_update_form})
