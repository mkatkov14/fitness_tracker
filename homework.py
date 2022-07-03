from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {0}; '
                    'Длительность: {1:.3f} ч.; '
                    'Дистанция: {2:.3f} км; '
                    'Ср. скорость: {3:.3f} км/ч; '
                    'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        """возвращает строку сообщения"""
        return self.MESSAGE.format(self.training_type,
                                   self.duration,
                                   self.distance,
                                   self.speed,
                                   self.calories)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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

        raise NotImplementedError('Метод не определен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_RUN_1: int = 18
    COEFF_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return((self.COEFF_RUN_1 * self.get_mean_speed() - self.COEFF_RUN_2)
               * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WLK_1: float = 0.035
    COEFF_WLK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return((self.COEFF_WLK_1 * self.weight
               + (self.get_mean_speed() ** 2 // self.height)
               * self.COEFF_WLK_2 * self.weight)
               * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_SWIM: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return(self.length_pool * self.count_pool / self.M_IN_KM
               / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return(self.get_mean_speed() + self.COEFF_SWIM) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_training: dict[str, type[Training]] = {'RUN': Running,
                                                'WLK': SportsWalking,
                                                'SWM': Swimming}
    if workout_type not in dict_training:
        raise ValueError(f'{workout_type} - неверный тип тренировки')
    return dict_training[workout_type](*data)


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
