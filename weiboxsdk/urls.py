from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('weiboxauth.views',
    # Examples:
    # url(r'^$', 'weiboxexample.views.home', name='home'),
    # url(r'^weiboxexample/', include('weiboxexample.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$','index',name='weiboxauth_index'),
    url(r'^login/$','qqweibo_login',name='weiboxauth_qqweibo_login'),
    url(r'^login/done/$','qqweibo_login_done',name='weiboxauth_qqweibo_login_done'),
    url(r'^logout/$','qqweibo_login_out',name='weiboxauth_qqweibo_login_out'),
    url(r'^home/$','home',name='weiboxauth_home'),
    url(r'^home_timeline/$','qqweibo_home_timeline',name='weiboxauth_qqweibo_home_timeline'),
    url(r'^mentions_timeline/$','qqweibo_mentions_timeline',name='weiboxauth_qqweibo_mentions_timeline'),
    url(r'^user_timeline/([^/]+)/$','qqweibo_user_timeline',name='weiboxauth_qqweibo_user_timeline'),
    url(r'^public_timeline/$','qqweibo_public_timeline',name='weiboxauth_qqweibo_public_timeline'),
    url(r'^tweet/$','qqweibo_tweet',name='weiboxauth_qqweibo_tweet'),
    url(r'^add/$','add_tweet',name='weiboxauth_add_tweet'),
    url(r'^re_add/$','re_add_tweet',name='weiboxauth_re_add_tweet'),
    url(r'^comment/$','comment_tweet',name='weiboxauth_comment_tweet'),
    url(r'^del/(?P<id>\d+)/$','del_tweet',name='weiboxauth_del_tweet'),
    url(r'^fanslist/$','qqweibo_get_fanslist',name='weiboxauth_qqweibo_get_fanslist'),
    url(r'^idollist/$','qqweibo_get_idollist',name='weiboxauth_qqweibo_get_idollist'),
    url(r'^speciallist/$','qqweibo_get_speciallist',name='weiboxauth_qqweibo_get_speciallist'),
    url(r'^blacklist/$','qqweibo_get_blacklist',name='weiboxauth_qqweibo_get_blacklist'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)