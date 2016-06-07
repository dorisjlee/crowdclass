from django.http import Http404
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader
from crowdclass.models import Question, Round, Edge, Bulge, Bar, Pattern, Sa, Sa_num, Prominence, Tidal, Odd, Parent, UserSession, PrePostTest
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone

from random import randint

class IndexView(generic.ListView):
    template_name = 'crowdclass/index.html'

class EllipticalView(generic.DetailView):
    model = Question
    template_name = 'crowdclass/elliptical.html'

class LensView(generic.DetailView):
    model = Lens
    template_name = 'crowdclass/lens.html'

class DustView(generic.DetailView):
    model = Dust
    template_name = 'crowdclass/dust.html'

class MergingView(generic.DetailView):
    model = Merging
    template_name = 'crowdclass/merging.html'

class TidalView(generic.DetailView):
    model = Tidal
    template_name = 'crowdclass/tidal.html'

class SpiralView(generic.DetailView):
    model = Spiral
    template_name = 'crowdclass/spiral.html'

class BarView(generic.DetailView):
    model = Bar
    template_name = 'crowdclass/bar.html'

class BulgeView(generic.DetailView):
    model = Bulge
    template_name = 'crowdclass/bulge.html'

class EdgeView(generic.DetailView):
    model = Edge
    template_name = 'crowdclass/edge.html'


def 