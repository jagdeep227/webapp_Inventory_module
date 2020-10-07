from django.urls import path
from . import views

app_name=''

urlpatterns = [
    path('testing',views.testing_css,name='tetsing_css'),
    path('', views.base, name='base'),
    path('base_employee/', views.base_employee, name='base_employee'),    
    path('base_customer/<str:pk>/', views.base_customer, name='base_customer'),    
    path('see_customers/',views.see_customers,name='see_customers'),
    path('see_customers_admin/',views.see_customers_admin,name='see_customers_admin'),
    path('see_employees/',views.see_employees,name='see_employees'),
    path('login/', views.login, name='login'),
    path('logout',views.logout,name='logout'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('add_customer/',views.add_customer,name='add_customer'),
    path('update_customer/<str:pk>/',views.update_customer,name='update_customer'),
    path('open_customer/',views.open_customer,name='open_customer'),
    path('view_customer/',views.view_customer,name='view_customer'),
    path('view_stock/<str:pk>/',views.view_stock,name='view_stock'),
    path('product_log/<str:pk>/',views.product_log,name='product_log'),
    path('add_stock/<str:pk>/',views.add_stock,name='add_stock'),
    path('see_stocks/',views.see_stocks,name='see_stocks'),
    path('see_stocks_admin/',views.see_stocks_admin,name='see_stocks_admin'),
    path('see_added_stocks_dates/',views.see_added_stocks_dates,name='see_added_stocks_dates'),
    path('prod_varities/<str:pk>/',views.prod_varities,name='prod_varities'),
    path('prod_varities_admin/<str:pk>/',views.prod_varities_admin,name='prod_varities_admin'),
    path('see_out_stocks/',views.see_out_stocks,name='see_out_stocks'),
    path('prod_out_varities/<str:pk>/',views.prod_out_varities,name='prod_out_varities'),
    path('see_out_stocks_admin/',views.see_out_stocks_admin,name='see_out_stocks_admin'),
    path('prod_out_varities_admin/<str:pk>/',views.prod_out_varities_admin,name='prod_out_varities_admin'),
    path('GeneratePDF/<str:pk>/',views.GeneratePDF,name='GeneratePDF'),
    path('GeneratePDF2/<str:pk>/',views.GeneratePDF2,name='GeneratePDF2'),
    path('GeneratePDF3/<str:pk>/',views.GeneratePDF3,name='GeneratePDF3'),
    path('checkout/<str:pk>/',views.checkout,name='checkout'),
    path('home_forcustomer/',views.home_forcustomer,name='home_forcustomer'),
    path('view_stock_forcustomer/<str:pk>/',views.view_stock_forcustomer,name='view_stock_forcustomer'),
    path('product_log_forcustomer/<str:pk>/',views.product_log_forcustomer,name='product_log_forcustomer'),

]