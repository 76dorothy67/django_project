from django.urls import path, include
from .views import *

urlpatterns = [
    path('', read_all, name='read_all'),
    path('create/', create, name="create"),
    path('record/<int:ind>/', read_record, name="create"),
    path('select/', select, name="select"),
    path('delete/<int:id>', delete, name='delete'),
    path('delete_category/<int:id>', delete_category, name='delete_category'),
    path('imagine', imagine, name='imagine'),
    path('all_categories', all_categories, name='all_categories'),
    path('create_category', create_category, name='create_category'),
    path('update_record/<int:id>', update_record, name='update_record'),
    path('update_record/updaterecord/<int:id>', updaterecord, name='updaterecord'),
    path('update_category/<int:id>', update_category, name='update_category'),
    path('update_category/updatecategory/<int:id>', updatecategory, name='updatecategory'),
]
