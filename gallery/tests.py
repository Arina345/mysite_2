from django.test import TestCase
from .models import Image
from django.core.files import File


class GalleryModelTest(TestCase):
    def test_gallery_model_save_and_retieve(self):
        image1 = Image(
            title=" image 1", image=File(open("gallery/test_images/image1.jpg", "rb"))
        )

        image1.save()

        image2 = Image(
            title=" image 2", image=File(open("gallery/test_images/image2.jpg", "rb"))
        )

        image2.save()
        # загрузи из базы все стаьи
        all_images = Image.objects.all()
        # проверь:статей должно быть 2

        self.assertEqual(all_images[0].title, image1.title)

        self.assertEqual(all_images[0].image, image1.image)

        self.assertEqual(all_images[1].title, image2.title)

        self.assertEqual(all_images[1].image, image2.image)
