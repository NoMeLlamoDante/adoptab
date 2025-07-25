from django.test import TestCase
from django.contrib.auth.models import User
from pets.models import Pet, Ownership
from pets.services.service import PetService
from datetime import date, timedelta
import datetime

# Create your tests here.


class PetServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='user_test',
            password='user_test_1234'
        )

        self.pet_service = PetService()

    def test_create_pet(self):
        pet = self.pet_service.createPet(
            user=self.user,
            name="Garfield",
            birth_date=datetime.datetime(2020, 5, 15),
            species=Pet.SPECIES_CHOICES[0],
            breed="exótico",
            sex=Pet.SEX_CHOICES[0],
            color="Naranja",
            hair=Pet.HAIR_CHOICES[0],
            size=Pet.SIZE_CHOICES[1],
            bio="no le gustan los lunes",
        )
        self.assertIsNotNone(pet)
        self.assertEqual("Garfield", pet.name)
        self.assertEqual(("M", "Macho"), pet.sex)
