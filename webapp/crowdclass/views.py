from django.http import Http404
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader
from .models import Elliptical, Spiral, Edge, Bulge, Bar, Merging, Dust, Lens, Tidal, UserSession, PrePostTest, Participant, EdgeDescription, BulgeDescription, BarDescription, MergingDescription, DustDescription, LensDescription, TidalDescription, EllipticalDescription, SpiralDescription, Introduction
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone

from random import randint
import random

# Global variables

#Threshold for transitioning to the next level
THRES_MEDIUM = 21 # max=23
THRES_HARD  =  20 # max=22

IMAGE_LIST = range(1,99)
r = 0.5
random.shuffle(IMAGE_LIST, lambda: r)

DURATION = 30 # in minutes

def timesup(request):
    return render(request, 'crowdclass/timesup.html')

def create_user(request):
    try:
        uid = int(request.POST['uid'])
        new = User.objects.create_user('%d' % uid,'%d@gmail.com' % uid,'%d' % uid)
        new.save()
    except:
        return render(request, 'crowdclass/index.html', {'error_message': "Please only enter the number given to you.",})
    
    user = authenticate(username=new.username, password=new.username)

    participant = Participant(user=user)
    participant.save()

    
    login(request,user)
    pretestSession = PrePostTest(user=user)
    pretestSession.save()


    qid = randint(0,9)
    context = {'qid':qid}
    return render(request, 'crowdclass/pretest%d.html' % qid, context)

def introduction(request):
    current_user = request.user

    pids = []

    for u in UserSession.objects.all().filter(user=current_user):
        pids.append(u.image)

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.count += 1
    participant.save()

    new_image = IMAGE_LIST[participant.count]

    session = UserSession(user=current_user, image = new_image, difficulty= participant.level)
    session.save()

    pic = "crowdclass/images/%d.png" % session.image


    
    try:
        intro = Introduction.objects.all().filter(difficulty=participant.level)[participant.introduction_count]
    except:
        pass


    # all the questions
    if participant.level == 2:
        questions = Elliptical.objects.all().filter(difficulty=1)    
    else:
        questions = Elliptical.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    if participant.level == 0:
        if participant.introduction_count >= 2:
            if participant.elliptical_count >= 5:
                context = {'elliptical':question,'pic': pic, 'pid':session.image}
                return render(request, 'crowdclass/elliptical.html', context)
            else:
                participant.elliptical_count += 1
                participant.save()
                description = EllipticalDescription.objects.get(id=participant.elliptical_count)
                image = "crowdclass/images/elliptical_%d.png" % description.image
                context = {'elliptical':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
                return render(request, 'crowdclass/elliptical_description.html', context)
        else:
            participant.introduction_count += 1
            participant.save()
            session.introduction_description_time = timezone.now()
            session.save()
            if participant.elliptical_count >= 5:
                image = "crowdclass/images/easy_%d.png" % intro.image
                context = {'elliptical':question,'image': image, 'caption':intro.caption,'heading':intro.heading,'description_text_1':intro.description_text_1, 'description_text_2':intro.description_text_2,'description_text_3':intro.description_text_3,'pid':session.image}
                return render(request, 'crowdclass/introduction.html', context)
            else:
                image = "crowdclass/images/easy_%d.png" % intro.image
                context = {'elliptical':question,'image': image,'diverge':True, 'caption':intro.caption,'heading':intro.heading,'description_text_1':intro.description_text_1, 'description_text_2':intro.description_text_2,'description_text_3':intro.description_text_3,'pid':session.image}
                return render(request, 'crowdclass/introduction.html', context)
    elif participant.level == 1:
        if participant.introduction_count >= 1:
            context = {'elliptical':question,'pic': pic, 'pid':session.image}
            return render(request, 'crowdclass/elliptical.html', context)
        else:
            participant.introduction_count += 1
            participant.save()
            session.introduction_description_time = timezone.now()
            session.save()
            image = "crowdclass/images/medium_%d.png" % intro.image
            context = {'elliptical':question,'image': image, 'caption':intro.caption,'heading':intro.heading,'description_text_1':intro.description_text_1, 'description_text_2':intro.description_text_2,'description_text_3':intro.description_text_3,'pid':session.image}
            return render(request, 'crowdclass/introduction.html', context)
    else:
        if participant.introduction_count >= 1:
            context = {'elliptical':question,'pic': pic, 'pid':session.image}
            return render(request, 'crowdclass/elliptical.html', context)
        else:
            participant.introduction_count += 1
            participant.save()
            session.introduction_description_time = timezone.now()
            session.save()
            image = "crowdclass/images/hard_%d.png" % intro.image
            context = {'elliptical':question,'image': image, 'caption':intro.caption,'heading':intro.heading,'description_text_1':intro.description_text_1, 'description_text_2':intro.description_text_2,'description_text_3':intro.description_text_3,'pid':session.image}
            return render(request, 'crowdclass/introduction.html', context)

# Randomly shuffles and proceeds with the pretest questions.
def pretest(request, pretest_id):
    current_user = request.user
    preSession = PrePostTest.objects.all().filter(user=current_user)[0]
    try:
        answer = request.POST['choice']
    except:
        return render(request, 'crowdclass/pretest%d.html' % int(pretest_id), {'qid':int(pretest_id),
            'error_message': "Please select a choice.",
        })
    if pretest_id == "0":
        preSession.pre_scheme = answer
        preSession.pre_scheme_time = timezone.now()
    elif pretest_id == "1":
        preSession.pre_elliptical = answer
        preSession.pre_elliptical_time = timezone.now()
    elif pretest_id == "2":
        preSession.pre_mergers = answer
        preSession.pre_mergers_time = timezone.now()
    elif pretest_id == "3":
        preSession.pre_tidal = answer
        preSession.pre_tidal_time = timezone.now()
    elif pretest_id == "4": 
        preSession.pre_lens = answer
        preSession.pre_lens_time = timezone.now()
    elif pretest_id == "5": 
        preSession.pre_dust = answer
        preSession.pre_dust_time = timezone.now()
    elif pretest_id == "6": 
        preSession.pre_properties = answer
        preSession.pre_properties_time = timezone.now()
    elif pretest_id == "7":   
        preSession.pre_bulges = answer
        preSession.pre_bulges_time = timezone.now()
    elif pretest_id == "8":   
        preSession.pre_not = answer
        preSession.pre_not_time = timezone.now()
    else:
        preSession.pre_formation = answer
        preSession.pre_formation_time = timezone.now()   

    preSession.pre_count += 1 
    preSession.save()

    if preSession.pre_count ==10:
        current_user = request.user
        participant = Participant.objects.all().filter(user=current_user)[0]
        context = {'level':participant.level}
        return render(request, 'crowdclass/transition.html',context)

    else:
        dic = {"0":preSession.pre_scheme, "1":preSession.pre_elliptical, "2":preSession.pre_mergers, "3":preSession.pre_tidal, "4":preSession.pre_lens, "5":preSession.pre_dust, "6":preSession.pre_properties, "7":preSession.pre_bulges, "8":preSession.pre_not, "9":preSession.pre_formation}
        qid = randint(0,9)
        while dic[str(qid)] != "empty":
            qid = randint(0,9)
        context = {'qid':qid}
        return render(request, 'crowdclass/pretest%d.html' % qid, context)

# Randomly shuffles and proceeds with the post test questions.
def posttest(request, posttest_id):
    current_user = request.user
    postSession = PrePostTest.objects.all().filter(user=current_user)[0]
    if posttest_id != "99":
        try:
            answer = request.POST['choice']
        except:
            return render(request, 'crowdclass/posttest%d.html' % int(posttest_id), {'qid':int(posttest_id),
                'error_message': "Please select a choice.",
            })
        if posttest_id == "0":
            postSession.post_scheme = answer
            postSession.post_scheme_time = timezone.now()
        elif posttest_id == "1":
            postSession.post_elliptical = answer
            postSession.post_elliptical_time = timezone.now()
        elif posttest_id == "2":
            postSession.post_mergers = answer
            postSession.post_mergers_time = timezone.now()
        elif posttest_id == "3":
            postSession.post_tidal = answer
            postSession.post_tidal_time = timezone.now()
        elif posttest_id == "4": 
            postSession.post_lens = answer
            postSession.post_lens_time = timezone.now()
        elif posttest_id == "5": 
            postSession.post_dust = answer
            postSession.post_dust_time = timezone.now()
        elif posttest_id == "6": 
            postSession.post_properties = answer
            postSession.post_properties_time = timezone.now()
        elif posttest_id == "7":   
            postSession.post_bulges = answer
            postSession.post_bulges_time = timezone.now()
        elif posttest_id == "8":   
            postSession.post_not = answer
            postSession.post_not_time = timezone.now()
        elif posttest_id == "9":
            postSession.post_formation = answer
            postSession.post_formation_time = timezone.now()   

        postSession.post_count += 1 
        postSession.save()

        if postSession.post_count == 10:
            postSession.end_time = timezone.now()
            postSession.save()
            return render(request, 'crowdclass/final.html')

        else:
            dic = {"0":postSession.post_scheme, "1":postSession.post_elliptical, "2":postSession.post_mergers, "3":postSession.post_tidal, "4":postSession.post_lens, "5":postSession.post_dust, "6":postSession.post_properties, "7":postSession.post_bulges, "8":postSession.post_not, "9":postSession.post_formation}
            qid = randint(0,9)
            while dic[str(qid)] != "empty":
                qid = randint(0,9)
            context = {'qid':qid}
            return render(request, 'crowdclass/posttest%d.html' % qid, context)
    qid = randint(0,9)
    context = {'qid':qid}
    return render(request, 'crowdclass/posttest%d.html' % qid, context)

def restart(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.restart = timezone.now()
    session.restart_count += 1
    session.save()
    
    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')
    participant = Participant.objects.all().filter(user=current_user)[0]

    if participant.level == 2:
        questions = Elliptical.objects.all().filter(difficulty=1)    
    else:
        questions = Elliptical.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    pic = "crowdclass/images/%d.png" % session.image
    context = {'elliptical':question,'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/elliptical.html', context)

# def to_(example): are for the transition from its respective description page to the question/classfication page.
# def (example): leads to either 1. the description page of a following class or 2. lead directly to another class

def to_elliptical(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.elliptical_description_time = timezone.now()
    session.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += EllipticalDescription.objects.all()[0].score
    # participant.elliptical_count += 1
    participant.save()

    if participant.level == 2:
        questions = Elliptical.objects.all().filter(difficulty=1)   
    else:
        questions = Elliptical.objects.all().filter(difficulty=participant.level) 
    question = random.choice(questions)

    pic = "crowdclass/images/%d.png" % session.image

    context = {'elliptical':question, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/elliptical.html', context)

def elliptical(request, question_id, pid):
    current_user = request.user

    try:
        choice = request.POST['choice']
    except:
        pass
        choice = "none"

    answer = Elliptical.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"

    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.elliptical_correct = 1;
    else:
        session.elliptical_correct = -1;
    session.elliptical_time = timezone.now()
    session.elliptical_question_id = question_id
    session.elliptical_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image
    if choice == "yes":
        if participant.level == 2:
            questions = Dust.objects.all().filter(difficulty=participant.level)
            question = random.choice(questions) 
            if participant.dust_count < 3:
                participant.dust_count += 1
                participant.save()
                description = DustDescription.objects.get(id=participant.dust_count)
                image = "crowdclass/images/dust_%d.png" % description.image
                context = {'dust':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
                return render(request, 'crowdclass/dust_description.html', context)

            context = {'dust':question,'pic': pic, 'pid':session.image}
            return render(request, 'crowdclass/dust.html', context)
        else:
            if participant.level == 0 and participant.score >= THRES_MEDIUM or participant.level == 1 and participant.score >= THRES_HARD:#boundary hard medium
                participant.level += 1
                participant.score = 0
                participant.introduction_count = 0
                participant.save()
                session.end_time = timezone.now()
                session.save()
                context = {'level':participant.level}
                return render(request, 'crowdclass/transition.html',context)
            return introduction(request)
    else:

        if participant.level == 0:
            questions = Edge.objects.all().filter(difficulty=participant.level)
            question = random.choice(questions)
            if participant.edge_count >= 1:
                context = {'edge':question,'pic': pic, 'pid':session.image}
                return render(request, 'crowdclass/edge.html', context)

            participant.edge_count += 1
            participant.save()
            description = EdgeDescription.objects.get(id=participant.edge_count)
            image = "crowdclass/images/edge_%d.png" % description.image
            context = {'edge':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
            return render(request, 'crowdclass/edge_description.html', context)

        questions = Bulge.objects.all()
        question = random.choice(questions)
        if participant.level == 1:
            
            if participant.bulge_count >= 3:
                context = {'bulge':question,'pic': pic, 'pid':session.image}
                return render(request, 'crowdclass/bulge.html', context) 

            participant.bulge_count += 1
            participant.save()
            description = BulgeDescription.objects.get(id=participant.bulge_count)
            image = "crowdclass/images/bulge_%d.png" % description.image
            context = {'bulge':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
            return render(request, 'crowdclass/bulge_description.html', context) 

        context = {'bulge':question,'pic': pic, 'pid':session.image}
        return render(request, 'crowdclass/bulge.html', context) 


def to_bulge(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.bulge_description_time = timezone.now()


    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += BulgeDescription.objects.all()[0].score
    session.score += BulgeDescription.objects.all()[0].score
    session.save()
    # participant.bulge_count += 1
    participant.save()
    

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    questions = Bulge.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    # question_id = randint(0,0)

    context = {'bulge':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/bulge.html', context)

def bulge(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Bulge.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.bulge_correct = 1;
    else:
        session.bulge_correct = -1;
    session.bulge_time = timezone.now()
    session.bulge_question_id = question_id
    session.bulge_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image  
    questions = Edge.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)
    context = {'edge':question,'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/edge.html', context)

def to_edge(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.edge_description_time = timezone.now()
    

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += EdgeDescription.objects.all()[0].score
    session.score += EdgeDescription.objects.all()[0].score
    session.save()
    # participant.edge_count += 1
    participant.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    # question_id = randint(0,0)
    questions = Edge.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    context = {'edge':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/edge.html', context)

def edge(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Edge.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.edge_correct = 1;
    else:
        session.edge_correct = -1;
    session.edge_time = timezone.now()
    session.edge_question_id = question_id
    session.edge_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image
    if choice == "yes":  
        if participant.level == 2:
            questions = Dust.objects.all().filter(difficulty=participant.level)
            question = random.choice(questions)
            if participant.dust_count >= 3:
                context = {'dust':question,'pic': pic, 'pid':session.image}
                return render(request, 'crowdclass/dust.html', context)

            participant.dust_count += 1
            participant.save()
            description = DustDescription.objects.get(id=participant.dust_count)
            image = "crowdclass/images/dust_%d.png" % description.image
            context = {'dust':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
            return render(request, 'crowdclass/dust_description.html', context)

        if participant.level == 0 and participant.score >= THRES_MEDIUM or participant.level == 1 and participant.score >= THRES_HARD:#boundary hard medium
            participant.level += 1
            participant.score = 0
            participant.introduction_count = 0  
            participant.save()
            session.end_time = timezone.now()
            session.save()
            context = {'level':participant.level}
            return render(request, 'crowdclass/transition.html',context)
        return introduction(request)
    else:
        if participant.level == 2:
            questions = Bar.objects.all().filter(difficulty=1)
        else:
            questions = Bar.objects.all().filter(difficulty=participant.level)    
        question = random.choice(questions)
        if participant.level == 0 and participant.bar_count >= 1 or participant.level >= 1:
            context = {'bar':question,'pic': pic, 'pid':session.image}
            return render(request, 'crowdclass/bar.html', context)
        participant.bar_count += 1
        participant.save()
        description = BarDescription.objects.get(id=participant.bar_count)
        image = "crowdclass/images/bar_%d.png" % description.image
        context = {'bar':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
        return render(request, 'crowdclass/bar_description.html', context)

def to_bar(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.bar_description_time = timezone.now()
    

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += BarDescription.objects.all()[0].score
    session.score += BarDescription.objects.all()[0].score
    session.save()
    # participant.bar_count += 1
    participant.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    # question_id = randint(0,0)
    questions = Bar.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    context = {'bar':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/bar.html', context)

def bar(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Bar.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.bar_correct = 1;
    else:
        session.bar_correct = -1;
    session.bar_time = timezone.now()
    session.bar_question_id = question_id
    session.bar_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    questions = Spiral.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    pic = "crowdclass/images/%d.png" % session.image
    if participant.level > 0 or participant.level == 0 and participant.spiral_count >= 3:
        context = {'spiral':question,'pic': pic, 'pid':session.image}
        return render(request, 'crowdclass/spiral.html', context)   
    participant.spiral_count += 1
    participant.save()
    description = SpiralDescription.objects.get(id=participant.spiral_count)
    image = "crowdclass/images/spiral_%d.png" % description.image
    context = {'spiral':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
    return render(request, 'crowdclass/spiral_description.html', context) 

def to_spiral(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.spiral_description_time = timezone.now()
    

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += SpiralDescription.objects.all()[0].score
    session.score += SpiralDescription.objects.all()[0].score
    session.save()
    # participant.spiral_count += 1
    participant.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    # question_id = randint(0,0)
    questions = Bar.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    context = {'spiral':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/spiral.html', context)

def spiral(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Spiral.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.spiral_correct = 1;
    else:
        session.spiral_correct = -1;
    session.spiral_time = timezone.now()
    session.spiral_question_id = question_id
    session.spiral_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image
    if participant.level == 0:
        if participant.score >= THRES_MEDIUM:#boundary medium
            participant.level += 1
            participant.score = 0
            participant.introduction_count = 0  
            participant.save()
            session.end_time = timezone.now()
            session.save()
            context = {'level':participant.level}
            return render(request, 'crowdclass/transition.html',context)
        return introduction(request)
        # context = {'elliptical':Elliptical.objects.get(id=question_id),'pic': pic, 'pid':session.image}
        # return render(request, 'crowdclass/elliptical.html', context)
    questions = Tidal.objects.all()
    question = random.choice(questions)
    if participant.level == 2 or participant.tidal_count >= 2:
        context = {'tidal':question,'pic': pic, 'pid':session.image}
        return render(request, 'crowdclass/tidal.html', context)

    participant.tidal_count += 1
    participant.save()
    description = TidalDescription.objects.get(id=participant.tidal_count)
    image = "crowdclass/images/tidal_%d.png" % description.image
    context = {'tidal':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
    return render(request, 'crowdclass/tidal_description.html', context)

def to_tidal(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.tidal_description_time = timezone.now()
    

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += TidalDescription.objects.all()[0].score
    session.score += TidalDescription.objects.all()[0].score
    session.save()
    # participant.tidal_count += 1
    participant.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    # question_id = randint(0,0)
    questions = Tidal.objects.all()
    question = random.choice(questions)

    context = {'tidal':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/tidal.html', context)

def tidal(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Tidal.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.tidal_correct = 1;
    else:
        session.tidal_correct = -1;
    session.tidal_time = timezone.now()
    session.tidal_question_id = question_id
    session.tidal_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    questions = Merging.objects.all()
    question = random.choice(questions)

    pic = "crowdclass/images/%d.png" % session.image
    if participant.merging_count >= 2 or participant.level == 2:
        context = {'merging':question,'pic': pic, 'pid':session.image}
        return render(request, 'crowdclass/merging.html', context)

    participant.merging_count += 1
    participant.save()
    description = MergingDescription.objects.get(id=participant.merging_count)
    image = "crowdclass/images/merging_%d.png" % description.image
    context = {'merging':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
    return render(request, 'crowdclass/merging_description.html', context)

def to_merging(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.merging_description_time = timezone.now()
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += MergingDescription.objects.all()[0].score
    session.score += MergingDescription.objects.all()[0].score
    session.save()
    # participant.merging_count += 1
    participant.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    # question_id = randint(0,0)
    questions = Merging.objects.all()
    question = random.choice(questions)

    context = {'merging':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/merging.html', context)

def merging(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Merging.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.merging_correct = 1;
    else:
        session.merging_correct = -1;
    session.merging_time = timezone.now()
    session.merging_question_id = question_id
    session.merging_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image    
    if participant.level == 1:
        if participant.score >= THRES_HARD:#boundary hard
            participant.level += 1
            participant.score = 0
            participant.introduction_count = 0
            participant.save()
            session.end_time = timezone.now()
            session.save()
            context = {'level':participant.level}
            return render(request, 'crowdclass/transition.html',context)
        # context = {'elliptical':Elliptical.objects.get(id=question_id),'pic': pic, 'pid':session.image}
        # return render(request, 'crowdclass/elliptical.html', context)
        return introduction(request)
    questions = Dust.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)
    if participant.dust_count >= 3:
        context = {'dust':question,'pic': pic, 'pid':session.image}
        return render(request, 'crowdclass/dust.html', context)

    participant.dust_count += 1
    participant.save()
    description = DustDescription.objects.get(id=participant.dust_count)
    image = "crowdclass/images/dust_%d.png" % description.image
    context = {'dust':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
    return render(request, 'crowdclass/dust_description.html', context)

def to_dust(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.dust_description_time = timezone.now()
    

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += DustDescription.objects.all()[0].score
    session.score += DustDescription.objects.all()[0].score
    session.save()
    # participant.dust_count += 1
    participant.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    # question_id = randint(0,0)
    questions = Dust.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    context = {'dust':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/dust.html', context)

def dust(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Dust.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.dust_correct = 1;
    else:
        session.dust_correct = -1;
    session.dust_time = timezone.now()
    session.dust_question_id = question_id
    session.dust_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    questions = Lens.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    pic = "crowdclass/images/%d.png" % session.image
    if participant.lens_count >= 3:
        context = {'lens':question,'pic': pic, 'pid':session.image}
        return render(request, 'crowdclass/lens.html', context) 

    participant.lens_count += 1
    participant.save()
    description = LensDescription.objects.get(id=participant.lens_count)
    image = "crowdclass/images/lens_%d.png" % description.image
    context = {'lens':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
    return render(request, 'crowdclass/lens_description.html', context)

def to_lens(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.lens_description_time = timezone.now()
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]
    participant.score += LensDescription.objects.all()[0].score
    session.score += LensDescription.objects.all()[0].score
    session.save()
    # participant.lens_count += 1
    participant.save()

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image

    # question_id = randint(0,0)
    questions = Lens.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    context = {'lens':question, 'question_id':question_id, 'pic': pic, 'pid':session.image}
    return render(request, 'crowdclass/lens.html', context)

def lens(request, question_id, pid):
    current_user = request.user
    try:
        choice = request.POST['choice']
    except:
        choice = "none"
    answer = Lens.objects.get(id=question_id).answer
    if not answer:
        if choice == "yes":
            choice = "no"
        else:
            choice = "yes"
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if choice == "yes":
        session.lens_correct = 1;
    else:
        session.lens_correct = -1;
    session.lens_time = timezone.now()
    session.lens_question_id = question_id
    session.lens_choice = choice
    session.save()

    participant = Participant.objects.all().filter(user=current_user)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    pic = "crowdclass/images/%d.png" % session.image
    # context = {'elliptical':Elliptical.objects.get(id=question_id),'pic': pic, 'pid':session.image}
    # return render(request, 'crowdclass/elliptical.html', context)
    print participant.level
    return introduction(request)

def to_elliptical_description(request, question_id, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]

    if (timezone.now()-current_user.date_joined).seconds/60 >= DURATION:
        return render(request, 'crowdclass/timesup.html')

    participant = Participant.objects.all().filter(user=current_user)[0]
    questions = Elliptical.objects.all().filter(difficulty=participant.level)
    question = random.choice(questions)

    participant.elliptical_count += 1
    participant.save()
    description = EllipticalDescription.objects.get(id=participant.elliptical_count)
    image = "crowdclass/images/elliptical_%d.png" % description.image
    # print image
    context = {'elliptical':question,'image': image, 'caption':description.caption,'description':description.description_text, 'pid':session.image}
    return render(request, 'crowdclass/elliptical_description.html', context)

def hint(request, qid, dest, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    if dest == "elliptical":
        question = Elliptical.objects.get(id=qid)
        session.elliptical_hint = True
    elif dest == "spiral":
        question = Spiral.objects.get(id=qid)
        session.spiral_hint = True
    elif dest == "edge":
        question = Edge.objects.get(id=qid)
        session.edge_hint = True
    elif dest == "bulge":
        question = Bulge.objects.get(id=qid)
        session.bulge_hint = True
    elif dest == "bar":
        question = Bar.objects.get(id=qid)
        session.bar_hint = True
    elif dest == "merging":
        question = Merging.objects.get(id=qid)
        session.merging_hint = True
    elif dest == "dust":
        question = Dust.objects.get(id=qid)
        session.dust_hint = True
    elif dest == "lens":
        question = Lens.objects.get(id=qid)
        session.lens_hint = True
    elif dest == "tidal":
        question = Tidal.objects.get(id=qid)
        session.tidal_hint = True
    session.save()
    context = {'hint':question.hint}
    return render(request, 'crowdclass/hint.html',context)

def ex_parents(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.parent_example = True
    session.save()
    return render(request, 'crowdclass/ex_parents.html')

def ex_round(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.round_example = True
    session.save()
    return render(request, 'crowdclass/ex_round.html')

def ex_edge(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.edge_example = True
    session.save()
    return render(request, 'crowdclass/ex_edge.html')

def ex_bulge(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.bulge_example = True
    session.save()
    return render(request, 'crowdclass/ex_bulge.html')

def ex_bar(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.bar_example = True
    session.save()
    return render(request, 'crowdclass/ex_bar.html')

def ex_pattern(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.pattern_example = True
    session.save()
    return render(request, 'crowdclass/ex_pattern.html')

def ex_sa(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.sa_example = True
    session.save()
    return render(request, 'crowdclass/ex_sa.html')

def ex_sanum(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.sa_num_example = True
    session.save()
    return render(request, 'crowdclass/ex_sanum.html')

def ex_prominence(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.prominence_example = True
    session.save()
    return render(request, 'crowdclass/ex_prominence.html')

def ex_tidal(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.tidal_example = True
    session.save()
    return render(request, 'crowdclass/ex_tidal.html')

def ex_odd(request, pid):
    current_user = request.user
    session = UserSession.objects.all().filter(user=current_user, image=pid)[0]
    session.odd_example = True
    session.save()
    return render(request, 'crowdclass/ex_odd.html')



