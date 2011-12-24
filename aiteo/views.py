from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.importlib import import_module

from django.contrib.auth.decorators import login_required

from aiteo.forms import AskQuestionForm, AddResponseForm
from aiteo.groups import group_and_bridge, group_context
from aiteo.models import Question
from django.utils import simplejson

workflow = import_module(getattr(settings, "AITEO_WORKFLOW_MODULE", "aiteo.workflow"))


def question_list(request, **kwargs):
    
    group, bridge = group_and_bridge(kwargs)
    
    questions = Question.objects.all().order_by("-score", "created", "id")
    
    if group:
        questions = group.content_objects(questions)
    else:
        questions = questions.filter(group_content_type=None)
    
    ctx = group_context(group, bridge)
    ctx.update({
        "group": group,
        "questions": questions,
    })
   # take care of ctx 
    ctx = RequestContext(request, ctx)
    return render_to_response("aiteo/question_list.html", ctx)


def question_create(request, **kwargs):
    
    group, bridge = group_and_bridge(kwargs)
    
    if request.method == "POST":
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            #question.user = request.user
            question.save()
            print "amit ", question.get_absolute_url()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = AskQuestionForm()
    
    ctx = group_context(group, bridge)
    ctx.update({
        "group": group,
        "form": form,
    })
    
    #ctx = RequestContext(request, ctx)
    return render_to_response("aiteo/question_create.html", {'form': form}, context_instance=RequestContext(request))


def question_detail(request, question_id, **kwargs):
    group, bridge = group_and_bridge(kwargs)
    
    questions = Question.objects.all()
    
    if group:
        questions = group.content_objects(questions)
    else:
        questions = questions.filter(group_content_type=None)
    
    question = get_object_or_404(questions, pk=question_id)
    responses = question.responses.order_by("-score", "created", "id")
    #if question.user == request.user:
    #    is_me = True
    #else:
    is_me = False
    
    if request.method == "POST":
        add_response_form = AddResponseForm(request.POST)
        if add_response_form.is_valid():
            response = add_response_form.save(commit=False)
            response.question = question
            #response.user = request.user
            response.save()
            return HttpResponseRedirect(response.get_absolute_url())
    else:
        #if not is_me or request.user.is_staff:
        add_response_form = AddResponseForm()
        #else:
         #   add_response_form = None
    
    ctx = group_context(group, bridge)
    ctx.update({
        "group": group,
        "can_mark_accepted": workflow.can_mark_accepted(request.user, question),
        "question": question,
        "responses": responses,
        "add_response_form": add_response_form,
    })
    
    ctx = RequestContext(request, ctx)
    return render_to_response("aiteo/question_detail.html", ctx)

def vote_on(request, object1, object_id, direction):
    print object1, object_id, direction
    [q_id, a_id] = object_id.split("_")
    print q_id, a_id
    if object1 == "vote-question":
        question = Question.objects.get(pk = q_id)
        if direction == "up":
            question.vote_up_count = question.vote_up_count + 1
            question.save()
            return HttpResponse(question.vote_up_count)
        else:
            question.vote_down_count = question.vote_down_count - 1
            question.save()
            return HttpResponse(question.vote_down_count)
    else:
        question = Question.objects.get(pk = q_id)
        response = question.responses.get(pk = a_id)
        if direction == "up":
            response.vote_up_count = response.vote_up_count + 1
            response.save()
            return HttpResponse(response.vote_up_count)
        else:
            response.vote_down_count = response.vote_down_count - 1
            response.save()
            return HttpResponse(response.vote_down_count)
    #return render_to_response("aiteo/question_detail.html")
#    return HttpResponseRedirect("/aiteo/question/"+object_id)
            


def mark_accepted(request, question_id, response_id, **kwargs):
    
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    group, bridge = group_and_bridge(kwargs)
    
    questions = Question.objects.all()
    
    if group:
        questions = group.content_objects(questions)
    else:
        questions = questions.filter(group_content_type=None)
    
    question = get_object_or_404(questions, pk=question_id)
    
    if not workflow.can_mark_accepted(request.user, question):
        return HttpResponseForbidden("You are not allowed to mark this question accepted.")
    
    response = question.responses.get(pk=response_id)
    response.accept()
    
    return HttpResponse("good")
