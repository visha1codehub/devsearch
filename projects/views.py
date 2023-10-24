from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

# Create your views here.
def home(request):
    projects, search_query = searchProjects(request)
    projects, custome_range = paginateProjects(request, projects, 6)
        
    context = {'projects':projects, 'search_query':search_query, 'custome_range':custome_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            
            project.getVoteCount
            
            messages.success(request, "Your review was successfully submitted.")
            return redirect('project', pk)
    context = {'project':project, 'form':form}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    newtags = request.POST.get('newtags').replace(',', ' ').split()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag. objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project) 
    # stringTags = ",  ".join([str(tag) for tag in project.tags.all()])  #$ just playing......
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form':form, 'project':project}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object':project}
    return render(request, 'delete.html', context)