import debug_toolbar
from django.conf import settings
from django.conf.urls import re_path
from django.urls import include, path
from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from .api import api_router


urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    #path('search/', search_views.search, name='search'),

    path('api/v2/', api_router.urls),

    re_path(r'^sitemap.xml$', sitemap),
    #path('', include('allauth.urls')),
    #path('', include('userauth.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('allauth.urls')),
    path('', include('userauth.urls')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + i18n_patterns(
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('search/', search_views.search, name='search'),
    path("", include(wagtail_urls)),
    prefix_default_language=False,

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
