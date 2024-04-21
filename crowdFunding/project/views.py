from django.shortcuts import render, redirect,get_object_or_404,reverse
from project.models import Project, Category,Picture
from project.forms import ProjectModelForm,CategoryModelForm,TagModelForm
from commentary.forms import CommentForm,ReportForm, ReplyForm
from project.models import Project , Donation
from project.forms import ProjectModelForm,CategoryModelForm,TagModelForm,DonationModelForm,PictureModelForm
from commentary.forms import CommentForm,ReportForm
from commentary.models import Comment
from django.db.models import F
from django.http import HttpResponseForbidden

from django.http import HttpResponse

def hello(request):
    print(request)
    return render(request, 'test.html', {'name': 'Hello'})



def create_project_model_form(request):
    if request.method == 'POST':
        form = ProjectModelForm(request.POST)        
        if form.is_valid():
            project = form.save(commit=False)
            project.project_owner = request.user
            project.save()

            # Save tags associated with the project
            form.save_m2m()

            # Save form_pic instances, associate them with the project
            for img in request.FILES.getlist('pic'):
                picture_instance = Picture(image=img, project=project)
                picture_instance.save()

            return redirect(project.show_url)  # Assuming there's a show_url method in your Project model
    else:
        form = ProjectModelForm()
        

    return render(request, 'project/forms/createmodel.html', {'form': form})






def show_category(request, id):
    category = Category.get_category_by_id(id)
    return render(request,'category/crud/show.html', context={"category": category})


def project_show(request,id):
    project = get_object_or_404(Project, pk=id)
    images = project.images.all()
    comments = project.comments.all()
    reports = project.reports.all()
    reviews_reply = project.comments.prefetch_related('replies')
    form = CommentForm()
    form2 = ReportForm()
    reply_form = ReplyForm()
    return render(request, "project/crud/show.html",
                context={"project": project,'images': images, 'comments': comments, 'reports': reports,
                         'form': form, 'form2': form2, "reply_form":reply_form, "reviews_reply":reviews_reply})

# def project_show(request,id):
#     project = get_object_or_404(Project, pk=id)
#     comments = Comment.objects.filter(project=project)
#     for comment in comments:
#         comment.stars = range(int(comment.rate))
#         comment.empty_stars = range(5 - int(comment.rate))
#
#     reports = project.reports.all()
#     form = CommentForm()
#     form2 = ReportForm()
#
#     return render(request, "project/crud/show.html",
#                   context={"project":project, 'comments': comments, 'reports': reports, 'form': form, 'form2': form2})
#


def cancel_project(request, id):
    project = get_object_or_404(Project, pk=id)
    
    # Check if the current user is the owner of the project
    if request.user == project.project_owner:
        total_target = project.total_target
        donation = project.current_donation
        if donation < total_target * 0.25:
            project.delete()
            return redirect(project.list_url)
        else:
            return HttpResponseForbidden("the donation is greter than 25%")
    else:
        # If the current user is not the owner, handle unauthorized access
        # For example, you can return a 403 Forbidden response or redirect to a different page
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
def list_project(request):
    projects = Project.objects.all()
    return render(request, 'project/crud/list.html', {'projects': projects})



def donate_project(request, id):
    project = get_object_or_404(Project, pk=id)
    if project.is_run_project() == False:
        return HttpResponseForbidden("the project is not run")
    
    
    if request.method == 'POST':
        form = DonationModelForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.project = project
            donation.user = request.user
            donation.save()
            
            # Increase the current donation for the project
            project.current_donation += donation.donation
            project.save()
            # Redirect to project details page or any other desired page
            return redirect(project.show_url, id=id)  

    else:
        form = DonationModelForm()

    return render(request, 'project/crud/donate.html', {'form': form, 'project': project})




def edit_project(request, id):
    project=Project.get_project_by_id(id)
    form=ProjectModelForm(instance=project)
    if request.method == "POST":
        form=ProjectModelForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project=form.save()
            return redirect(project.show_url)

    return render (request,'project/crud/edit.html', context={"form":form})

