from django.urls import path
from . import views

urlpatterns = [
    path('', views.BatchListView.as_view(), name='home'),
    path('upcomming-batches', views.get_upcoming_batches, name='upcomming_batches'),
    path('mark_batches_notified', views.mark_notified, name='mark_batch_times_notified'),
    path('batches/', views.BatchListView.as_view(), name='batches'),
    path('batches/create/', views.BatchCreateView.as_view(), name='batch-create'),
    path('batches/<int:pk>/update/', views.BatchUpdateView.as_view(), name='batch-update'),
    path('batches/<int:pk>/delete/', views.BatchDeleteView.as_view(), name='batch-delete'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    path('instructors/', views.InstructorListView.as_view(), name='instructors'),
    path('instructors/create/', views.InstructorCreateView.as_view(), name='instructor-create'),
    path('instructors/<int:pk>/update/', views.InstructorUpdateView.as_view(), name='instructor-update'),
    path('instructors/<int:pk>/delete/', views.InstructorDeleteView.as_view(), name='instructor-delete'),
    path('parents/', views.ParentListView.as_view(), name='parents'),
    path('parents/create/', views.ParentCreateView.as_view(), name='parent-create'),
    path('parents/<int:pk>/update/', views.ParentUpdateView.as_view(), name='parent-update'),
    path('parents/<int:pk>/delete/', views.ParentDeleteView.as_view(), name='parent-delete'),
    path('students/', views.StudentListView.as_view(), name='students'),
    path('students/create/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
]
