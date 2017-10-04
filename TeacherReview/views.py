# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
from .models import Teacher , Review , Questions
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
from django.template.loader import render_to_string

import datetime

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def login(request):
    return render(request , 'login.html')

def review(request):
    current = request.session.get("review" , "")
    if(current == ""):
        current = 1
        request.session['review'] = 1
    q = Questions.objects.all()
    teach = Teacher.objects.all().filter(semester = request.session["sem"] , div = request.session["div"] , teacher_class_id = current)
    name = ""
    for i in teach:
        name = i.name 
    return render(request , "review.html" , {"ques" : q , "name" : name , "pos" : current})
        


def process(request):
    q = Questions.objects.all()
    teach = Teacher.objects.get(semester = request.session["sem"] , div = request.session["div"] , teacher_class_id = request.session["review"])
    for i in range(1,q.__len__() + 1):
        ques = Questions.objects.get(question_no = i)
        Review(teacher = teach , question = ques , ans = request.GET.get(str(i),0)).save()
    request.session['review'] +=1
    if(request.session['review'] > 6):
        request.session['review'] = ""
        return HttpResponseRedirect("/app/dashboard")
    return HttpResponseRedirect("/app/review")

def skip(request):
    request.session['review'] +=1
    if(request.session['review'] > 6):
        request.session['review'] = ""
        return HttpResponseRedirect("/app/dashboard")
    return HttpResponseRedirect("/app/review")

def cancel(request):
    request.session['review'] = ""
    return HttpResponseRedirect("/app/dashboard")

def printpdf(request):
    teacherid = request.GET.get("id","0")
    sem = request.session["sem"]
    divi = request.session["div"]
    scores = ["0","2","4","6","8","10"]
    opinion = ["No Opinion" , "Strongly Disagree" , "Disagree" , "Neutral" , "Agree" , "Strongly Agree"]
    out = []
    q = Questions.objects.all()
    for k in q:
        current_score = [0] * scores.__len__()
        cquestion = "Q" + str(k.question_no) + " " + k.question 
        for i,j in enumerate(scores):
            pass
            current_score[i] = Review.objects.all().filter(teacher__semester = sem , teacher__div = divi , teacher__teacher_class_id = teacherid , question__question_no = k.question_no , ans = j).__len__()
        outlis = [  str(current_score[x]) + str("    " ) for x,y in enumerate(opinion)]
        out.append({"question" : cquestion , "result" : "   " + "  ".join(outlis) })
    tname = Teacher.objects.get(semester = sem , div = divi , teacher_class_id = teacherid).name
    tcourse = Teacher.objects.get(semester = sem , div = divi , teacher_class_id = teacherid).course

    data = {
        "sem": sem, "div": divi.upper(), "name": tname, "ques": out , "course" : tcourse , "date" : datetime.datetime.now().date()
    }
    pdf = render_to_pdf('printpdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
    #return render(request,"printpdf.html",{ })

def logout(request):
    request.session["sem"] = ""
    request.session["div"] = ""
    return HttpResponseRedirect("/app/login")

def dash(request):
    if( u"sem"   in request.GET.keys()):
        request.session["sem"] = request.GET.get("sem")
        request.session["div"] = request.GET.get("div").lower()
        print "Here"
        return HttpResponseRedirect("/app/dashboard")
    sem = request.session["sem"]
    div = request.session["div"]
    teach = Teacher.objects.all().filter(semester = sem , div = div )
    data_name = []
    for i in range(1,7):
        name = ""
        course = ""
        check = False
        for k in teach :
            if(k.teacher_class_id == i ):name = k.name ; course = k.course
        if(name == ""):name = "unknown" ; course = "unknown"
        data_name.append({ "pos" :  i , "name" : name , "course" : course ,  "printurl" : "/app/printpdf?id=" + str(i) })
    return render(request , "dashboard.html" , {"data" : data_name , "sem" : sem , "div" : div.upper})

def set(request):
    sem = request.session["sem"]
    div = request.session["div"]
    for i in range(1,7):
            teach = Teacher.objects.all().filter(semester = sem , div = div , teacher_class_id = i )
            if(teach.__len__() == 1):Teacher.objects.all().filter(semester = sem , div = div , teacher_class_id = i ).update(name = request.GET.get("N" + str(i)) , course = request.GET.get("C" + str(i)) )
            else:
                Teacher(name = request.GET.get("N" + str(i)) , course = request.GET.get("C" + str(i)) , semester = sem , div = div , teacher_class_id = i ).save()
    return HttpResponseRedirect("/app/dashboard")