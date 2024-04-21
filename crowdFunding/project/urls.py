from project.views import (hello, create_project_model_form,
    list_project, cancel_project,project_show, donate_project, edit_project,
                            show_category)
from commentary.views import add_comment
from django.urls import path

urlpatterns = [
    path("hello", hello, name= "hello"),
    path('<int:id>/comment', add_comment, name='project.comment'),
    path('createproject', create_project_model_form, name='project.createmodel'),
    path('<int:id>', project_show, name='project.show'),
    path('cancelproject/<int:id>', cancel_project, name='project.cancel'),
    path('', list_project, name='project.list'),
    path('donate/<int:id>', donate_project, name='project.donate'),
    path('<int:id>/edit', edit_project, name='project.edit'),
    path('category/<int:id>/show', show_category, name='category.show'),

]