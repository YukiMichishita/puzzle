import logging

from question import questions
from sudoku import solve


def run():
    for q_no, q in enumerate(questions):
        print("=" * 80)
        print(f'Question {q_no}')
        print("-" * 80)
        print_table(q)
        print()

        for a_no, a in enumerate(solve(q)):
            print("-" * 80)
            print(f'Answer {q_no}-{a_no}')
            print("-" * 80)
            print_table(a)
            print()


def print_table(table):
    for y, row in enumerate(table):
        for x, n in enumerate(row):
            if n == 0:
                print(' ', end='')
            else:
                print(n, end='')
            if x in (2, 5):
                print('|', end='')
        print()
        if y in (2, 5):
            print('---+---+---')


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    run()
