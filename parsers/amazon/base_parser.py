class BaseParser:
    @staticmethod
    def get_photo_and_videos_if_exists(base_info):
        keys = ("images", "videos")
        base_dict = {}

        for key in keys:
            data = base_info.get(key)
            data_dict = {}
            if data:
                data_dict.update(
                    {f"{key}_link{i}": d.get("link") for i, d in enumerate(data)}
                )
            base_dict.update({key: data_dict})

        return base_dict
