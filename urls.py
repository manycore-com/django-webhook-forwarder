from django.urls import path
from . import views
from .classviews import ConfigureESP, ForwardingDashboard, ForwardingDashboardAjax

urlpatterns = [
    path('configure-esp/', ConfigureESP.as_view()),
    path('forwarding-dashboard/', ForwardingDashboard.as_view()),
    path('forwarding-dashboard-ajax/', ForwardingDashboardAjax.as_view()),
    path('debug-post/', views.debug_post),
    path('debug-post/<str:extra>/', views.debug_post),
]
