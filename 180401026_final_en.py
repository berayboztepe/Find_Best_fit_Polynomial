# Emre Beray BOZTEPE 180401026

from sympy import Symbol

file = open("veriler_final.txt", "r")
data = []

x = Symbol('x')

# Read the values from the file and store them in a list
for i in file:
    data.append(int(i))

# Number of elements in the list
n = len(data)
# Sum of the elements in the list
total_yi = sum(data)

# This function calculates the sum of powers of x up to x^12 and returns the results in a list.
def calculate_x_values(lst, n):
    x_values = []
    for i in range(13):
        x_sum = 0
        for k in range(n):
            x_sum += (k + 1)**i
        x_values.append(x_sum)
    return x_values

# This function calculates the sum of (x^i * y) for x^i up to x^6*y and returns the results in a list.
def calculate_xi_yi_sums(lst, n):
    xi_yi_values = []
    for i in range(7):
        xi_yi_sum = 0
        for k in range(n):
            xi_yi_sum += ((k + 1)**i) * lst[k]
        xi_yi_values.append(xi_yi_sum)
    return xi_yi_values

# This function solves the given matrix using Gaussian elimination and returns the solution.
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

# This function approximates values to polynomials of degree 1 to 6,
# calculates coefficients, and returns them in a list.
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

# Generate the best-fit polynomial as a function, and return its value for a given x.
def fx(x):
    function = 0
    best_degree = find_closest_to_one(list_solutions(data, n), data, n, total_yi)[0][0]
    for solution in list_solutions(data, n):
        if len(solution) == best_degree + 1:
            for j in range(0, best_degree + 1):
                function += solution[j] * (x ** j)
    return function

# Compute the integral of the best-fit polynomial.
def integral1():
    a = 180401026 % 10
    b = len(data)
    delta_x = 0.1
    integral = 0

    n = int((b - a) / delta_x)
    equation = fx(x)
    for i in range(n):
        integral += delta_x * (equation.subs({x: a}) + equation.subs({x: a + delta_x})) / 2
        a += delta_x

    return integral

# Compute the integral directly from the data points.
def integral2():
    a = 180401026 % 10
    b = len(data)
    delta_x = 1
    integral = 0

    n = int((b - a) / delta_x)

    for i in range(n - 1):
        integral += delta_x * (data[a] + data[a + delta_x]) / 2
        a += delta_x

    return integral

# Print the results.
def print_results():
    print("--------------------------------------------------------------")
    print("\n\n")
    print("Best-Fit Polynomial =", find_closest_to_one(list_solutions(data, n), data, n, total_yi)[0][0], 
          "Degree Polynomial.")
    print("\nEquation Found:")
    print(fx(x))  # Print the function as an equation
    print("\n\n")
    print("--------------------------------------------------------------")
    print("\n\n")
    print("Integral of the Best-Fit Polynomial = ", integral1())
    print("\n\n")
    print("--------------------------------------------------------------")
    print("\n\n")
    print("Integral Without Polynomial Fit = ", integral2())
    fnew = open("180401026-comment_en.txt", 'w', encoding='UTF8')
    fnew.write("The smaller the deltax (width of the rectangles), the closer the computed value is to the actual value.\n")
    fnew.write("This is because we find the integral by dividing the polynomial into small rectangles and summing their areas.\n")
    fnew.write("So, the smaller deltax is, the more accurate the value becomes, though it takes longer to compute.\n")
    fnew.write("However, the difference between the two integrals is not primarily due to deltax,\n")
    fnew.write("but because the first integral approximates the polynomial to a certain correlation coefficient.\n")
    fnew.write("Thus, even with the same deltax values, the results differ.")
    
print_results()
