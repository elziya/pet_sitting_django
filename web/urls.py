from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, pet_edit_view, profile_view, \
    post_edit_view, post_delete_view, analytics_view

urlpatterns = [
    path("", main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("analytics/", analytics_view, name="analytics"),
    path("pets/add/", pet_edit_view, name="pets_add"),
    path("pets/<int:id>/", pet_edit_view, name="pets_edit"),
    path("profile/", profile_view, name="profile"),
    path("posts/add/", post_edit_view, name="posts_add"),
    path("posts/<int:id>/", post_edit_view, name="posts_edit"),
    path("posts/<int:id>/delete", post_delete_view, name="posts_delete")
]
