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
@TODO 
1) Fixa alpha pass, also known as the forward pass
2) Fixa beta pass, also known as the backward pass
3) Fixa gamma pass
4) Fixa xi pass
5) Fixa re-estimation
6) Fixa convergence
7) Fixa output
"""

#@TODO --> Alpha pass also known as forward pass algorithm 
# OBS, heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def alpha_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements):
  """@docstring
  The alpha pass is also known as the forward pass algorithm. It is used to calculate the probability of a given sequence of observations given a model.
  The alpha pass is a dynamic programming algorithm that uses the following recursion:
  alpha_t(i) = sum_j(alpha_t-1(j) * a_ji) * b_i(o_t)
  where:
  alpha_t(i) = the probability of being in state i at time t given the previous observations
  a_ji = the probability of transitioning from state j to state i
  b_i(o_t) = the probability of observing o_t given that we are in state i
  """

  total_observations = len(emission_elements)
  total_states = len(transitions_matrix)
  # Create alpha matrix
  alpha = [[0 for x in range(total_states)] for y in range(total_observations)]
  scale = [0 for x in range(total_observations)]

  # Initial Alpha matrix values at step 0
  for i in range(total_states):
    # Initial probability of observing the first emission element given the initial state
    alpha[0][i] = pi_matrix[0][i] * emission_matrix[i][emission_elements[0]]
    scale[0] += alpha[0][i]
  # Scale the initial alpha like Mark Stamp
  scale[0] = 1 / scale[0]
  for i in range(total_states):
    alpha[0][i] = scale[0] * alpha[0][i]

  # Calculate the rest of the alpha matrix
  for t in range(1, total_observations):
    for i in range(total_states):
      alpha[t][i] = 0
      for j in range(total_states):
        # Calculate the probability of being in state i at time t given the previous observations
        alpha[t][i] += alpha[t-1][j] * transitions_matrix[j][i]
      # Calculate the probability of observing the emission element given the state
      alpha[t][i] *= emission_matrix[i][emission_elements[t]]
      scale[t] += alpha[t][i]
    # Scale alpha at time t like Mark Stamp
    scale[t] = 1 / scale[t]
    for i in range(total_states):
      alpha[t][i] = scale[t] * alpha[t][i]

  return alpha, scale


#@TODO --> Beta pass also known as backward pass algorithm
# OBS, heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def beta_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements, scale):
  """@docstring
  The beta pass is also known as the backward pass algorithm. It is used to calculate the probability of a given sequence of observations given a model.
  The beta pass is a dynamic programming algorithm that uses the following recursion:
  beta_t(i) = sum_j(a_ij * b_j(o_t+1) * beta_t+1(j))
  where:
  beta_t(i) = the probability of being in state i at time t given the previous observations
  a_ij = the probability of transitioning from state i to state j
  b_j(o_t+1) = the probability of observing o_t+1 given that we are in state j
  """
  total_observations = len(emission_elements)
  total_states = len(transitions_matrix)
  # Create beta matrix
  beta = [[0 for x in range(total_states)] for y in range(total_observations)]

  # Initial beta matrix values at step T
  for i in range(total_states):
    beta[total_observations-1][i] = scale[total_observations-1]

  # Calculate the rest of the beta matrix
  for t in range(total_observations-2, -1, -1):
    for i in range(total_states):
      beta[t][i] = 0
      for j in range(total_states):
        # Calculate the probability of being in state i at time t given the front observations
        beta[t][i] += transitions_matrix[i][j] * emission_matrix[j][emission_elements[t+1]] * beta[t+1][j]
      # Scale beta at time t like Mark Stamp
      beta[t][i] = scale[t] * beta[t][i]
  return beta

  

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