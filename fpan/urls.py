from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.conf import settings
from arches.app.views.auth import UserProfileView, GetClientIdView
from fpan.views import api, main, report, auth, scout, search

uuid_regex = settings.UUID_REGEX
handler500 = main.server_error

urlpatterns = [
    url(r'^$', main.index, name='fpan_home'),
    url(r'^user/resource-instance-permissions', main.get_resource_instance_permissions, name='resource_instance_permissions'),
    url(r'^hms/home', main.hms_home, name='hms_home'),
    url(r'^state/home', main.state_home, name='state_home'),
    url(r'^regions/$', main.show_regions, name='show_regions'),
    url(r'^dashboard', main.fpan_dashboard, name='fpan_dashboard'),
    url(r'^index.htm', RedirectView.as_view(pattern_name='fpan_home', permanent=True)),
    url(r'^scout/signup', scout.scout_signup, name='scout_signup'),
    url(r'^scout/profile', scout.scout_profile, name='scout_profile'),
    url(r'^scouts/$', scout.scouts_dropdown, name='scouts_dropdown'),
    url(r'^scout-list-download/$', scout.scout_list_download, name='scout_list_download'),
    url(r'^report/(?P<resourceid>%s)$' % uuid_regex, report.FPANResourceReportView.as_view(), name='resource_report'),
    # url(r'^search$', search.FPANSearchView.as_view(), name="search_home"),
    url(
        r"^mvt/(?P<nodeid>%s)/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$" % uuid_regex,
        api.MVT.as_view(),
        name="mvt",
    ),
    url(r'^auth/user_profile$', UserProfileView.as_view(), name='user_profile'),
    url(r'^auth/get_client_id$', GetClientIdView.as_view(), name='get_client_id'),
    url(r'^auth/password$', auth.change_password, name='change_password'),
    url(r'^auth/(?P<login_type>[\w-]+)', auth.auth, name='auth'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth.activate, name='activate'),
    url(r'^auth/', RedirectView.as_view(pattern_name='fpan_home', permanent=True)),
    url(r'^', include('arches.urls')),
]
