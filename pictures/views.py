from django.shortcuts import render

from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Picture
from .utils import generate_custom_presigned_url

# Create your views here.


@method_decorator(csrf_exempt, name="dispatch")
class UploadPictureView(View):
    def post(self, request):
        file = request.FILES.get("file")
        title = request.POST.get("title")

        if not file or not title:
            return JsonResponse(
                {"error": "File and title are required"}, status=400
            )

        picture = Picture.objects.create(title=title, file=file)
        return JsonResponse(
            {
                "id": picture.id,
                "title": picture.title,
                "url": picture.file.url,
                "file_url": generate_custom_presigned_url(picture.file.name),
                "uploaded_at": picture.uploaded_at,
            },
            status=201,
        )


class ListPicturesView(View):
    def get(self, request):
        pictures = Picture.objects.all()
        data = []
        for picture in pictures:
            data.append(
                {
                    "id": picture.id,
                    "title": picture.title,
                    "url": picture.file.url,
                    "file_url": generate_custom_presigned_url(picture.file.name),
                    "uploaded_at": picture.uploaded_at,
                }
            )
        return JsonResponse(data, safe=False)


class DownloadPictureView(View):
    def get(self, request, id):
        picture = get_object_or_404(Picture, id=id)
        return JsonResponse(
            {"url": generate_custom_presigned_url(picture.file.name)})


@method_decorator(csrf_exempt, name="dispatch")
class DeletePictureView(View):
    def delete(self, request, id):
        picture = get_object_or_404(Picture, id=id)
        picture.file.delete(save=False)
        picture.delete()
        return JsonResponse({"message": "Document deleted"})
