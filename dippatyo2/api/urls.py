from django.urls import path
from . import views

urlpatterns = [
    path('api/sample/', views.SampleListCreate.as_view()),
    path('api/fileupload/', views.FileUploadView.as_view()),
    path('api/word/<slug:word>/', views.SingleWordView.as_view()),
    path('api/word/', views.WordView.as_view()),
    path('api/wordrelation/', views.AllWordRelations.as_view()),
    path('api/wordrelation/<slug:word1>/', views.WordRelationView.as_view()),
    path('api/scan/', views.Scan.as_view()),
]
