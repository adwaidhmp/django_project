from django.urls import path
from . import views

urlpatterns = [
    path('', views.std_view, name='std_view'),       
    path('add/', views.std_add, name='std_add'),        
    path('edit/<int:pk>/', views.std_edit, name='std_edit'),  
    path('delete/<int:pk>/', views.std_delete, name='std_delete'), 
    path('dept_add',views.department_add, name='department'),
    path('dept_add/edit/<int:dept_id>/', views.edit_department, name='edit_department'),
    path('dept_add/delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path("courses/", views.course_manage, name="course_manage"),
    path("courses/<int:course_id>/edit/", views.course_edit, name="course_edit"),
    path("courses/<int:course_id>/delete/", views.course_delete, name="course_delete"),
    path('course-requests/', views.manage_course_requests, name='manage_course_requests'),
    path('course-requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('course-requests/reject/<int:request_id>/', views.reject_request, name='reject_request'),
]
