from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.UserSerializerAPIView.as_view()),
    path('', views.LoginAPIView.as_view()),
    path('api/token/', views.Generate_access_token),
    path('api/token/refresh/', views.Generate_refresh_token),
    path('zone/', views.ZoneAPIView.as_view()),
    path('showzone/', views.ShowzoneAPIView.as_view()),
    path('notification/<int:zone_id>', views.NotificationAPIView.as_view()),
    path('shownoitification/', views.ShowNotificatoinAPIView.as_view()),
    path('acceptreject/<int:notification_id>',
         views.AcceptRejectAPIView.as_view()),
    path('showrequest/', views.ShowrequestAPIView.as_view()),
    path('sendemail/', views.SendEmailAPIVIew.as_view()),
    path('activity/', views.ActivityAPIView.as_view()),
    path('showactivity/', views.ShowActivityAPIView.as_view()),
    path('score/<int:id>', views.ScoreAPIView.as_view()),
    path('showscore/<int:id>', views.ShowScoreAPIView.as_view()),
    path("show-package/",views.GetPackageView.as_view()),
    path('package/', views.PackageAPIView.as_view()),
    path('Purchasepackage/', views.PurchasepackageAPIView.as_view()),
    path('Purchasepackage/<int:id>', views.PurchasepackageAPIView.as_view()),
    path('invitation/', views.InvitationAPIView.as_view()),
    path('addition-register/<int:id>', views.AdditionalAPIView.as_view()),
    

]
