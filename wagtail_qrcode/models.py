from django import forms
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from wagtail_qrcode.field_panels import QrCodeSVGFieldPanel, QrCodeSVGUsageFieldPanel

ImageModel = get_image_model()
DocumentModel = get_document_model()


class QRCodeMixin(models.Model):
    GENERATE_QR_CODE = True

    qr_code_svg = models.TextField(
        verbose_name="QR Code SVG",
        blank=True,
        null=True,
        help_text="The QR code SVG sample.",
    )

    qr_code_eps = models.ForeignKey(
        get_document_model(),
        verbose_name="QR Code EPS",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    qr_code_eps_email = models.EmailField(
        verbose_name="QR Code EPS Email",
        blank=True,
        null=True,
        help_text="The email address will not be saved to the database and is used only once to send the EPS file.",
    )

    qr_code_usage = models.IntegerField(
        verbose_name="QR Code Usage Count",
        default=0,
        help_text="The number of times the QR code has been used.",
    )

    class Meta:
        abstract = True

    panels = [
        QrCodeSVGUsageFieldPanel(
            "qr_code_usage",
            widget=forms.HiddenInput(),
        ),
        QrCodeSVGFieldPanel(
            "qr_code_svg",
            widget=forms.HiddenInput(),
        ),
        FieldPanel("qr_code_eps"),
        MultiFieldPanel(
            [
                FieldPanel("qr_code_eps_email"),
            ],
            heading="Email address to send the QR code EPS file to",
        ),
    ]