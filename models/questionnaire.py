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

    def __str__(self):
        return f"{self.name}\n" \
               f"{self.age} лет\n" \
               f"{'Курю' if self.smoking == 1 else 'Не курю'}\n" \
               f"Желаемое количество комнат: {self.rooms_number}\n" \
               f"{self.about}"
