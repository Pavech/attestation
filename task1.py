import itertools
import json
from typing import Iterable, Dict, Optional, List, Any


class NoProductionError(Exception):
    def __init__(self: Any, message: str) -> None:
        super().__init__(message)


def read_json(json_file: str) -> Any:
    """Чтение файла."""
    with open(json_file, 'r', encoding='utf-8') as file:
        json_dict = json.load(file)
    return json_dict


def get_robot(item: Dict) -> Optional[int]:
    """Возвращает количество роботов"""
    return item.get("robot")


def calculate(mydict: Iterable) -> List:
    """Функция распределяет напитки"""
    # группируем исходные данные по роботам
    robot_resource = itertools.groupby(mydict, get_robot)
    overall_instruction = list()  # запишем сюда все инструкции
    robot_manager = dict()  # для того чтобы распределять ресурсы на разных роботах и избежать пересечений
    for key, group in robot_resource:
        if not robot_manager.get(key):
            robot_manager[key] = dict()
            robot_manager[key]["сахар"] = dict()
            robot_manager[key]["вода"] = dict()
            robot_manager[key]["топинги"] = list()
        for resource in group:
            if resource.get("resource") == "вода":  # вода - базовый ресурс, работаем с ним отдельно
                robot_manager[key]["вода"] = resource
            elif resource.get("resource") == "сахар":
                robot_manager[key]["сахар"] = resource
            else:
                robot_manager[key]["топинги"].append(resource)  # топинги - в отдельный список, для упорядочивания

    for key, item in robot_manager.items():
        water = item.get("вода")
        sugar = item.get("сахар")
        other_resources = item.get("топинги")
        other_resources = sorted(other_resources, key=lambda item: item.get('portion'))  # сортируем топинги по порциям
        try:
            max_water_available = int(water.get("limit") // water.get("portion"))  # сортируем воду по порциям
            max_sugar_available = int(sugar.get("limit") // sugar.get("portion"))  # сортируем сахар по порциям
        except TypeError:
            print('no product')
            break

        for other_resource in other_resources:
            # Выясняем сколько раз можем использовать этот топинг
            portions_avail = int(other_resource.get("limit") // other_resource.get("portion"))
            # Смотрим какое общее количество напитков мы сможем сделать
            portions_with_rest_of_water_sugar = min(max_sugar_available, max_water_available)
            # Пополняем инструкции для производства новыми инструкциями изготовления напитков
            while portions_with_rest_of_water_sugar != 0:
                if portions_avail == 0:
                    overall_instruction.append(
                        {
                            water.get("resource"): water.get("portion"),
                            sugar.get("resource"): sugar.get("portion"),
                            "robot": key
                        }
                    )
                else:
                    overall_instruction.append(
                        {
                            water.get("resource"): water.get("portion"),
                            sugar.get("resource"): sugar.get("portion"),
                            other_resource.get("resource"): other_resource.get("portion"),
                            "robot": key
                        }
                    )
                # вычитаем из возможного количества порций.
                portions_with_rest_of_water_sugar -= 1
                portions_avail -= 1

    # если не удалось составить ни одной инструкции - говорим что ресурсы распределены неверно
    if not overall_instruction:
        raise NoProductionError("no production")

    return overall_instruction


j = read_json("test.json")
print(calculate(j))
