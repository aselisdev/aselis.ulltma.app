from django.urls import path

from . import views
from ulltma.views import ActivateAccount

urlpatterns = [
	path('', views.index, name='index'),
	path('signin', views.signin, name='signin'),
	path('signinotp', views.signinotp, name='signinotp'),
	path('ltprep', views.ltprep, name='ltprep'),
	path('ltestprop', views.ltestprop, name='ltestprop'),
	path('learnstylereport', views.learnstylereport, name='learnstylereport'),
	path('dashboard', views.dashboard, name='dashboard'),
	path('skillsearch', views.skillsearch, name='skillsearch'),
	path('reportsearch', views.reportsearch, name='reportsearch'),
	path('changepassword', views.changepassword, name='changepassword'),
	path('changepasswordlogin', views.changepasswordlogin, name='changepasswordlogin'),
	path('skillprep/<str:keyword>/', views.skillprep, name='skillprep'),
	path('pretest/<str:keyword>/', views.pretest, name='pretest'),
	path('ltools/<str:keyword>/', views.ltools, name='ltools'),
	path('posttest/<str:keyword>/', views.posttest, name='posttest'),
	path('results/<str:keyword>/', views.results, name='results'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('test/<int:page>/', views.test, name='test'),
	path('learnresult/<str:skillname>/', views.learnresult, name='learnresult'),
	path('pfpchange', views.pfpchange, name='pfpchange'),
	path('loglink', views.loglink, name='loglink'),
	path('faq', views.faq, name='faq'),
	path('techsupport', views.techsupport, name='techsupport'),
	path('reportissue', views.reportissue, name='reportissue'),
	path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]