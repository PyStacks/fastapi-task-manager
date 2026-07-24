from dataclasses import dataclass, asdict
import yaml

@dataclass
class Config:
    name: str
    param: str
    value: str

config = Config('1','key','123')
dict_config = asdict(config)
print(yaml.safe_dump(config))
