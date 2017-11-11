from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.activity, name='activity'),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^logout/$', views.logout_user, name="logout"),
    #url(r'^check/$', views.check, name="check"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^account/new/$', views.account_new, name='account_new'),
    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^search/$', views.search, name="search"),
    url(r'^add/$', views.add_link, name="add_link"),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete_link, name="delete_link"),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_link, name="edit_link"),
    url(r'^submissions/$', views.submissions, name="submissions"),
    url(r'^statistics/$', views.statistics, name="statistics"),
    url(r'^(?P<tagfilter>TV)/$', views.index, name='index'),
    url(r'^(?P<tagfilter>Movie)/$', views.index, name='index'),
    url(r'^(?P<tagfilter>Game)/$', views.index, name='index'),
    url(r'^(?P<tagfilter>Software)/$', views.index, name='index'),
    url(r'^(?P<tagfilter>Ebook)/$', views.index, name='index'),
    url(r'^(?P<tagfilter>Tutorial)/$', views.index, name='index'),
    url(r'^(?P<tagfilter>Music)/$', views.index, name='index'),
    url(r'^(?P<tagfilter>Documentary)/$', views.index, name='index'),

]