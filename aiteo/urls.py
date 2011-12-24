from django.conf.urls.defaults import *

from aiteo.models import Question, Response


urlpatterns = patterns("",
    url(r"^$",
        "aiteo.views.question_list",
        name="aiteo_question_list"
    ),
    url(r"^ask/$",
        "aiteo.views.question_create",
        name="aiteo_question_create"
    ),
    url(r"^question/(?P<question_id>\d+)/$",
        "aiteo.views.question_detail",
        name="aiteo_question_detail"
    ),
    url(r"^question/(?P<question_id>\d+)/accept/(?P<response_id>\d+)/$",
        "aiteo.views.mark_accepted",
        name="aiteo_mark_accepted"
    ),
    
    # Question voting
    url(r"^question/(?P<object1>vote-\w+)/(?P<object_id>\w+)/(?P<direction>up|down|clear)vote/$",
        "aiteo.views.vote_on", 
        name="aiteo_question_vote"
    ),
    
    # Response voting
    url(r"^question/vote-response/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/$",
        "aiteo.views.vote_on", dict(
            model = Response,
            template_object_name = "object",
            template_name = "questions/confirm_vote.html",
            allow_xmlhttprequest = True
        ),
        name="aiteo_response_vote"
    ),
)
