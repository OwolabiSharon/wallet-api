import random
number=random.sample(range(1000000000000), 1)
for number in number:
    print(number)


def plausibleAccNo():
    number = random.sample(range(999999999), 1)

    if len(number) != 10:
        number = random.sample(range(999999999), 1)
