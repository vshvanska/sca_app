from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cats.models import Cat


class SpyCatTests(APITestCase):
    def setUp(self):
        self.cat_data = {
            "name": "Persik",
            "years_of_experience": 2,
            "breed": "American Shorthair",
            "salary": 500,
        }
        self.cat = Cat.objects.create(**self.cat_data)
        self.url = reverse("cats:cat-list")

    def test_create_spy_cat(self):
        response = self.client.post(
            self.url,
            {
                "name": "TestCat",
                "years_of_experience": 5,
                "breed": "Aegean",
                "salary": 800,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cat.objects.count(), 2)

    def test_create_spy_cat_invalid_breed(self):
        response = self.client.post(
            self.url,
            {
                "name": "Test cat",
                "years_of_experience": 3,
                "breed": "Unknown Breed",
                "salary": 4000,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("breed", response.data)

    def test_get_spy_cat_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_spy_cat(self):
        response = self.client.get(reverse("cats:cat-detail", args=[self.cat.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.cat.name)

    def test_update_spy_cat_salary(self):
        response = self.client.patch(
            reverse("cats:cat-detail", args=[self.cat.id]), {"salary": 700}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.salary, 700)

    def test_update_spy_cat_experience(self):
        response = self.client.patch(
            reverse("cats:cat-detail", args=[self.cat.id]), {"years_of_experience": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.years_of_experience, 5)

    def test_update_spy_cat_salary_and_experience(self):
        response = self.client.put(
            reverse("cats:cat-detail", args=[self.cat.id]),
            {"salary": 800, "years_of_experience": 6},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.salary, 800)
        self.assertEqual(self.cat.years_of_experience, 6)

    def test_forbidden_update_name(self):
        response = self.client.patch(
            reverse("cats:cat-detail", args=[self.cat.id]), {"name": "New name"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forbidden_update_breed(self):
        response = self.client.patch(
            reverse("cats:cat-detail", args=[self.cat.id]), {"breed": "New breed"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_spy_cat(self):
        response = self.client.delete(reverse("cats:cat-detail", args=[self.cat.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cat.objects.count(), 0)
