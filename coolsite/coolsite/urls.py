from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coolsite import settings
from mount.views import page_not_found
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mount.urls')),
    path('captcha/', include('captcha.urls')),
]



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls')),] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
