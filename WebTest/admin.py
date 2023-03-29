from django.contrib import admin
from .models import List_test, Question, Result, Category


class CategoryAdmin(admin.ModelAdmin):
        list_display=('id','name',)
        list_display_links=('id','name',)
        search_fields=('name',)

class List_testAdmin(admin.ModelAdmin):
        list_display=('id','name','category','time_start','time_end',)
        list_display_links=('id','name','category','time_start','time_end',)
        search_fields=('name','category',)

class QuestionAndmin(admin.ModelAdmin):
        list_display=('id',"ltest_id",'question',)
        list_display_links=('id','question',"ltest_id",)
        search_fields=('question',)

class ResultAdmin(admin.ModelAdmin):
        list_display=('id','user_id','list_test_id','time','status',)
        list_display_links=('id','user_id','list_test_id',)
        search_fields=('user_id','status','list_test_id',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(List_test,List_testAdmin)
admin.site.register(Question,QuestionAndmin)
admin.site.register(Result,ResultAdmin)
