class Questionnaire:

    def __init__(self, attributes):
        self.telegram_id = attributes[0]
        self.name = attributes[1]
        self.age = attributes[2]
        self.gender = attributes[3]
        self.roommate_gender = attributes[4]
        self.smoking = attributes[5]
        self.rooms_number = attributes[6]
        self.about = attributes[7]
        self.photo = attributes[8]

    def __str__(self):
        return f"{self.name}\n" \
               f"{self.age} лет\n" \
               f"{'Курю' if self.smoking == 1 else 'Не курю'}\n" \
               f"Желаемое количество комнат: {self.rooms_number}\n" \
               f"{self.about}"
