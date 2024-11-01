import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.headless = False  # Mode "headless" per executar sense interfície gràfica
        cls.selenium = WebDriver(service=Service(GeckoDriverManager().install()), options=opts)
        cls.selenium.implicitly_wait(5)

        # Crear superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_staff_user_access(self):
        # Log in as superuser
        self.selenium.get(f'{self.live_server_url}/admin/')
        
        # Trobar camps d'usuari i contrasenya
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        # Inserir credencials
        username_input.send_keys("isard")
        password_input.send_keys("pirineus")

        # Prémer botó d'inici de sessió
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()

        # Comprovar que hem iniciat sessió
        assert "Site administration" in self.selenium.page_source

        # Crear un nou usuari amb permisos de staff
        self.selenium.get(f'{self.live_server_url}/admin/auth/user/add/')
        
        # Trobar camps d'usuari
        new_user_username_input = self.selenium.find_element(By.NAME, "username")
        new_user_password_input = self.selenium.find_element(By.NAME, "password1")
        new_user_password_confirm_input = self.selenium.find_element(By.NAME, "password2")

        # Inserir dades del nou usuari
        new_user_username_input.send_keys("staffUser")
        new_user_password_input.send_keys("@password123")
        new_user_password_confirm_input.send_keys("@password123")

        # Prémer botó de guardar
        self.selenium.find_element(By.NAME, "_continue").click()

        # Marcar com a staff
        staff_status_checkbox=self.selenium.find_element(By.NAME, "is_staff")
        if not staff_status_checkbox.is_selected():
            staff_status_checkbox.click()
        
        self.selenium.find_element(By.NAME, "_save").click()

        # Comprovar que el nou usuari apareix a la llista
        self.selenium.get(f'{self.live_server_url}/admin/auth/user/')
        try:
            self.selenium.find_element(By.XPATH, "//a[text()='staffUser']")
        except NoSuchElementException:
            assert False, "L'usuari 'staffUser' no apareix a la llista d'usuaris."

        # Log out
        logout_button = self.selenium.find_element(By.ID, "logout-form").find_element(By.XPATH, ".//button")
        logout_button.click()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/logout/'))

        # Comprovar que l'element de log out no existeix després de desconnectar
        try:
            self.selenium.find_element(By.XPATH, "//a[text()='Log out']")
            assert False, "L'element de 'Log out' no hauria d'existir després de desconnectar."
        except NoSuchElementException:
            pass

        # Log in as staff user
        self.selenium.get(f'{self.live_server_url}/admin/')
        
        # Trobar camps d'usuari i contrasenya
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        # Inserir credencials de l'usuari staff
        username_input.send_keys("staffUser")
        password_input.send_keys("@password123")

        # Prémer botó d'inici de sessió
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()

        # Comprovar que hem iniciat sessió
        assert "Site administration | Django site admin" in self.selenium.page_source

        try:
            # Busca l'element "Log out" per XPath
            self.selenium.find_element(By.XPATH, "//a[text()='Log out']")
            print("Botó de Log Out")
            # Si es troba l'element, el test fallarà amb aquest missatge d'error
            assert False, "Trobat element que NO hi ha de ser"
        except NoSuchElementException:
            # Si no troba l'element, el test passarà correctament
            pass
