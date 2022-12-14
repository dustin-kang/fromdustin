from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')

    return render(
        request,
        'blogs/index.html',
        {
            'posts' : posts,
        }
    )

def post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blogs/post_page.html',
        {
            'post' : post,
        }
    )