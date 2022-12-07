# Reads user input
def readInput():
  transition_matrix_guess = []
  emission_matrix_guess = []
  initial_probabilities_guess = []
  emissions_sequence_guess = []
  for x in input().split():
    transition_matrix_guess.append(float(x))
  for x in input().split():
    emission_matrix_guess.append(float(x))
  for x in input().split():
    initial_probabilities_guess.append(float(x))
  for x in input().split():
    emissions_sequence_guess.append(int(x))
  return transition_matrix_guess, emission_matrix_guess, initial_probabilities_guess, emissions_sequence_guess

# Creates matrix from input
def create_matrix(matrix):
  cols = int(matrix[1])
  matrix = matrix[2:]
  matrix = [matrix[i:i+cols] for i in range(0, len(matrix), cols)]
  return matrix


"""
To do list:
1) 
"""


def main():
  # Start by reading all inputs
  A_guess, B_guess, pi_guess, emission_sequence = readInput()

  # Now create the matrices 
  transitions_matrix = create_matrix(A_guess)
  emission_matrix = create_matrix(B_guess)
  pi_matrix = create_matrix(pi_guess)
  emission_elements = emission_sequence[1:]

  





if __name__ == '__main__':
  main()