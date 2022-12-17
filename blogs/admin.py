from django.contrib import admin

from .models import Post, Category

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )} # name을 입력했을 때, 자동으로 slug가 만들어진다.

admin.site.register(Category, CategoryAdmin)