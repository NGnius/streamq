import multiprocessing
import requests
from ..objects.basecase import BaseCase
import time

class APICase(BaseCase):
    def setUp(self):
        super().setUp()
        def main_runner():
            from ...main import main
            main.run()
        self.flask_thread = multiprocessing.Process(target=main_runner)
        self.flask_thread.start()
        time.sleep(1)  # TODO: Ensure flask webapp is actually started

    def tearDown(self):
        super().tearDown()
        requests.get('http://localhost:5000/api/shutdown?password=DEBUG')
        self.flask_thread.join()
