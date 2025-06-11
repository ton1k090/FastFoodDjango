from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>/', category_list, name='category_list'),
    # path('post/<int:pk>/', post_detail, name='post_detail'),
    # path('add_article', add_post, name='add'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('profile/<int:user_id>', profile, name='profile'),

    path('', Index.as_view(), name='index'),
    path('category/<int:pk>', ArticleByCategory.as_view(), name='category_list' ),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('add_article/', AddPost.as_view(), name='add'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchResult.as_view(), name='search'),
    path('password/', UserChangePassword.as_view(), name='change_password'),

    path('posts/api/', CookingAPI.as_view(), name='CookingAPI'),
    path('posts/api/<int:pk>', CookingAPIDetail.as_view(), name='CookingAPIDetail'),
    path('categories/api/', CookingCategoryAPI.as_view(), name='CookingCategoryAPI'),
    path('categories/api/<int:pk>', CookingCategoryAPIDetail.as_view(), name='CookingCategoryAPIDetail'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]