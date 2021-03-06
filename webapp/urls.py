"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import (
    path,
    include,
)
from django.views.generic import RedirectView
from rest_framework.authtoken import views

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/')),
    path('admin/', admin.site.urls),
    path('api/v1/token/auth/', views.obtain_auth_token),
    path('api/v1/', include('mainapp.urls', namespace='mainapp')),
]

if settings.DEBUG:
    from rest_framework.documentation import (
        get_docs_view,
        get_schemajs_view,
        include_docs_urls,
    )

    urlpatterns += [
        # path(
        #     'api/auth/',
        #     RedirectView.as_view(url='login/')
        # ),
        path(
            'api/auth/',
            include('rest_framework.urls', namespace='rest_framework')
        ),
        path(
            'api/docs/',
            include_docs_urls(title='API Service')
        ),
        path(
            'api/docs_view/',
            get_docs_view(title='API Service')
        ),
        path(
            'api/schemajs/',
            get_schemajs_view(title='API Service')
        ),
    ]

