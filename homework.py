class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        return f"Тип тренировки: {self.training_type};"\
            f" Длительность: {'%.3f' %self.duration} ч.;" \
            f" Дистанция: {'%.3f' %self.distance} км;"\
            f" Ср. скорость: {'%.3f' %self.speed} км/ч;"\
            f" Потрачено ккал: {'%.3f' %self.calories}."


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    action: float
    duration: float
    weight: float
    training_type: str = ''

    def __init__(self,
                 action: float,
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    training_type: str = 'Running'

    def get_spent_calories(self) -> float:
        calories_coff_1 = 18
        calories_coff_2 = 20
        calories_coff_3 = 60
        return ((calories_coff_1 * self.get_mean_speed() - calories_coff_2)  
                * self.weight / self.M_IN_KM * self.duration * calories_coff_3)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type: str = 'SportsWalking'
    height: float

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_coff_1 = 0.035
        calories_coff_2 = 2
        calories_coff_3 = 0.029
        calories_coff_4 = 60
        return ((calories_coff_1 * self.weight + (self.get_mean_speed()
                ** calories_coff_2 // self.height) * calories_coff_3
                * self.weight) * self.duration * calories_coff_4)


class Swimming(Training):
    """Тренировка: плавание."""
    training_type: str = 'Swimming'
    length_pool: float
    count_pool: float
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
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
        calories_coff_1 = 1.1
        calories_coff_2 = 2
        return ((self.get_mean_speed() + calories_coff_1) * calories_coff_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(action=data[0], duration=data[1], weight=data[2],
                        length_pool=data[3], count_pool=data[4])
    elif workout_type == 'RUN':
        return Running(action=data[0], duration=data[1], weight=data[2])
    elif workout_type == 'WLK':
        return SportsWalking(action=data[0], duration=data[1], weight=data[2],
                             height=data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
