from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from setup import settings
from django.urls import path
from core.views import HistoricoCriminalList, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/historicos/', HistoricoCriminalList.as_view(), name='historico-list'),
    path('', IndexView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






