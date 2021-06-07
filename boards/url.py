
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('boards/<int:board_id>/', views.board_topics, name = 'board_topics'),
    path('boards/<int:board_id>/new/', views.new_topic, name = 'new_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>', views.topic_posts, name = 'topic_posts'),
    path('boards/<int:board_id>/topics/<int:topic_id>/replay/', views.replay_post, name = 'replay_post'),
    path('boards/<int:board_id>/topics/<int:topic_id>/post/<int:post_id>/', views.PostUpdateView.as_view(), name = 'edit_post'),
    path('result/', views.search_view, name = 'result'),
    path('resultBoard/', views.searchBoard_view, name = 'board_search'),
    path('resultUser/', views.searchUser_view, name = 'user_search'),
    path('resultUserTopics/<str:username>', views.searchUserTopic_view.as_view(), name = 'user_search_topics'),

]