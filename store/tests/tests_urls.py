from django.test import TestCase
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from store.views import resultats, home, aliment, save_aliment, detail_favori, aliment_delete



class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_resultats_url_resolves(self):
        url = reverse('resultats')
        self.assertEquals(resolve(url).func, resultats)

    def test_aliment_url_resolves(self):
        url = reverse('aliment')
        self.assertEquals(resolve(url).func, aliment)

    def test_save_aliment_url_resolves(self):
        url = reverse('save_aliment', args=[2, 3])
        self.assertEquals(resolve(url).func, save_aliment)
    
    def test_detail_favori_url_resolves(self):
        url = reverse('detail_favori', args=[2])
        self.assertEquals(resolve(url).func, detail_favori)
    
    def test_aliment_delete_url_resolves(self):
        url = reverse('aliment_delete', args=[2])
        self.assertEquals(resolve(url).func, aliment_delete)




