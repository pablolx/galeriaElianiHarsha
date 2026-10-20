from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Artwork(models.Model):
    title = models.CharField("título", max_length=160)
    slug = models.SlugField("identificador", max_length=180, unique=True, blank=True)
    description = models.TextField("características", blank=True)
    dimensions = models.CharField("dimensões", max_length=120, blank=True)
    materials = models.CharField("materiais", max_length=240, blank=True)
    creation_date = models.DateField("data de criação", blank=True, null=True)
    creation_location = models.CharField("local de criação", max_length=160, blank=True)
    image = models.ImageField("imagem", upload_to="artworks/")
    alt_text = models.CharField("texto alternativo", max_length=200, blank=True)
    is_featured = models.BooleanField("obra em destaque", default=False)
    is_published = models.BooleanField("publicada", default=True)
    created_at = models.DateTimeField("cadastrada em", auto_now_add=True)

    class Meta:
        ordering = ("-is_featured", "-created_at")
        verbose_name = "obra"
        verbose_name_plural = "obras"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("artwork_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "obra"
            candidate = base_slug
            suffix = 2
            while Artwork.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class Exhibition(models.Model):
    title = models.CharField("título", max_length=160)
    description = models.TextField("descrição", blank=True)
    start_date = models.DateField("data de início")
    end_date = models.DateField("data de encerramento", blank=True, null=True)
    location = models.CharField("local", max_length=200)
    external_url = models.URLField("link externo", blank=True)
    is_published = models.BooleanField("publicada", default=True)

    class Meta:
        ordering = ("start_date",)
        verbose_name = "exposição ou evento"
        verbose_name_plural = "exposições e eventos"

    def __str__(self):
        return self.title
