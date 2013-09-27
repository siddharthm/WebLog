from django.conf.urls import patterns,url

from weblog import views

urlpatterns=patterns('',
				url(r'^u/(?P<user_id>\d+)/$',views.index,name='index_user'),
				url(r'^c/(?P<cat_id>\d+)/$',views.index,name='index_cat'),
				url(r'^q/(?P<searchkw>\w+)/$',views.index,name='index_search'),
				url(r'^$',views.index,name='index'),
				url(r'^search/$',views.search,name='search'),

				url(r'^entry/(?P<pid>\d+)/$',views.entry,name='entry'),
				url(r'^comment_action/(?P<pid>\d+)/$',views.comment_action,name='comment_action'),
				

				url(r'^post/$',views.post,name='post'),				
				url(r'^post_action/$',views.post_action,name='post_action'),				

				url(r'^signup/$',views.signup,name='signup'),
				url(r'^signup_action/$',views.signup_action,name='signup_action'),

				url(r'^login/$',views.login,name='login'),
				url(r'^login_action/$',views.login_action,name='login_action'),
				url(r'^signout/$',views.signout,name='signout'),
				url(r'^team/$',views.team,name='team'),
				
				)
		
