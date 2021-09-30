from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.urls import reverse
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .fileUpload import handle_uploaded_file

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args,**kwargs)
    

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            
        context['search_input']= search_input

        return context
        
def upload_file(request, pk:int):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc=Task(archivos=request.FILES['docfile'])
            newdoc.save()
            
            return HttpResponseRedirect(reverse('base.views.upload_file'))
        else:
            form = UploadFileForm()
    
    documents = Task.objects.all()
    
    return render(request,'base/task_detail.html')



class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name='task'
    template_name = 'base/task_detail.html'
    
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['user','title','description','complete','Estatus','Departamento']
    success_url = reverse_lazy('tasks')
    
    #def form_invalid(self, form):
     #   form.instance.user = self.request.user
      #  return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['user','title','description','complete','Estatus','Departamento','archivos']
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name='task'
    success_url = reverse_lazy('tasks')
    
class TaskAllList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='tasks'
    template_name = 'base/task_all_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            
        context['search_input']= search_input

        return context