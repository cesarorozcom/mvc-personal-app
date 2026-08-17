from django.urls import path

app_name = "movements"

urlpatterns = [
    path("import/", lambda request: None, name="import-start"),
]
