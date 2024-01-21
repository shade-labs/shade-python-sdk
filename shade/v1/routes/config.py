# get/set config. Add/remove models
# TODO pause, unpause indexing, resync, indexing status / queue size, reset
from shade.v1.api import API
from shade.v1.types import MountInfo


class Config:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_config(self) -> dict:
        # TODO make this a pydantic model
        return self.__api.get('config').json()

    def set_config(self, config: dict) -> None:
        """
        Get the config using the get route, modify it, then set it using this
        :param config: The config dict to set
        :return: None
        """
        self.__api.post('config', json=config)

    # TODO move this to a "models" file
    def enable_all_models(self) -> None:
        """
        Enable all models
        :return: None
        """
        config_ = self.get_config()

        models_ = config_['models']

        for model in models_:
            self.__api.post(f'models/{model}')
