from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.static import serve

from .forms import ContactForm
from .models import Artwork, Exhibition


def home(request):
    featured_artworks = Artwork.objects.filter(is_published=True, is_featured=True)[:6]
    if not featured_artworks:
        featured_artworks = Artwork.objects.filter(is_published=True)[:6]
    today = timezone.localdate()
    next_exhibition = (
        Exhibition.objects.filter(is_published=True)
        .filter(Q(start_date__gte=today) | Q(end_date__gte=today))
        .order_by("start_date")
        .first()
    )
    return render(
        request,
        "gallery/home.html",
        {"featured_artworks": featured_artworks, "next_exhibition": next_exhibition},
    )


def artwork_list(request):
    artworks = Artwork.objects.filter(is_published=True)
    return render(request, "gallery/artwork_list.html", {"artworks": artworks})


def artwork_detail(request, slug):
    artwork = get_object_or_404(Artwork, slug=slug, is_published=True)
    return render(request, "gallery/artwork_detail.html", {"artwork": artwork})


def artwork_media(request, path):
    image_name = f"artworks/{path}"
    images = Artwork.objects.filter(image=image_name)
    if not request.user.is_staff:
        images = images.filter(is_published=True)
    if not images.exists():
        raise Http404
    return serve(request, image_name, document_root=settings.MEDIA_ROOT)


def biography(request):
    return render(request, "gallery/biography.html")


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        recipient = settings.CONTACT_EMAIL or settings.DEFAULT_FROM_EMAIL
        email = EmailMessage(
            subject=f"[Site Eliani Harsha] {form.cleaned_data['subject']}",
            body=(
                f"Mensagem de {form.cleaned_data['name']} "
                f"({form.cleaned_data['email']}):\n\n{form.cleaned_data['message']}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[form.cleaned_data["email"]],
        )
        email.send()
        messages.success(request, "Sua mensagem foi enviada. Obrigada pelo contato!")
        return redirect("contact")
    return render(request, "gallery/contact.html", {"form": form})
