"""

8 - 14
13 - 11
7 - 10
9 - 9
1 - 8
6 - 7
11 - 6

2 - 5
10 - 5

4 - 3
3 - 2

5 - 1
12 - 1



1 - 8
6 - 7
10 - 5
12 - 1

13 - 11
11 - 6
3 - 2
5 - 1

7 - 10
9 - 9
2 - 5
4 - 3

"""
import math
from itertools import islice
import random


def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n - 1, n), None)


class LPT(object):

    def __init__(self, jobs, cars):
        self.jobs = jobs
        self.cars = cars

    def run(self):
        scheduled_jobs, loads = self.lpt_algorithm()
        return scheduled_jobs, loads

    def lpt_algorithm(self):
        sorted_jobs = sorted(self.jobs, reverse=True)

        loads = []
        scheduled_jobs = []
        for processor in range(self.cars):
            loads.append(0)
            scheduled_jobs.append([])

        state = []

        for job in sorted_jobs:
            minloadproc = self._minloadproc(loads)
            if self.jobs.count(job) == 2:
                if job not in state:
                    idx = nth_index(self.jobs, job, 1)
                    scheduled_jobs[minloadproc].append(idx + 1)
                    state.append(job)
                else:
                    idx = nth_index(self.jobs, job, 2)
                    scheduled_jobs[minloadproc].append(idx + 1)
            else:
                scheduled_jobs[minloadproc].append(self.jobs.index(job) + 1)

            loads[minloadproc] += job

        return scheduled_jobs, loads

    def _minloadproc(self, loads):
        minload = min(loads)
        for proc, load in enumerate(loads):
            if load == minload:
                return proc


def generate_values(count: int = 13, left_value: int = 1, right_value:int = 14) -> tuple:

    random_list = random.sample(range(left_value, right_value), count)  # рандомний генератор робіт

    random.shuffle(random_list)  # додаткове переміщення елементів

    # додавання рандомного елемента в рандомне місце ближче до середини
    while True:
        random_inx = random.randint(4, 8)
        random_value = random.randint(1, 12)
        if random_value in random_list and random_list[random_inx] != random_value:
            random_list[random_inx] = random_value
            break

    # Знаходження оптимальності розкладу
    number_optimum = sum(random_list) / 3
    if number_optimum % 1 != 0:
        number_optimum = math.ceil(number_optimum)
    else:
        number_optimum = int(number_optimum)

    # кількість m машин
    cars = list(range(1, 4))

    my_l = []
    row = {}
    # використання LPT-алгоритму
    for car in cars:
        lpt = LPT(random_list, car)
        scheduled_jobs, loads = lpt.run()
        if car == cars[-1]:
            row['car1'] = scheduled_jobs[0]
            row['car2'] = scheduled_jobs[1]
            row['car3'] = scheduled_jobs[2]
            row['f'] = max(loads)

            my_l.append(row)
    return random_list, my_l, number_optimum


from faker import Faker

FAKER = Faker()

MAX_VALUE = 'max'


def generate_tds(list_values):
    tds = ''
    for i, v in enumerate(list_values):
        tds += f'<td width="31" style="text-align: center;"> {v} </td>'
    return tds


# if __name__ == "__main__":
#     counter = 0
#     length = 100_000
#     for i in range(length):
#         random_list, list_dict, summa_optimum = generate_values()
#         for row in list_dict:
#             if row['f'] != summa_optimum:
#                 counter += 1
#                 break
#     value = math.ceil((counter / length) * 100)
#     print(value)

if __name__ == "__main__":
    START_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
        <quiz>
        <!-- question: 0  -->
          <question type="category">
            <category>
              <text>$course$/top/По умолчанию для pz85ot/Терія розкладів</text>
            </category>
            <info format="html">
              <text></text>
            </info>
            <idnumber></idnumber>
          </question>

        <!-- question: 0  -->
          <question type="category">
            <category>
              <text>$course$/top/По умолчанию для pz85ot/Терія розкладів/АрК</text>
            </category>
            <info format="html">
              <text></text>
            </info>
            <idnumber></idnumber>
          </question>"""
    FINAL_TEMPLATE = START_TEMPLATE

    for i in range(99):


        random_list, list_dict, summa_optimum = generate_values() # генератор значень

        tds = generate_tds(list_values=random_list) # генератор таблички з часу робіт

        # основний цикл по кількості прогонів
        for row in list_dict:

            car1 = ' '.join(map(str, row['car1']))
            car2 = ' '.join(map(str, row['car2']))
            car3 = ' '.join(map(str, row['car3']))
            f_max = row['f']
            if f_max == summa_optimum:
                is_optimum = '=так~ні~однозначно сказати не можна'
            else:
                is_optimum = 'так~ні~=однозначно сказати не можна'


            TEMPLATE = """

            <!-- question: """+FAKER.bothify(text='#######')+"""  -->
              <question type="cloze">
                <name>
                  <text>LPT_13_3 """+'%03d' % (i+1)+"""</text>
                </name>
                <questiontext format="html">
                  <text><![CDATA[<p></p>
            <p><span style="font-size: 0.9375rem;">Маємо систему: \\( n=13 \), \\( m=3 \\),&nbsp;\\( F_{max} \\rightarrow min \\) .&nbsp;</span><br><span style="font-size: 0.9375rem;">Тривалості&nbsp; робіт наведені у таблиці.&nbsp;</span><br><span style="font-size: 0.9375rem;">Для побудову розкладу використати &nbsp;\\( LPT \\) - алгоритм.&nbsp;</span></p>
            <p><em>У випадку рівності тривалостей робіт, першою призначається робота з меншим номером. У&nbsp;<em style="font-size: 0.9375rem;"><span lang="RU">разі рівності поточної навантаженості декількох машин, робота призначається на машину
            з меншим номером.</span></em>&nbsp;</em>
            </p>
            <p></p>
            <table border="2" cellpadding="0" cellspacing="0" width="350">
                <colgroup>
                    <col width="31" span="5">
                </colgroup>
                <tbody>
                    <tr height="25">
                        <td height="25" width="31" style="text-align: center;"><strong><em>\( i \)</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>1</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>2</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>3</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>4</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>5</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>6</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>7</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>8</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>9</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>10</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>11</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>12</em></strong></td>
                        <td width="31" style="text-align: center;"><strong><em>13</em></strong>&nbsp;</td>
                    </tr>

                    <tr height="29">
                        <td height="29" width="31" style="text-align: center;">\( t_i \)<br></td>
                        """+tds+"""
                    </tr>
                </tbody>
            </table>
            <p></p><strong>Результуючий розклад </strong><em>(номери робіт через пробіл):</em><br>
            Машина 1 : """"{2:SA:="+car1+"}&nbsp;<br>""""
            Машина 2 : """"{2:SA:="+car2+"}&nbsp;<br>""""
            Машина 3 : """"{2:SA:="+car3+"}&nbsp;<br><strong>""""
            Значення ЦФ</strong>:&nbsp;&nbsp;""""{3:SA:="+str(f_max)+"}<br>""""
            Чи є розклад оптимальним?&nbsp;{2:MC:"""+is_optimum+"""}<br>
            <p></p>]]></text>
                </questiontext>
                <generalfeedback format="html">
                  <text></text>
                </generalfeedback>
                <penalty>0.3333333</penalty>
                <hidden>0</hidden>
                <idnumber></idnumber>
              </question>
            """

        FINAL_TEMPLATE += TEMPLATE
    FINAL_TEMPLATE += '</quiz>'
    with open ('test_question.xml', 'w', encoding='utf-8') as f:
        f.write(FINAL_TEMPLATE)


# def test_lpt():
#     """Testing LPT algorithm with a basic non repeated jobs."""
#     jobs = [8, 5, 2, 3, 1, 7, 10, 14, 9, 5, 6, 2, 11]
#     cars = list(range(1, 4))
#
#     print(DELIMITER1)
#     print("Jobs: {}".format(pprint.pformat(jobs)))
#
#     for car in cars:
#         print(DELIMITER2)
#         print("Car: {}".format(car))
#         lpt = LPT(jobs, car)
#         scheduled_jobs, loads = lpt.run()
#         if car == cars[-1]:
#             print("F max: {}".format(max(loads)))
#         print("Scheduled Jobs: {}".format(pprint.pformat(scheduled_jobs)))
#         print("Loads: {}".format(pprint.pformat(loads)))
#         # LOAD_LIST.append(loads)
#         print(DELIMITER2)
#
#     print(DELIMITER1)

# print(LOAD_LIST)
