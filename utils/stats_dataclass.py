from dataclasses import dataclass
from typing import List, Dict, Union
from datetime import datetime

@dataclass
class PersonData:
    name: str
    balance: float      # остаток
    total_amount: float # полная сумма

@dataclass
class YearData:
    # 12 месяцев: каждый — список PersonData
    january: List[PersonData] = None
    february: List[PersonData] = None
    march: List[PersonData] = None
    april: List[PersonData] = None
    may: List[PersonData] = None
    june: List[PersonData] = None
    july: List[PersonData] = None
    august: List[PersonData] = None
    september: List[PersonData] = None
    october: List[PersonData] = None
    november: List[PersonData] = None
    december: List[PersonData] = None

    def __post_init__(self):
        # Инициализируем списки, если они не переданы
        if self.january is None:
            self.january = []
        if self.february is None:
            self.february = []
        if self.march is None:
            self.march = []
        if self.april is None:
            self.april = []
        if self.may is None:
            self.may = []
        if self.june is None:
            self.june = []
        if self.july is None:
            self.july = []
        if self.august is None:
            self.august = []
        if self.september is None:
            self.september = []
        if self.october is None:
            self.october = []
        if self.november is None:
            self.november = []
        if self.december is None:
            self.december = []

        # Словарь: индекс (int) -> название месяца (str)
        self._index_to_month = {
            1: 'january',
            2: 'february',
            3: 'march',
            4: 'april',
            5: 'may',
            6: 'june',
            7: 'july',
            8: 'august',
            9: 'september',
            10: 'october',
            11: 'november',
            12: 'december'
        }

        # Словарь: название (рус/англ) -> атрибут (англ)
        self._name_to_attr = {
            'январь': 'january',
            'january': 'january',
            'февраль': 'february',
            'february': 'february',
            'март': 'march',
            'march': 'march',
            'апрель': 'april',
            'april': 'april',
            'май': 'may',
            'may': 'may',
            'июнь': 'june',
            'june': 'june',
            'июль': 'july',
            'july': 'july',
            'август': 'august',
            'august': 'august',
            'сентябрь': 'september',
            'september': 'september',
            'октябрь': 'october',
            'october': 'october',
            'ноябрь': 'november',
            'november': 'november',
            'декабрь': 'december',
            'december': 'december',
        }

    def get(self, month: Union[str, int]) -> List[PersonData]:
        """
        Возвращает список пользователей в указанном месяце.
        month: можно передать как строку (рус/англ) или как int (1-12)
        """
        if isinstance(month, int):
            if 1 <= month <= 12:
                attr_name = self._index_to_month[month]
            else:
                raise ValueError(f"Месяц должен быть от 1 до 12, передано: {month}")
        elif isinstance(month, str):
            attr_name = self._name_to_attr.get(month.lower())
            if attr_name is None:
                raise ValueError(f"Месяц '{month}' не существует")
        else:
            raise TypeError("Месяц должен быть строкой или числом")

        return getattr(self, attr_name)

@dataclass
class AllData:
    # Год -> YearData
    years: Dict[str, YearData] = None
    timestamp : datetime = None

    def __post_init__(self):
        if self.years is None:
            self.years = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()


    def get(self, year: str) -> YearData:
        """
        Возвращает YearData для указанного года.
        Если год не существует — возвращает пустой YearData.
        """
        if year not in self.years:
            self.years[year] = YearData()
        return self.years[year]

    def add_or_update_person(self, year: str, month: str, name: str, balance: float, total_amount: float):
        """
        Добавляет или обновляет данные пользователя в указанном году и месяце.
        Месяц должен быть строкой: 'january', 'february', ..., 'december'.
        Если год или месяц не существуют — создаются.
        """
        year_data = self.get(year)  # используем get, чтобы создать, если нет

        # Получаем список людей в месяце
        month_list = year_data.get(month)

        # Проверяем, есть ли пользователь с таким именем
        for person in month_list:
            if person.name == name:
                # Обновляем данные
                person.balance = balance
                person.total_amount = total_amount
                return

        # Если нет — добавляем нового
        month_list.append(PersonData(name=name, balance=balance, total_amount=total_amount))
        self.timestamp = datetime.now()


months = {"январь": "january",
          "февраль": "february",
          "март": "march",
          "апрель":"april",
          "май": "may",
          "июнь": "june",
          "июль": "july",
          "август": "august",
          "сентябрь": "september",
          "октябрь": "october",
          "ноябрь": "november",
          "декабрь": "december"}

months_int = {
          1: "январь",
          2: "февраль",
          3: "март",
          4: "апрель",
          5: "май",
          6: "июнь",
          7: "июль",
          8: "август",
          9: "сентябрь",
          10: "октябрь",
          11: "ноябрь",
          12: "декабрь"
}