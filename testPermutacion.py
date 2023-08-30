# Number of Directional Runs test statistic function
def calculate_directional_runs(S_prime):
    #print(S_prime)
    T = 1  # Initialize the number of runs

    for i in range(1, len(S_prime)):
        if S_prime[i] != S_prime[i - 1]:
            T += 1

    return T


# Length of Longest Directional Run test statistic function
def calculate_length_of_longest_directional_run(S_prime):
    max_run_length = 1
    current_run_length = 1

    for i in range(1, len(S_prime)):
        if S_prime[i] == S_prime[i - 1]:
            current_run_length += 1
            max_run_length = max(max_run_length, current_run_length)
        else:
            current_run_length = 1

    return max_run_length



# Number of Increases and Decreases test statistic function
def calculate_number_of_increases_decreases(S_prime):
    num_increases = S_prime.count(1)
    num_decreases = S_prime.count(-1)
    T = max(num_increases, num_decreases)

    return T

# Number of Runs Based on the Median test statistic function
def calculate_number_of_runs_median(data):
    median = sorted(data)[len(data) // 2]
    S_prime = [1 if value >= median else -1 for value in data]
    T = 1

    for i in range(1, len(S_prime)):
        if S_prime[i] != S_prime[i - 1]:
            T += 1

    return T


# Length of Runs Based on Median test statistic function
def calculate_length_of_runs_median(data):
    median = sorted(data)[len(data) // 2]
    S_prime = [1 if value >= median else -1 for value in data]
    max_run_length = 1
    current_run_length = 1

    for i in range(1, len(S_prime)):
        if S_prime[i] == S_prime[i - 1]:
            current_run_length += 1
            max_run_length = max(max_run_length, current_run_length)
        else:
            current_run_length = 1

    return max_run_length


def calculate_average_collision(data):
    C = []  # List to store the number of samples observed to find two occurrences of the same value
    i = 0
    L = len(data)

    while i < L-1:
        tmp = [data[i]]
        j = 1
        while i + j < L:
            if data[i + j] in tmp:
                C.append(j + 1)  # Include both indices i and i + j
                i = i + j + 1
                break
            else:
                tmp.append(data[i + j])
            j += 1
        else:
            C.append(j)  # Include only the current index i
            i += 1
    T = sum(C) // len(C) if len(C) > 0 else 0

    return T


def calculate_max_collision(data):
    C = []  # List to store the number of samples observed to find two occurrences of the same value
    i = 0
    L = len(data)

    while i < L-1:
        tmp = [data[i]]
        j = 1
        while i + j < L:
            if data[i + j] in tmp:
                C.append(j + 1)  # Include both indices i and i + j
                i = i + j + 1
                break
            else:
                tmp.append(data[i + j])
            j += 1
        else:
            C.append(j)  # Include only the current index i
            i += 1
    T = max(C)

    return T
