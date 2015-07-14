from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete, password_reset_done
from progress import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sayn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^password/reset$', password_reset, {
        'template_name': 'progress/password_reset_form.html',
        'post_reset_redirect': '/password/reset/done'
    }),
    url(r'^password/reset/done$', password_reset_done, {
        'template_name': 'progress/password_reset_done.html',
    }),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {
            'template_name': 'progress/password_reset_confirm.html',
            'post_reset_redirect' : '/password/done'
        },
        name='password_reset_confirm'
    ),
    url(r'^password/done/$', password_reset_complete, {'template_name': 'progress/password_reset_complete.html'}),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/$', views.dashboard),
    url(r'^dashboard/society$', views.society),
    url(r'^dashboard/society/new$', views.newsociety),
    url(r'^dashboard/society/print$', views.printsociety),
    url(r'^dashboard/society/(?P<id>\d+)/edit$',views.editsociety),
    url(r'^dashboard/user$', views.user),
    url(r'^dashboard/user/new$',views.newuser),
    url(r'^dashboard/user/print$',views.printuser),
    url(r'^dashboard/user/(?P<id>\d+)/edit$',views.edituser),
    url(r'^dashboard/task$', views.task),
    url(r'^dashboard/task/new$', views.newtask),
    url(r'^dashboard/task/print$', views.printtask),
    url(r'^dashboard/task/(?P<id>\d+)/edit$',views.edittask),
    url(r'^dashboard/news$', views.news),
    url(r'^dashboard/news/new$', views.newnews),
    url(r'^dashboard/news/(?P<id>\d+)/edit$', views.editnews),
    url(r'^dashboard/user/changepassword$', views.changepassword),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
