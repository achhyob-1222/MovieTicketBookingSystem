
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    # The root path now serves the frontend
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
