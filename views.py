from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def debug_post(request: HttpRequest, extra: str = "") -> HttpResponse:
    arg = {
        'extra': extra,
        'requestpost': request.body,
        'requestheaders': request.headers
    }

    print("/webhook-forwarder/debug-post/: " + str(extra) + " body:" + str(request.body))
    print("/webhook-forwarder/debug-post/: headers:" + str(request.headers))

    return render(request, 'webhook-forwarder/debug_post_page.html', arg)
