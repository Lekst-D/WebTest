from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Category, List_test, Question, Result
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import json
import urllib
import random
from WebTest.service import ResultfForView, ResultfTestForView, ResultfTestAdmin, ResultAnswer, AllTest, AllResult


def LoginPage(request):
    us = request.user
    if request.user.is_authenticated == True:
        return redirect(to='main')

    else:
        return render(request, "Login.html")

def LogIn(request):

    Login = request.POST.get("Login")
    Password = request.POST.get("Password")

    user = authenticate(username=Login, password=Password)
    if user is not None:
        login(request, user)
        return JsonResponse({"User": "main"})
    else:
        return JsonResponse({"User": "none"})

def LogOut(request):
    logout(request)
    return JsonResponse({"User": "none"})

def Main(request):
    # Name, Category, IdTest, ResultPersent, CountResult
    Ltest = List_test.objects.all()
    category = Category.objects.all()
    us = request.user
    d = dict()
    tests = list()
    for test in Ltest:
        result = Result.objects.filter(user_id=us.id, list_test_id=test)
        count = result.count()
        if (count != 0 ):
            last_result = result.last()
            st = last_result.answers
            d.clear()
            s1 = json.dumps(st)
            d = json.loads(s1)
            d = json.loads(d)

            if (last_result.status == "Завершон" and result.count() >= 2):
                count = 3

            i = 0
            rightcountanswer = 0
            for key, value in d.items():
                questions = Question.objects.get(id=key)
                st_answer = ""
                if ("1" in questions.trueAnswer):
                    st_answer = questions.answer1
                if ("2" in questions.trueAnswer):
                    st_answer = questions.answer2
                if ("3" in questions.trueAnswer):
                    st_answer = questions.answer3
                if ("4" in questions.trueAnswer):
                    st_answer = questions.answer4

                if (value == st_answer):
                    rightcountanswer += 1
                    i += 1

            i = ((rightcountanswer/int(test.count_answer))*100)

            allTest = AllTest(test.name,
                              test.category.name,
                              test.id,
                              i,
                              count
                              )
            tests.append(allTest)
        else:
            last_result = 0
            st = 'none'
            allTest = AllTest(test.name,
                              test.category.name,
                              test.id,
                              "0",
                              "none"
                              )
            tests.append(allTest)

    resultsTests = list()
    for test in Ltest:
        result = Result.objects.filter(
            user_id=us.id, status="Завершон", list_test_id=test)
        count = result.count()
        name = test.name
        category = test.category.name
        idResult1 = 'none'
        idResult2 = 'none'
        result1 = 'none'
        result2 = 'none'
        if (count != 0):
            if (count == 1):
                last_result = result.last()
                idResult1 = last_result.id
                st = last_result.answers
                d.clear()
                s1 = json.dumps(st)
                d = json.loads(s1)
                d = json.loads(d)
                i = 0
                rightcountanswer = 0
                for key, value in d.items():
                    questions = Question.objects.get(id=key)
                    st_answer = ""
                    if ("1" in questions.trueAnswer):
                        st_answer = questions.answer1
                    if ("2" in questions.trueAnswer):
                        st_answer = questions.answer2
                    if ("3" in questions.trueAnswer):
                        st_answer = questions.answer3
                    if ("4" in questions.trueAnswer):
                        st_answer = questions.answer4

                    if (value == st_answer):
                        rightcountanswer += 1
                        i += 1

                i = ((rightcountanswer/int(test.count_answer))*100)
                result1 = i

            if (count == 2):
                first_result = result.first()
                last_result = result.last()
                idResult1 = first_result.id
                idResult2 = last_result.id

                st = first_result.answers
                d.clear()
                s1 = json.dumps(st)
                d = json.loads(s1)
                d = json.loads(d)
                i = 0
                rightcountanswer = 0
                for key, value in d.items():
                    questions = Question.objects.get(id=key)
                    st_answer = ""
                    if ("1" in questions.trueAnswer):
                        st_answer = questions.answer1
                    if ("2" in questions.trueAnswer):
                        st_answer = questions.answer2
                    if ("3" in questions.trueAnswer):
                        st_answer = questions.answer3
                    if ("4" in questions.trueAnswer):
                        st_answer = questions.answer4

                    if (value == st_answer):
                        rightcountanswer += 1
                        i += 1

                i = ((rightcountanswer/int(test.count_answer))*100)
                result1 = i

                st = last_result.answers
                d.clear()
                s1 = json.dumps(st)
                d = json.loads(s1)
                d = json.loads(d)
                i = 0
                rightcountanswer = 0
                for key, value in d.items():
                    questions = Question.objects.get(id=key)
                    st_answer = ""
                    if ("1" in questions.trueAnswer):
                        st_answer = questions.answer1
                    if ("2" in questions.trueAnswer):
                        st_answer = questions.answer2
                    if ("3" in questions.trueAnswer):
                        st_answer = questions.answer3
                    if ("4" in questions.trueAnswer):
                        st_answer = questions.answer4

                    if (value == st_answer):
                        rightcountanswer += 1
                        i += 1

                i = ((rightcountanswer/int(test.count_answer))*100)
                result2 = i
            # name, category, idResult1, idResult2, result1, result2)
            resultTest = AllResult(name,
                                   category,
                                   idResult1,
                                   idResult2,
                                   result1,
                                   result2
                                   )
            resultsTests.append(resultTest)

    data = {'tests': tests, "resultsTests": resultsTests}
    return render(request, "Main.html", data)

def TestInfo(request, idTest):

    Ltest = List_test.objects.get(id=idTest)
    data = {'Ltest': Ltest}
    return render(request, "TestInfo.html", data)

def Test(request, idTest):
    us = request.user
    result = (Result.objects.filter(
        user_id=us.id, status="Исполняется")).last()
    c = list()
    d = dict()
    i = 0

    if result is not None:
        st = result.answers

        s1 = json.dumps(st)
        d = json.loads(s1)
        d = json.loads(d)
        for key, value in d.items():
            questions = Question.objects.get(id=key)
            resultForView = ResultAnswer(key, questions, value)
            i += 1
            c.append(resultForView)
        data = {"c": c, "idTest": idTest,"idRes":result.id }
        return render(request, "Testing.html", data)
    else:

        questions = Question.objects.filter(ltest_id=idTest)
        Ltest = List_test.objects.get(id=idTest)

        id = list()
        for value in questions:
            id.append(int(value.id))

        random.shuffle(id)
        i = Ltest.count_answer
        st = '{'
        for value in id:
            i -= 1
            number = value
            if (i != 0):
                st += f"\"{number}\": \"0!0\" , "
            else:
                st += f"\"{number}\": \"0!0\" "
                break
        st += '}'

        s1 = json.dumps(st)
        d = json.loads(s1)
        d = json.loads(d)

        for key, value in d.items():
            questions = Question.objects.get(id=key)
            resultForView = ResultAnswer(key, questions, value)
            i += 1
            c.append(resultForView)

        result = Result()
        result.answers = st
        result.user_id = us
        result.list_test_id = Ltest
        result.time = "40 00"
        result.status = "Исполняется"
        result.save()

        data = {"c": c, "st": st,"idRes":result.id}
        return render(request, "Testing.html", data)
        # Test(request,idTest)

    # st='{'
    # while(i<0):

    # st=st+"}"
    # result = Result()
    # result.answers = answer
    # result.user_id = us
    # result.value = 20
    # result.list_test_id = (Ltest)
    # result.time = "0"
    # result.status = "Испольняется"
    # result.save()

    data = {'questions': questions, 'idTest': idTest, 'c': st}
    return render(request, "Testing.html", data)


def ResultCreate(request):

    us = request.user
    answer = request.POST.get("answer")
    testID = (request.POST.get("testID"))
    stat = (request.POST.get("status"))

    Ltest = List_test.objects.get(id=testID)
    result = Result.objects.filter(user_id=us, list_test_id=Ltest.id)

    if (result.count() > 0):
        # return JsonResponse({"text": "successfull","id":result.count()-1})
        res = (Result.objects.filter(user_id=us, list_test_id=Ltest.id).last())
        # .update(answers=answer)
        res.answers = answer
        res.status = stat
        res.save()
        # result[0].user_id = us
        # result[0].value = 20
        # result[0].list_test_id = (Ltest)
        # result[0].time = "11:58"
        # result[0].status = "Испольняется"
        return JsonResponse({"text": answer, "id": res.id})
    else:
        result = Result()
        result.answers = answer
        result.user_id = us
        result.value = 20
        result.list_test_id = (Ltest)
        result.time = "11:58"
        result.status = "Исполняется"
        result.save()

    return JsonResponse({"text": "successfull", "id": result.last().id})


def ResultUser(request, idResult):

    result = Result.objects.get(id=idResult)
    question = Question.objects.filter(ltest_id=result.list_test_id)
    test = List_test.objects.get(id=result.list_test_id.id)
    category = Category.objects.get(id=test.category.id)

    st = result.answers
    # resultValue =json.loads(st)
    d = dict()
    # n=(urllib.unquote(st))
    # d = json.loads("{"+st+"}")
    s1 = json.dumps(st)
    d = json.loads(s1)
    d = json.loads(d)

    # for key,value in d.keys():
    # keysdict =d.keys()
    # valuedict =d.values()

    c = list()
    i = 0
    rightcountanswer = 0
    for key, value in d.items():
        questions = Question.objects.get(id=key, ltest_id=result.list_test_id)
        st_answer = ""
        if ("1" in questions.trueAnswer):
            st_answer = questions.answer1
        if ("2" in questions.trueAnswer):
            st_answer = questions.answer2
        if ("3" in questions.trueAnswer):
            st_answer = questions.answer3
        if ("4" in questions.trueAnswer):
            st_answer = questions.answer4

        if (value == st_answer):
            rightcountanswer += 1

        resultForView = ResultfForView(
            questions.question, key, value, st_answer)
        i += 1
        c.append(resultForView)

    # resultForView=ResultfForView(question[0].question,'0',"asd","asdf")

    # c.append(resultForView)

    data = {'result': result, 'question': question,
            'test': test, 'category': category,
            'resultForView': c, 'countright': rightcountanswer}

    return render(request, "ResultUser.html", data)


def QuestionAdmin(request, idQuestion):
    question = Question.objects.get(id=idQuestion)
    data = {'question': question}
    return render(request, "QuestionAdmin.html", data)


def ResultAdmin(request, idResult):

    result = Result.objects.get(id=idResult)
    question = Question.objects.filter(ltest_id=result.list_test_id)
    test = List_test.objects.get(id=result.list_test_id.id)
    category = Category.objects.get(id=test.category.id)

    FIO = result.user_id.first_name

    st = result.answers
    d = dict()
    s1 = json.dumps(st)
    d = json.loads(s1)
    d = json.loads(d)
    c = list()
    i = 0
    rightcountanswer = 0

    for key, value in d.items():
        questions = Question.objects.get(id=key, ltest_id=result.list_test_id)
        st_answer = ""
        done = "no"
        if ("1" in questions.trueAnswer):
            st_answer = questions.answer1
        if ("2" in questions.trueAnswer):
            st_answer = questions.answer2
        if ("3" in questions.trueAnswer):
            st_answer = questions.answer3
        if ("4" in questions.trueAnswer):
            st_answer = questions.answer4

        if (value == st_answer):
            rightcountanswer += 1
            done = "yes"

        resultForView = ResultfTestAdmin(questions.id, questions.question, questions.answer1, questions.answer2, questions.answer3, questions.answer4,
                                         st_answer, done)
        i += 1
        c.append(resultForView)

    rightcountanswer = ((rightcountanswer/int(test.count_answer))*100)

    data = {'result': result, 'question': question,
            'test': test, 'category': category,
            'resultForView': c, 'countright': rightcountanswer,
            'FIO': FIO, }

    return render(request, "ResultAdmin.html", data)


def TestAdmin(request, idTest):

    test = List_test.objects.get(id=idTest)
    question = Question.objects.filter(ltest_id=test.id)
    category = Category.objects.get(id=test.category.id)
    countQuestion =question.count()
    data = {'question': question,
            'test': test, 'category': category,"countQuestion":countQuestion}

    return render(request, "TestAdmin.html", data)
