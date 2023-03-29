from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=35,verbose_name="Название категории",)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="Категории"
        verbose_name_plural="Категории"

class List_test(models.Model):
    name = models.CharField(max_length=35,verbose_name="Название теста")
    category =  models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="Категория теста")
    time_start = models.DateTimeField(verbose_name="Время начало теста")
    time_end = models.DateTimeField(verbose_name="Время окончания теста")
    count_answer = models.IntegerField(verbose_name="Кол-во вопросов в тесте")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="Тест"
        verbose_name_plural="Тесты"
    
    def get_absolute_url(self):
        return f'/testAdmin/{self.id}'

class Question(models.Model):
    ltest_id = models.ForeignKey(List_test,on_delete=models.CASCADE,verbose_name="Название теста")
    question =  models.TextField(max_length=1500,verbose_name="Вопрос")
    answer1 =  models.TextField(max_length=1500,verbose_name="Ответ 1")
    answer2 =  models.TextField(max_length=1500,verbose_name="Ответ 2")
    answer3 =  models.TextField(max_length=1500,verbose_name="Ответ 3")
    answer4 =  models.TextField(max_length=1500,verbose_name="Ответ 4")
    trueAnswer=  models.CharField(max_length=20,verbose_name="Номер правильного ответа")

    class Meta:
        verbose_name="Вопрос"
        verbose_name_plural="Вопросы"
    
    def get_absolute_url(self):
        return f'/questionAdmin/{self.id}'

class Result(models.Model):
    answers = models.CharField(max_length=5000000,verbose_name="Ответы на тест")
    user_id =models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Имя пользователя")
    list_test_id = models.ForeignKey(List_test,on_delete=models.CASCADE,verbose_name="Название теста")
    status= models.CharField(max_length=20,verbose_name="Статус теста")
    time= models.CharField(max_length=20,verbose_name="Время прохождения теста")

    class Meta:
        verbose_name="Результат"
        verbose_name_plural="Результаты"

    def get_absolute_url(self):
        return f'/resultAdmin/{self.id}'
