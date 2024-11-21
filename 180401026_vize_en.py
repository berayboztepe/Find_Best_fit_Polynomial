# Emre Beray BOZTEPE 180401026
# Solution for the midterm assignment given for the Scientific Computing course.
# The task is to approximate the given data to polynomials of degree 1 to 6, select the best-fit polynomial,
# and then divide the data into groups of 10 and repeat the process.

file = open("veriler_vize.txt", "r")
data = []

# Read the values from the file and store them in a list
for i in file:
    data.append(int(i))

# Number of elements in the list
n = len(data)
# Sum of the elements in the list
total_yi = sum(data)

# Calculate the sum of powers of x up to x^12 and return the results in a list.
def calculate_x_values(lst, n):
    x_values = []
    for i in range(13):
        x_sum = 0
        for k in range(n):
            x_sum += (k + 1)**i
        x_values.append(x_sum)
    return x_values

# Calculate the sum of (x^i * y) for x^i up to x^6 * y and return the results in a list.
def calculate_xi_yi_sums(lst, n):
    xi_yi_values = []
    for i in range(7):
        xi_yi_sum = 0
        for k in range(n):
            xi_yi_sum += ((k + 1)**i) * lst[k]
        xi_yi_values.append(xi_yi_sum)
    return xi_yi_values

# Solve the given matrix using Gaussian elimination and return the solution.
def gaussian_elimination(matrix, n):
    n = len(matrix)

    for i in range(0, n):
        # Find the highest value in the column and its corresponding row
        max_value = abs(matrix[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > max_value:
                max_value = abs(matrix[k][i])
                max_row = k

        # Swap the row with the maximum value with the current row
        for k in range(i, n + 1):
            temp = matrix[max_row][k]
            matrix[max_row][k] = matrix[i][k]
            matrix[i][k] = temp

        # Make all values below the current row in the column zero
        for k in range(i + 1, n):
            factor = -matrix[k][i] / matrix[i][i]
            for j in range(i, n + 1):
                if i == j:
                    matrix[k][j] = 0
                else:
                    matrix[k][j] += factor * matrix[i][j]

    # Solve the upper triangular matrix
    result = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        result[i] = matrix[i][n] / matrix[i][i]
        for k in range(i - 1, -1, -1):
            matrix[k][n] -= matrix[k][i] * result[i]
    return result

# Approximate the data to polynomials of degree 1 to 6, calculate coefficients, and return them in a list.
def list_solutions(lst, n):
    solutions = []
    for degree in range(2, 8):  # Start from degree 2 since a degree 1 polynomial has 2 unknowns
        matrix = []
        for j in range(degree):
            matrix.append([])
            for k in range(degree):
                # Append x values and at the end append the xiyi value to the list
                matrix[j].append(calculate_x_values(lst, n)[k + j])
            matrix[j].append(calculate_xi_yi_sums(lst, n)[j])
            if j == degree - 1:
                # Solve the matrix and clear it after appending the solution
                solutions.append(gaussian_elimination(matrix, n))
                matrix.clear()
    return solutions

# Calculate the ST value using the formula.
def calculate_st(x, data, n, total_yi):
    y_mean = total_yi / n
    st = 0
    for i in range(n):
        st += (data[i] - y_mean) ** 2
    return st

# Calculate the SR value using the formula, then return the correlation coefficient.
def calculate_correlation_and_sr(x, data, n, total_yi):
    sr = 0
    for i in range(n):
        calculation = 0
        calculation += x[0]
        for j in range(1, len(x)):
            calculation += x[j] * (i + 1) ** j
        sr += (data[i] - calculation) ** 2

    return ((calculate_st(x, data, n, total_yi) - sr) / calculate_st(x, data, n, total_yi)) ** (1 / 2)

# Generate a list of correlation coefficients.
def list_correlation_values(correlation_values, data, n, total_yi):
    r_values = []
    for value in correlation_values:
        r_values.append(calculate_correlation_and_sr(value, data, n, total_yi))
    return r_values

# Find the value closest to 1 in the correlation coefficients list and return it.
def find_closest_to_one(correlation_values, data, n, total_yi):
    correlation_list = list_correlation_values(correlation_values, data, n, total_yi)
    closest_value = float('inf')
    closest_poly = []
    for i in range(len(correlation_list)):
        difference = abs(1 - correlation_list[i])
        if difference < closest_value:
            closest_value = difference
            closest_poly.clear()
            closest_poly.append((i + 1, correlation_list[i]))
    return closest_poly

# Print the results for all data and for groups of 10 data points.
def print_results():
    file_output = open("result_vize_en.txt", "w+")
    file_output.write("*******************FOR ALL DATA*******************" + "\n\n\n")
    a = 0
    for solution in list_solutions(data, n):
        file_output.write("\t\t" + str(a + 1) + " Degree Polynomial\n")
        b = 0
        for coefficient in solution:
            file_output.write(str(b + 1) + ". Coefficient = " + str(coefficient) + "\n")
            b += 1
        file_output.write("Correlation = " + str(list_correlation_values(list_solutions(data, n), data, n, total_yi)[a]) + "\n")
        a += 1
    file_output.write("\n\t***Best Polynomial and Correlation Value for All Data = " + str(
        find_closest_to_one(list_solutions(data, n), data, n, total_yi)[0]) + "***\n\n\n")

    # Divide the data into groups of 10 and repeat the calculations.
    for j in range(len(data)):
        a = 0
        new_list = []
        if j + 10 > len(data):
            break
        for l in range(j, j + 10):
            new_list.append(data[l])
        file_output.write("*******************For Data From " + str(j + 1) + " to " + str(j + 10) + "*******************")
        file_output.write("\n\t***Best Polynomial and Correlation Value for This Range = " + str(
            find_closest_to_one(list_solutions(new_list, len(new_list)), new_list, len(new_list), sum(new_list))[0]) + "***\n\n\n")

    # Divide the data into non-overlapping groups of 10
    start = 1
    end = 10
    a = 0
    for j in range(len(data)):
        new_list = []
        if (end * a) + 10 > len(data):
            break
        for l in range((start * a * 10), end * a + 9):
            new_list.append(data[l])
        file_output.write(
            "*******************For Data From " + str(start * a * 10) + " to " + str(end * a + 9) + "*******************")
        file_output.write("\n\t***Best Polynomial and Correlation Value for This Range = " + str(
            find_closest_to_one(list_solutions(new_list, len(new_list)), new_list, len(new_list), sum(new_list))[0]) + "***\n\n\n")
        a += 1
    file_output.close()

print_results()
