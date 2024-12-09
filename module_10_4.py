import threading
import random
import time
import queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        wait = random.randint(3, 10)
        time.sleep(wait)


class Cafe:
    thread_lst = []

    def __init__(self, *tables):
        self.queue = queue.Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        guests_lst = list(guests)
        tables_lst = self.tables
        len_guests_lst = len(guests_lst)
        guests_table_min = min(len_guests_lst, len(self.tables))
        for i in range(guests_table_min):
            tables_lst[i].guest = guests[i]
            thread_1 = guests[i]
            thread_1.start()
            Cafe.thread_lst.append(thread_1)
            print(f'{guests_lst[i].name} сел(-а) за стол номер {tables_lst[i].number}')
        if len_guests_lst > guests_table_min:
            for i in range(guests_table_min, len_guests_lst):
                self.queue.put(guests[i])
                print(f'{guests_lst[i].name} в очереди')

    def discuss_guests(self):
        while not (self.queue.empty()) or Cafe.check_table(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if (not (self.queue.empty())) and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    thread_1 = table.guest
                    thread_1.start()
                    Cafe.thread_lst.append(thread_1)

    def check_table(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
for thread in Cafe.thread_lst:
    thread.join()
