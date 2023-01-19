def readInput():
  # Moving from one state to another, the probability of that happening
  transition_matrix = []
  # The probability of a certain emission given a certain state
  emission_matrix = []
  # The probability of starting in a certain state
  initial_probabilities = []
  for x in input().split():
    transition_matrix.append(float(x))
  for x in input().split():
    emission_matrix.append(float(x))
  for x in input().split():
    initial_probabilities.append(float(x))
  return transition_matrix, emission_matrix, initial_probabilities

# Reads conver
def create_matrix(matrix):
  cols = int(matrix[1])
  matrix = matrix[2:]
  matrix = [matrix[i:i+cols] for i in range(0, len(matrix), cols)]
  return matrix

# matrix_multiplication
def matrix_multiplication(matrix1, matrix2):
  result = [[0 for x in range(len(matrix2[0]))] for y in range(len(matrix1))]
  for i in range(len(matrix1)):
    # Visiting columns of matrix 2
    for j in range(len(matrix2[0])):
      # Visiting rows of matrix 2
      for k in range(len(matrix2)):
        # Multiplying and adding to result
        result[i][j] += matrix1[i][k] * matrix2[k][j]
  return result

def main():
  trans_input, emis_inpus, init_input = readInput()

  transition_matrix = create_matrix(trans_input)
  emission_matrix = create_matrix(emis_inpus) 
  initial_probabilities = create_matrix(init_input)

  # Creating transitions tables 
  first_transitions = matrix_multiplication(initial_probabilities, transition_matrix)
  
  # Creating emission tables
  probabilities_matrix = matrix_multiplication(first_transitions, emission_matrix)

  # Rounding the results 
  for i in range(len(probabilities_matrix)):
    probabilities_matrix[0][i] = round(probabilities_matrix[0][i], 3)
  
  # Printing the results
  stringRows = str(len(first_transitions))
  stringCols = str(len(emission_matrix[0])) 
  elementString = (" ".join(map(str, probabilities_matrix[0])))
  print(stringRows + " " + stringCols + " " + elementString) 

if __name__ == "__main__":
  main()