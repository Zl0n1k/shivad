from loguru import logger


class ConfigHelper:
    def __init__(self, config):
        self.config = config

    def get_childs(self, root_key, filters={"enabled": True}):
        data = []
        for child_key, child_data in self.config.get(root_key, {}).items():
            filters_success = True
            for k, v in filters.items():
                d_key = f"{root_key}:{child_key}:{k}"
                # print(f'{d_key} -> {self.config[d_key]}')
                if self.config.get(root_key, {}).get(child_key, {}).get(k) != v:
                    filters_success = False
                    break
            if filters_success:
                data.append((child_key, self.config[root_key][child_key]))
        return data

    def gen_filters(self, filters):
        pass
