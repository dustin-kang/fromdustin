# My Web log Introduction (version 1.0)
## Table of Contents
- What is MyWeblog project?
- Overall description
- Prototype
- UserGuide

## What is MyWeblog project?
My Weblog Project is a just Resume + Blog Webside.
i want to logging Blog about Technical story, just strict contents are not fun.
> + To use Django Web Framework.

## Process
### 1. Create Web Design Prototype
To create a blog design:
 - Use Bootstrap 5.0.2.
 - in the Details field, add Markdownx libaray.
 - Before Implement, i created WireFrame

### 2. Django Basic Structure
```
blog - single_page
        - modal
     - blog
        - Create
        - Uploade
        - Detail
        - Search
        - Category
```

- Implement blog page using PostView
- To  Create Project information in Single_page, use Modal tag.

### 3. Implement Module
- Search Module : Use Modal Button and Post Search Class #27
- Pagination : Setting paginating count, Connect Html Tag #25
- Comment : Use DISQUS Social Comment, Available Use Comment without Login. #24
- Markdown : Change Post Model's Content Field to MardownxField #21
- Tag, Category : Implement categories to classify posts #12

### 4. Server Connect
- AWS LightSail : Use AWS for a better price.
> Of course, if there are more users and traffic, it should be upgraded to a better specification. better specification.
- Connects the instance image and static IP and opens the port for external connections.
- Use the Web server Nginx and Gunicorn as the WISG server to invoke Python programs for static and dynamic page requests.
- buy domain at Gabia.
- For security purposes, obtain an SSL certificate and apply it to Nginx, HTTPS protocol service
- Setting up logging processing for quick processing of various issues.


## UserGuide

- virtual Env : blog

1. Connecting to an SSH terminal for server operations.
```zsh
ssh -i ~/[ssh].pem ubuntu@[static ip or ]
```
2. git update
```zsh
projects/myblog/ $ git pull
```
3. gunicorn service start
```zsh
sudo systemctl restart myblog.service
sudo systemctl status myblog.service # error confirm
```
4. nginx service start
```zsh
sudo systemctl start nginx
sudo nginx -t # error confirm
```
0. Edit Ststic File Location
```
/etc/nginx/sites-available$ sudo nano myblog
```

### Module List
```
asgiref==3.5.2
beautifulsoup4==4.11.1
certifi==2022.12.7
charset-normalizer==2.1.1
distlib==0.3.6
Django==4.1.4
django-crispy-forms==1.14.0
django-markdownx==4.0.0b1
filelock==3.8.0
idna==3.4
importlib-metadata==5.1.0
Markdown==3.4.1
mock==4.0.3
Pillow==9.3.0
pipenv==2022.10.12
platformdirs==2.5.2
pytz==2022.7
requests==2.28.1
soupsieve==2.3.2.post1
sqlparse==0.4.3
tzdata==2022.7
urllib3==1.26.13
virtualenv==20.16.5
virtualenv-clone==0.5.7
zipp==3.11.0
```
### ENV List
```
conda 4.10.3
pip 22.3.1
python 3.9
```
