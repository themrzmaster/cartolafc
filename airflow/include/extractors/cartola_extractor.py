import logging

import fsspec
import requests

from . import AbstractExtractor


class CartolaExtractor(AbstractExtractor):
    def __init__(self, path):
        self.base_url = "https://api.cartolafc.globo.com"
        self.path = path

    def extract(self, execution_date):
        endpoint_list = ["partidas", "atletas/pontuados"]
        max_rounds = 38

        for endpoint in endpoint_list:
            logging.info(f"Extracting data from {self.base_url}/{endpoint}...")
            normalized_name = endpoint.replace("/", "_")
            folder = f"{self.path}/{execution_date.date()}/{normalized_name}"

            try:
                for round in range(1, max_rounds + 1):
                    download_url = f"{self.base_url}/{endpoint}/{round}"
                    filename = f"{round}.json"
                    self.save_file(download_url, folder, filename)
            except requests.exceptions.HTTPError as e:
                logging.error(e)
                logging.info(f"Latest round of the season: {round-1}...")
                break

        logging.info("Extracting season status...")
        download_url = f"{self.base_url}/mercado/status"
        folder = f"{self.path}/{execution_date.date()}/mercado_status"
        self.save_file(download_url, folder, "1.json")

        logging.info("Finishing...")
