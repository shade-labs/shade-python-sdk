from shade.v1.api import API
from typing import List
from shade.v1.types import MountInfo


class Models:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_models(self) -> List[str]:
        """
        Get the models
        :return: The models
        """
        return self.__api.get('models').json()

    def enable_model(self, model: str) -> None:
        """
        Enable a model
        :param model: The model to enable
        :return: None
        """
        self.__api.post(f'models/{model}')

    def disable_model(self, model: str) -> None:
        """
        Disable a model
        :param model: The model to disable
        :return: None
        """
        self.__api.delete(f'models/{model}')

    def enable_all_models(self) -> None:
        """
        Enable all models
        :return: None
        """
        models_ = self.get_models()

        for model in models_:
            self.enable_model(model)

    def get_download_progress(self) -> dict:
        """
        Get the download progress of the models required for indexing.
        :return: The download progress
        """
        return self.__api.get('models/download-progress').json()
