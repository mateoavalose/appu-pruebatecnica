from django.urls import path
from . import views

urlpatterns = [
    path('api/documents/', views.create_document_view, name='document_create'),
    path('api/documents/', views.document_list_view, name='document_list'),
    path('api/documents/<str:document_id>/', views.get_document_by_id, name='document_detail'),
    path('api/documents/<str:document_id>/', views.document_delete_view, name='document_delete'),
]
