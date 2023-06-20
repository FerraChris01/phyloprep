import random

def generate_integers(start_range, end_range, num_numbers):
    random_numbers = random.sample(range(start_range, end_range + 1), num_numbers)

    return random_numbers