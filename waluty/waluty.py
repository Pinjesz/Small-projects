import requests as rq
import matplotlib.pyplot as plt


class Currency():
    def __init__(self, code):
        self.data = rq.get(f"http://api.nbp.pl/api/exchangerates/rates/A/{code}/2019-12-01/2019-12-31/?format=json").json()
        self.dates = None
        self.values = None
        self.name = code
    

    def transform_data(self):
        days = self.data["rates"]
        values = []
        dates = []
        for day in days:
            dates.append(day["effectiveDate"][8:])
            values.append(float(day["mid"]))
        self.values = values
        self.dates = dates


    def compare(self, other:'Currency'):
        if self.dates == other.dates:
            quotients = []
            for s_value, o_value in zip(self.values, other.values):
                quotients.append(s_value/o_value)
        return quotients


def calc_deal(cur1:Currency, cur2:Currency):
    values = cur1.compare(cur2)
    dates = cur1.dates
    big_num, big_day = find(values)
    before = values[:big_day]
    small_num, small_day = find(before, True)
    gain = big_num/small_num
    return dates[small_day], dates[big_day], gain


def plot(cur1:Currency, cur2:Currency):
    values = cur1.compare(cur2)
    dates = cur1.dates
    plt.plot(dates, values)
    plt.xlabel("grudzień 2019")
    plt.ylabel(f"Stosunek {cur1.name} do {cur2.name}")
    plt.show()


def find(numbers, lowest=False):
    number = numbers[0]
    idx = 0
    if not lowest:
        for i, num in enumerate(numbers):
            if num > number:
                number  = num
                idx = i
        return number, idx

    for i, num in enumerate(numbers):
        if num < number:
            number  = num
            idx = i
    return number, idx


if __name__ == "__main__":
    buy = "PHP"
    sell = "USD"

    cur1 = Currency(buy)
    cur2 = Currency(sell)
    cur1.transform_data()
    cur2.transform_data()
    deal = calc_deal(cur1, cur2)
    print(f"{cur1.name} należałoby kupić {deal[0]}.12.2019, sprzedać {deal[1]}.12.2019")
    print(f"Zysk wyniósłby {deal[2]} za każdego zainwestowanego {cur2.name}")
    plot(cur1, cur2)
