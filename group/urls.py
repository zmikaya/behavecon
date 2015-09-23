from django.conf.urls import patterns, url
from group import views

urlpatterns = patterns('',
        url(r'^Category3Dams/p([0-9]{2}\-[0-9]{1})', views.Category3Dams),
        url(r'^Category3Dams/p([0-9]{2})', views.Category3Dams),
        url(r'^Category3Dams/p([0-9]{1})', views.Category3Dams),
        url(r'^Category3Dams/', views.Category3Dams),
        url(r'^Free3Dams/p([0-9]{2})', views.Free3Dams),
        url(r'^Priming3Dams/p([0-9]{2})', views.Free3Dams),
        # url(r'^Free3Dams/p([0-9]{1})', views.Free3Dams),
        # url(r'^Free3Dams/', views.Free3Dams),
        url(r'^login', views.login_user),
        url(r'^profile', views.profile),
        url(r'^create_session', views.create_session),
        url(r'^end_session', views.end_session),
        url(r'^data/(?P<session>[a-zA-Z0-9_]*$)', views.get_data),
        url(r'^chat_data/(?P<session>[a-zA-Z0-9_]*$)', views.get_chat_data),
        url(r'^player_state/(?P<session>[a-zA-Z0-9_]*$)', views.get_player_states),
        url(r'^logout', views.logout_user),
        url(r'^', views.index)
        )