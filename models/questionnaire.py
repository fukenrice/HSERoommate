class Questionnaire:

    def __init__(self, attributes):
        self.id = attributes[0]
        self.telegram_id = attributes[1]
        self.name = attributes[2]
        self.age = attributes[3]
        self.gender = attributes[4]
        self.roommate_gender = attributes[5]
        self.smoking = attributes[6]
        self.rooms_number = attributes[7]
        self.about = attributes[8]
        self.photo = attributes[9]
        self.how_long = attributes[10]
        self.location = attributes[11]
        self.local_location = attributes[12]
        self.roommate_pets = attributes[13]
        self.budget = attributes[14]
        self.found = attributes[15]

    def __str__(self):
        male = "\N{MAN}"
        female = "\N{WOMAN}"
        return f"{male if self.gender[0].upper() == 'М' else female} {self.name}, " \
               f"{self.age} {'год' if self.age % 10 == 1 else 'года' if 1 < self.age % 10 < 5 else 'лет'}\n" \
               f"\N{ROUND PUSHPIN}О квартире:\n"\
               f"Ищу квартиру {'неважно где' if self.location == 'Неважно' else self.location.lower() if self.local_location == 'Неважно' else (self.location.lower() + ', ' + self.local_location.lower())}\n" \
               f"Хочу снимать {self.how_long.lower()}\n" \
               f"{'Против домашних животных' if self.roommate_pets == 'Нет' else 'Не против домашних животных'}\n" \
               f"Количество комнат: {self.rooms_number.lower()}\n" \
               f"Бюджет с человека {self.budget}\n" \
               f"{'Уже нашел варианты квартир' if self.found == 'Да' else 'Пока ищу варианты квартир'}\n" \
               f"{'Курю' if self.smoking == 1 else 'Не курю'}\n" \
               f"\N{SPEECH BALLOON}О себе:\n{self.about}"
