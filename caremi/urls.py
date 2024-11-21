from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload_image, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path("dashboard/",views.user_dashboard, name='dashboard'),
    path('employee/', views.client_side, name='employee'),
    path('vouchers/', views.voucher_list, name='voucher_list'),
    path('vouchers/redeem/<int:voucher_id>/', views.redeem_voucher, name='redeem_voucher'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)