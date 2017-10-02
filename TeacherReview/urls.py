from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login',views.login ),
    url(r'review', views.review),
    url(r'process', views.process),
    url(r'skip', views.skip),
    url(r'cancel', views.cancel),

    url(r'set', views.set),
    url(r'printpdf', views.printpdf),
    url(r'dashboard', views.dash),
    
    url(r'logout', views.logout),
]

