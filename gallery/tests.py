from datetime import timedelta
from unittest.mock import patch

from django.core import mail
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Artwork, Exhibition


class PublicPagesTests(TestCase):
    def setUp(self):
        self.artwork = Artwork.objects.create(
            title="Cores da mata",
            image="artworks/cores.jpg",
            is_featured=True,
            dimensions="30 x 40 cm",
            materials="Acrílica sobre tela",
        )

    def test_home_shows_featured_artwork(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Cores da mata")

    def test_home_falls_back_to_latest_published_artworks(self):
        self.artwork.is_featured = False
        self.artwork.save()
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Cores da mata")

    def test_home_omits_unpublished_artworks(self):
        self.artwork.is_published = False
        self.artwork.save()
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Cores da mata")

    def test_artwork_details_include_metadata_and_share_actions(self):
        response = self.client.get(reverse("artwork_detail", args=[self.artwork.slug]))
        self.assertContains(response, "30 x 40 cm")
        self.assertContains(response, "Acrílica sobre tela")
        self.assertContains(response, "facebook.com/sharer")
        self.assertContains(response, "Instagram · compartilhar link")
        self.assertContains(response, 'property="og:image"')

    def test_unpublished_artwork_has_no_public_detail(self):
        self.artwork.is_published = False
        self.artwork.save()
        response = self.client.get(reverse("artwork_detail", args=[self.artwork.slug]))
        self.assertEqual(response.status_code, 404)

    @patch("gallery.views.serve", return_value=HttpResponse())
    def test_public_artwork_image_is_served(self, serve):
        response = self.client.get("/media/artworks/cores.jpg")
        self.assertEqual(response.status_code, 200)
        serve.assert_called_once()

    def test_unpublished_artwork_image_is_not_served(self):
        self.artwork.is_published = False
        self.artwork.save()
        response = self.client.get("/media/artworks/cores.jpg")
        self.assertEqual(response.status_code, 404)

    def test_home_shows_next_published_exhibition(self):
        Exhibition.objects.create(
            title="Exposição futura",
            start_date=timezone.localdate() + timedelta(days=5),
            location="Natal",
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Exposição futura")

    def test_home_hides_past_and_unpublished_exhibitions(self):
        Exhibition.objects.create(
            title="Exposição passada",
            start_date=timezone.localdate() - timedelta(days=5),
            location="Natal",
        )
        Exhibition.objects.create(
            title="Exposição não publicada",
            start_date=timezone.localdate() + timedelta(days=5),
            location="Natal",
            is_published=False,
        )
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Exposição passada")
        self.assertNotContains(response, "Exposição não publicada")
        self.assertNotContains(response, "Próximo encontro")

    def test_home_shows_ongoing_exhibition(self):
        Exhibition.objects.create(
            title="Exposição em andamento",
            start_date=timezone.localdate() - timedelta(days=2),
            end_date=timezone.localdate() + timedelta(days=3),
            location="Natal",
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Exposição em andamento")

    def test_biography_page_contains_provided_history(self):
        response = self.client.get(reverse("biography"))
        self.assertContains(response, "São Paulo, em 1949")
        self.assertContains(response, "IBAMA")
        self.assertContains(response, "papel machê")

    def test_gallery_page_lists_published_artworks(self):
        response = self.client.get(reverse("artwork_list"))
        self.assertContains(response, "Cores da mata")


@override_settings(CONTACT_EMAIL="artista@example.com")
class ContactPageTests(TestCase):
    def test_valid_contact_message_is_sent(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Pessoa",
                "email": "pessoa@example.com",
                "subject": "Sobre uma obra",
                "message": "Gostaria de saber mais.",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["artista@example.com"])
        self.assertEqual(mail.outbox[0].reply_to, ["pessoa@example.com"])

    def test_invalid_contact_message_is_not_sent(self):
        response = self.client.post(reverse("contact"), {"email": "invalido"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_subject_is_kept_on_one_line(self):
        self.client.post(
            reverse("contact"),
            {
                "name": "Pessoa",
                "email": "pessoa@example.com",
                "subject": "Sobre a obra\nBcc: outra@example.com",
                "message": "Olá.",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn("\n", mail.outbox[0].subject)


class AdministrationAccessTests(TestCase):
    def test_admin_requires_authentication(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    @override_settings(
        DEBUG=False,
        SECURE_SSL_REDIRECT=True,
        SECURE_REDIRECT_EXEMPT=[r"^health/$"],
    )
    def test_render_health_check_is_available_without_https_redirect(self):
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")
