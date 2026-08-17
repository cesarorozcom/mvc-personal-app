from django.http import HttpResponse


def import_start(request):
    return HttpResponse("Import start")


def import_detail(request, import_id):
    return HttpResponse(f"Import {import_id}")
