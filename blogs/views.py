from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from django.utils.text import slugify
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
    
    def form_valid(self, form):
      current_user = self.request.user
      if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
        form.instance.author = current_user
        response = super(PostCreate, self).form_valid(form) # 1. CreateView의 함수 결과값을 저장
        
        tags_str = self.request.POST.get('tags_str') # 2. POST 방식 정보 중 names='tags_str' 인 인풋값을 가져온다.
        if tags_str: # 3-1. tag_str이 존재하는 경우 구분자 처리하여
          tags_str = tags_str.strip()

          tags_str = tags_str.replace(',',';')
          tags_list = tags_str.split(';') # 3-2. 리스트 형태로 담는다.

          for t in tags_list:
            t = t.strip() # 4. 문자열로 담긴 리스트이므로 앞뒤 공백을 제거한 상태로 저장
            tag, is_tag_created = Tag.objects.get_or_create(name=t) # 5. name으로 갖는 태그가 있으면 가져오고 없으면 새로 만든다.
            if is_tag_created: # 만약 name을 갖는 테그가 없어 새로 생성했다면 
              tag.slug = slugify(t, allow_unicode=True) # 슬러그 값 생성
              tag.save() # 저장
            self.object.tags.add(tag) # 새로 태그를 만들었든 기존 것을 가져왔든 tags 필드에 추가
        return response # 결과값 리턴
            


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'category']

    template_name = 'blogs/post_update_form.html'

    def get_context_data(self, **kwargs):
      context = super(PostUpdate, self).get_context_data()
      if self.object.tags.exists():
        tags_str_list = list()
        for t in self.object.tags.all():
          tags_str_list.append(t.name)
        context['tags_str_default'] = '; '.join(tags_str_list)
      return context

    def dispatch(self, request, *args, **kwargs):
      # 방문자(request.user)는 로그인 상태, 작성자와 동일해야 합니다.
        if request.user.is_authenticated and request.user == self.get_object().author:
          return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
          raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
          tags_str = tags_str.strip()
          tags_str = tags_str.replace(',',';')
          tags_list = tags_str.split(';')

          for t in tags_list:
              t = t.strip
              tag, is_tag_created = Tag.objects.get_or_create(name=t)
              if is_tag_created:
                tag.slug = slugify(t, allow_unicode=True)
                tag.save()
              self.object.tags.add(tag)

        return response

def tag_page(request, slug):
  tag = Tag.objects.get(slug=slug)
  post_list = tag.post_set.all()

  return render(
    request,
    'blogs/post_list.html',
    {
      'post_list' : post_list,
      'tag' : tag,
      'categories' : Category.objects.all(),
      'no_category_post_count' : Post.objects.filter(category=None).count(),
    }
  )