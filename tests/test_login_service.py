import unittest

from src.login_service import (
    LoginService,
    LoginResult,
    MSG_CHAMPS_VIDES,
    MSG_ECHEC,
    MSG_EMAIL_INVALIDE,
    MSG_SUCCES,
)

class LoginServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = LoginService({"etudiant@ensa.ma": "Secret123"})

    def test_identifiants_valides(self):  # CA1
        r = self.service.login("etudiant@ensa.ma", "Secret123")
        self.assertTrue(r.success)
        self.assertEqual(r.message, MSG_SUCCES)

    def test_champs_vides(self):  # CA2
        for email, pwd in [("", "x"), ("etudiant@ensa.ma", ""), (None, None)]:
            r = self.service.login(email, pwd)
            self.assertFalse(r.success)
            self.assertEqual(r.message, MSG_CHAMPS_VIDES)

    def test_format_email_invalide(self):  # CA2
        r = self.service.login("etudiant-ensa.ma", "Secret123")
        self.assertFalse(r.success)
        self.assertEqual(r.message, MSG_EMAIL_INVALIDE)

    def test_message_generique(self):  # CA3
        inconnu = self.service.login("inconnu@ensa.ma", "Secret123")
        mauvais_mdp = self.service.login("etudiant@ensa.ma", "Faux")
        self.assertFalse(inconnu.success)
        self.assertFalse(mauvais_mdp.success)
        self.assertEqual(inconnu.message, mauvais_mdp.message)
        self.assertEqual(inconnu.message, MSG_ECHEC)

class TestChampsAvecEspaces(unittest.TestCase):

    def setUp(self):
        self.service = LoginService({"user@example.com": "secret"})

    def test_champs_avec_espaces_consideres_vides(self):
        cas = [
            ("   ", "secret"),               
            ("user@example.com", "   "),     
            ("\t", "\n"),                    
        ]
        for email, password in cas:
            with self.subTest(email=email, password=password):
                self.assertEqual(
                    self.service.login(email, password),
                    LoginResult(False, MSG_CHAMPS_VIDES),
                )

if __name__ == "__main__":
    unittest.main()
