from django.shortcuts import render

# Create your views here.
#from celery import registry
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


import forms
# Create your views here.

@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        data = request.POST
        form = forms.ChangePasswordForm(data)
        if form.is_valid():
            task_id = form.save()
            # url = 'http://ops.lab.hollow.pt:5555/task/' + task_id
            url = 'http://localhost:5555/task/' + task_id
            return HttpResponseRedirect(url)

            #return render_to_response(
            #    'change_password_form.html',
            #    {'form': form, 'task_id': task_id}
            #)
    else:
        form = forms.ChangePasswordForm()
    return render_to_response('change_password_form.html', {'form': form})


from .models import TaskState, TaskMeta, WorkerState
from rest_framework import viewsets
from .serializers import (TaskStateSerializer, TaskMetaSerializer,
                          WorkerStateSerializer)
class TaskStateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TaskState objects to be viewed.
    """
    queryset = TaskState.objects.all()
    serializer_class = TaskStateSerializer
    # lookup_field = 'task_id'

    # class Meta:
    #     exclude = ('worker',)


class WorkerStateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows WorkerState objects to be viewd.
    """
    queryset = WorkerState.objects.all()
    serializer_class = WorkerStateSerializer


class TaskMetaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TaskMeta objects to be viewed.
    """
    queryset = TaskMeta.objects.all()
    serializer_class = TaskMetaSerializer
