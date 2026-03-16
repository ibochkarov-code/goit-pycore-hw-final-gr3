from datetime import date

from models.fields import Birthday, Email, Name, Phone


class Record:
    """Клас запису (контакту) в адресній книзі."""

    def __init__(
        self,
        name: str,
        phones: list[str] | None = None,
        email: str | None = None,
        birthday: str | None = None,
    ) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        # Додаємо початкові телефони, якщо надано
        if phones:
            for ph in phones:
                self.add_phone(ph)
        self.email: Email | None = Email(email) if email else None
        self.birthday: Birthday | None = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number: str) -> bool:
        """Додати новий номер телефону до контакту."""
        new_phone = Phone(phone_number)
        # Уникаємо дублювання номерів
        if new_phone.value not in [p.value for p in self.phones]:
            self.phones.append(new_phone)
            return True
        return False  # Якщо такий номер вже є

    def remove_phone(self, phone_number: str) -> bool:
        """Видалити номер телефону з контакту."""
        for p in self.phones:
            if p.value == phone_number:
                self.phones.remove(p)
                return True
        # Якщо номер не знайдено, генеруємо помилку
        raise ValueError("Phone number not found")

    def edit_phone(self, old_number: str, new_number: str) -> None:
        """Замінити існуючий номер old_number на new_number."""
        # Знаходимо та видаляємо старий номер
        removed = False
        for p in self.phones:
            if p.value == old_number:
                self.phones.remove(p)
                removed = True
                break
        if not removed:
            raise ValueError(f"Phone number {old_number} not found")
        # Додаємо новий номер
        self.add_phone(new_number)

    def edit_email(self, new_email: str) -> None:
        """Змінити email-адресу контакту."""
        self.email = Email(new_email)

    def edit_birthday(self, new_birthday: str) -> None:
        """Змінити дату народження контакту."""
        self.birthday = Birthday(new_birthday)

    def days_to_birthday(self) -> int | None:
        """Повернути кількість днів до наступного дня народження контакту."""
        if not self.birthday:
            return None
        bdate = self.birthday.value  # тип datetime.date
        today = date.today()
        # Обчислюємо найближчий день народження (цього року або наступного)
        year = today.year
        while True:
            try:
                next_bday = date(year, bdate.month, bdate.day)
            except ValueError:
                # Якщо дата народження 29 лютого, а рік не високосний
                year += 1
                continue
            if next_bday < today:
                year += 1
                continue
            break
        return (next_bday - today).days

    def __str__(self) -> str:
        phones_str = (
            ", ".join(p.value for p in self.phones) if self.phones else "no phones"
        )
        email_str = f", Email: {self.email.value}" if self.email else ""
        bday_str = (
            f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
            if self.birthday
            else ""
        )
        return f"{self.name.value}: Phones: {phones_str}{email_str}{bday_str}"
