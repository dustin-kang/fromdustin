from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category
from django.core.exceptions import PermissionDenied

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

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'category']

    def test_func(self):
        # 스태프나 superuser인 경우에만 작성가능하다.
        return self.request.user.is_superuser or self.request.user.is_staff

class PostUpdate(LoginRequiredMixin, UpdateView):
      model = Post
      fields = ['title', 'hook_text', 'content', 'head_image', 'category']

      template_name = 'blog/post_update_form.html'

      def dispatch(self, request, *args, **kwargs):
        # 방문자(request.user)는 로그인 상태, 작성자와 동일해야 합니다.
          if request.user.is_authenticated and request.user == self.get_object().author():
              return super(PostUpdate, self).dispatch(request, *args, **kwargs)
          else:
            raise PermissionDenied
             