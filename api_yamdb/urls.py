from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from users.views import CodeConfirmView, EmailSignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path(
        'api/v1/auth/email/',
        EmailSignUpView.as_view(),
        name='token_obtain_pair'
    ),
    path('api/v1/auth/token/', CodeConfirmView.as_view()),
    path('api/', include('users.urls')),
    path('api/', include('api.urls'))
]
