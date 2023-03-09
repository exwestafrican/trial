import json

from django.http import HttpResponse

from minicom.service import CustomerIntercomMessanger


def render_to_json(content, **kwargs):
    return HttpResponse(json.dumps(content), content_type="application/json", **kwargs)


def verify(request):
    return render_to_json({"success": True})


def get_company_prompt(request):
    try:
        if request.method == "GET":
            messanger = CustomerIntercomMessanger()
            domain = request.GET.get("company_domain")
            prompt = messanger.get_prompt(domain)
            return render_to_json(
                {
                    "success": True,
                    "message": "success",
                    "data": {"prompt": prompt.content},
                },
                status=200,
            )
        else:
            return render_to_json(
                {"success": False, "message": "Unsupported HTTP method"},
                status=400,
            )
    except:
        return render_to_json(
            {
                "success": False,
                "message": "Somthing unexpected happend please try again later",
            },
            status=500,
        )


def send_message(request):
    try:
        if request.method == "POST":
            messanger = CustomerIntercomMessanger()
            domain = request.POST.get("company_domain")
            conversation_ref = request.POST.get("conversation_ref")
            content = request.POST.get("content")
            conv_ref = conversation_ref if conversation_ref != "" else None
            if conv_ref is None:
                msg = messanger.start_conversation(msg=content, company_domain=domain)
            else:
                msg = messanger.send_message(msg=content, conversation_ref=conv_ref)
            return render_to_json(
                {
                    "success": True,
                    "message": "success",
                    "data": {
                        "conversation_ref": msg.conversation.id,
                        "domain": domain,
                        "content": msg.content,
                    },
                },
                status=201,
            )
        else:
            return render_to_json(
                {"success": False, "message": "Unsupported HTTP method"},
                status=400,
            )
    except:
        return render_to_json(
            {
                "success": False,
                "message": "Somthing unexpected happend please try again later",
            },
            status=500,
        )


def fetch_response_from_org(request):
    try:
        if request.method == "GET":
            messanger = CustomerIntercomMessanger()
            conversation_ref = request.GET.get("conversation_ref")
            unseen_messages = messanger.fetch_unseen_messages(conversation_ref)
            return render_to_json(
                {
                    "success": True,
                    "message": "success",
                    "data": [
                        {
                            "conversation_ref": msg.conversation.id,
                            "content": msg.content,
                        }
                        for msg in unseen_messages
                    ],
                },
            )
        else:
            return render_to_json(
                {"success": False, "message": "Unsupported HTTP method"},
                status=400,
            )
    except:
        return render_to_json(
            {
                "success": False,
                "message": "Somthing unexpected happend please try again later",
            },
            status=500,
        )
