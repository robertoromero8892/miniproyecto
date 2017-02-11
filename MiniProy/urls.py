from django.conf.urls import url
from django.contrib import admin
from miniproy.views import HomeView, DownloadGRLFile

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^download/$', DownloadGRLFile.as_view(), name='download'),
]
