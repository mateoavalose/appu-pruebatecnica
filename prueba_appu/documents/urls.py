from django.urls import path
from . import views

urlpatterns = [
    path('documents/create/', views.create_document_view, name='document_create'),
    path('documents/', views.document_list_view, name='document_list'),
    path('documents/<str:document_id>/delete/', views.document_delete_view, name='document_delete'),
]
