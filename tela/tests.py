from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Configurar o driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Abrir o Google
driver.get("https://www.google.com")
print("Página aberta com sucesso:", driver.title)

# Fechar o navegador
driver.quit()