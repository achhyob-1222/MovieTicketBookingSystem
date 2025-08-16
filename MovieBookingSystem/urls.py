
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),

    path('api/movies/', include('movies.urls')),
    path('api/bookings/', include('booking.urls')),

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
path('movie/<int:pk>/', TemplateView.as_view(template_name='movie_detail.html'), name='movie-detail-page'),
    path('booking/<int:pk>/', TemplateView.as_view(template_name='booking.html'), name='booking-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
