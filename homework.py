from dataclasses import dataclass
from typing import Union, List, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type};"
                f" Длительность: {self.duration:.3f} ч.;"
                f" Дистанция: {self.distance:.3f} км;"
                f" Ср. скорость: {self.speed:.3f} км/ч;"
                f" Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_COFF_1: ClassVar[float] = 18
    CALORIES_COFF_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_COFF_1 * self.get_mean_speed()
                - self.CALORIES_COFF_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_COFF_1: ClassVar[float] = 0.035
    SQUARE_COFF: ClassVar[float] = 2
    CALORIES_COFF_2: ClassVar[float] = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_COFF_1 * self.weight + (self.get_mean_speed()
                ** self.SQUARE_COFF // self.height) * self.CALORIES_COFF_2
                * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_COFF_1: ClassVar[float] = 1.1
    CALORIES_COFF_2: ClassVar[int] = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_COFF_1)
                * self.CALORIES_COFF_2 * self.weight)


def read_package(workout_type: str, data: List[Union[int, float]]) -> Union[
        Training, Union[Running, SportsWalking, Swimming]]:
    """Прочитать данные полученные от датчиков."""

    TrainingMap = {'SWM': Swimming,
                   'RUN': Running,
                   'WLK': SportsWalking,
                   }

    return TrainingMap[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: str = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
