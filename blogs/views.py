from django.views.generic import ListView, DetailView
from .models import Post, Category

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
      context = super(PostList,self).get_context_data() # 기존 제공한 기능 context에 저장
      context['categories'] = Category.objects.all() # 카테고리 모든 정보를 딕셔너리 키와 연결
      context['no_category_post_count'] = Post.objects.filter(category=None).count() # 카테고리가 지정되지 않은 포스트 수 정보
      return context

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
      context = super(PostDetail,self).get_context_data() # 기존 제공한 기능 context에 저장
      context['categories'] = Category.objects.all() # 카테고리 모든 정보를 딕셔너리 키와 연결
      context['no_category_post_count'] = Post.objects.filter(category=None).count() # 카테고리가 지정되지 않은 포스트 수 정보
      return context
