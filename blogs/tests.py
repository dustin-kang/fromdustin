from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

class TestView(TestCase):
    def setUp(self):
        # setup()함수 내에서 기본적으로 Client를 사용하겠다.
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_biden = User.objects.create_user(username='biden', password='somepassword')

    def navbar_test(self, soup):
        # 1.4 네비게이션 바가 있다.
        navbar = soup.nav
        # 1.5 Blog, cv, project 라는 문구가 네비게이션 바에 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('CV', navbar.text)
        self.assertIn('Project', navbar.text)

        logo_btn = navbar.find('a', text='Dongwoo Kang')
        self.assertEqual(logo_btn.attrs['href'], '/')

        cv_btn = navbar.find('a', text='CV')
        self.assertEqual(cv_btn.attrs['href'], '/cv/')

        project_btn = navbar.find('a', text='Project')
        self.assertEqual(project_btn.attrs['href'], '/project/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        

    def  test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 Blog - Dongwoo Kang이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog - Dongwoo Kang')

        self.navbar_test(soup) # navbar_test 함수 실행


        # 2.1 메인 영역에 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 '아직 게시물이 존재하지 않습니다.'라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)


        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title= "첫 번째 포스트입니다.",
            content = 'Hello World. We are the world',
        )
        post_002 = Post.objects.create(
            title= "두 번째 포스트입니다.",
            content = '1등은 전부가 아니잖아요.',
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로 고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 '아직 게시물이 존재하지 않습니다.'라는 문구가 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title= "첫 번째 포스트입니다.",
            content = 'Hello World. We are the world',
        )
        # 1.2 그 포스트의 url의 '/blog/1/' 이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫번째 포스트의 상세 페이지 테스트
        # 2.1 첫번째 포스트의 url로 접근하면 정상 작동된다. (statcode : 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 포스트 목록 페이지와 똑같은 네비게이션 바가 있다.
        self.navbar_test(soup) # navbar_test 함수 실행

        # 2.3 첫번째 포스트의 제목이 웹 브라우저 탭 타이틀에 다 들어있다.
        self.assertIn(post_001.title, soup.title.text)

        # 2.4 첫번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 2.5 첫번쨰 포스트의 내용이 포스트 영역에 있다. 
        self.assertIn(post_001.content, post_area.text)

    def test_create_post(self):
        # 로그인이 안된 경우
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)
        # 로그인이 된 경우
        self.client.login(username='trump', password='somepassword')

        # 포스트 작성 페이지 테스트
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('📝 Create New Post', main_area.text)
