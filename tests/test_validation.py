from django.urls import reverse
from rest_framework.exceptions import ValidationError

from generic_permissions.config import ValidatorsConfig
from generic_permissions.validation import validator_for

from .models import Model1, Model2


def test_custom_validation(db, admin_client):
    model1 = Model1.objects.create(text="hello")

    class LowercaseUsername:
        @validator_for(Model1)
        def lowercase_text_attr(self, data, context):
            data["text"] = data["text"].lower()
            return data

    class RejectEverything:
        # Two validator markers - we support stacking/chaining
        @validator_for(Model1)
        @validator_for(Model2)
        def reject_all(self, data, context):
            raise ValidationError("NOPE")

    def send_update():
        return admin_client.patch(
            url,
            format="json",
            data={
                "text": "SOME UPPERCASE TEXT",
                "id": str(model1.pk),
            },
        )

    url = reverse("model1-detail", args=[model1.pk])

    # First, check if rejection works
    ValidatorsConfig.clear_handlers()
    ValidatorsConfig.register_handler_class(RejectEverything)
    resp = send_update()

    assert resp.json() == {"non_field_errors": ["NOPE"]}

    # Then, check if the data modification works
    ValidatorsConfig.clear_handlers()
    ValidatorsConfig.register_handler_class(LowercaseUsername)

    resp = send_update()
    assert resp.json()["text"] == "some uppercase text"

    # Also check in DB
    model1.refresh_from_db()
    assert model1.text == "some uppercase text"
