from wsgiref.util import FileWrapper
import imghdr

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from wagtail.images import get_image_model
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import SourceImageIOError


class DynamicResizes(View):
    model = get_image_model()

    def get(self, request, image_id, filter_spec):

        if filter_spec not in settings.PERMITTED_FILTER_SPECS:
            raise PermissionDenied

        image = get_object_or_404(self.model, id=image_id)

        try:
            rendition = image.get_rendition(filter_spec)
        except SourceImageIOError:
            return HttpResponse(
                "Source image file not found", content_type="text/plain", status=410
            )
        except InvalidFilterSpecError:
            return HttpResponse(
                "Invalid filter spec: " + filter_spec, content_type="text/plain", status=400
            )

        rendition.file.open("rb")
        image_format = imghdr.what(rendition.file)

        return StreamingHttpResponse(
            FileWrapper(rendition.file), content_type="image/" + image_format
        )
