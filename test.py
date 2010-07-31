import unittest

class LoadingTest(unittest.TestCase):
    def testSetup(self):
        import dataloader as dl
        

if __name__ == "__main__":
    loading = unittest.TestLoader().loadTestsFromTestCase(LoadingTest)
    unittest.TextTestRunner(verbosity=2).run(loading)

    


