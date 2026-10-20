from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from gallery.models import Artwork


class Command(BaseCommand):
    help = "Importa as imagens existentes em IMG como obras iniciais."

    def handle(self, *args, **options):
        project_root = Path(__file__).resolve().parents[3]
        source_directory = project_root / "IMG"
        image_paths = sorted(source_directory.glob("*")) if source_directory.exists() else []
        image_paths = [
            path for path in image_paths if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ]
        if not image_paths:
            self.stdout.write(self.style.WARNING("Nenhuma imagem encontrada em IMG/."))
            return

        created_count = 0
        for index, image_path in enumerate(image_paths, start=1):
            slug = slugify(f"obra-sem-titulo-{index}")
            if Artwork.objects.filter(slug=slug).exists():
                continue
            artwork = Artwork(
                title=f"Obra sem título {index}",
                slug=slug,
                alt_text=f"Obra de arte de Eliani Harsha, imagem {index}.",
                is_published=True,
            )
            with image_path.open("rb") as image_file:
                artwork.image.save(image_path.name, File(image_file), save=True)
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count} obra(s) inicial(is) importada(s)."))
