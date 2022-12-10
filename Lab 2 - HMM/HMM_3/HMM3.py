import math

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

# @TODO --> Alpha pass also known as forward pass algorithm
# OBS, heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def alpha_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements):
  """@docstring
  The alpha pass is also known as the forward pass algorithm. It is used to calculate the probability of a given sequence of observations given a model.
  The alpha pass is a dynamic programming algorithm that uses the following recursion:
  alpha_t(i) = sum_j(alpha_t-1(j) * a_ji) * b_i(o_t)
  where:
  alpha_t(i) = the probability of being in state i at time t given the observations up to time t
  a_ji = the probability of transitioning from state j to state i
  b_i(o_t) = the probability of observing o_t given that we are in state i
  """

  total_observations = len(emission_elements)
  total_states = len(transitions_matrix)

  # Create alpha matrix and scaling factor for each observation
  alpha = [[0 for x in range(total_observations)] for y in range(total_states)]
  scale = [0 for x in range(total_observations)]

  # [ 1= [ALLA OBSERVATIONER], 2= [ALLA OBSERVATIONER] ] 1 och 2 är states 
  # Initialize alpha matrix with first observation
  for state in range(total_states):
    alpha[state][0] = pi_matrix[0][state] * emission_matrix[state][emission_elements[0]]
    # Calculate scaling factor --> sum of all alpha values for each observation
    scale[0] += alpha[state][0] 
  
  # Scale alpha matrix for first observation like Mark Stamp (A Reavaling introduction to Hidden Markov Models)
  scale[0]  = 1 / scale[0]
  for state in range(total_states):
    alpha[state][0] = scale[0] * alpha[state][0]
  
  # Calculate alpha matrix for all observations
  for observation in range(1, total_observations):
    for from_state in range(total_states):
      # Calculate scaling factor --> sum of all alpha values for each observation
      alpha[from_state][observation] = 0
      for to_state in range(total_states):
        # Calculate the probability of being in state i at time t given the observations up to current observation
        alpha[from_state][observation] += alpha[from_state][observation -1]  * transitions_matrix[to_state][from_state]
      # Multiply with the probability of observing o_t given that we are in state i
      alpha[from_state][observation] *= emission_matrix[from_state][emission_elements[observation]]
      scale[observation] += alpha[from_state][observation]
    
    # Scale alpha matrix for current observation like Mark Stamp (A Reavaling introduction to Hidden Markov Models)
    scale[observation] = 1 / scale[observation]
    for state in range(total_states):
      alpha[state][observation] = scale[observation] * alpha[state][observation] 
  return alpha, scale
       


# @TODO --> Beta pass also known as backward pass algorithm
# OBS, heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def beta_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements, scale):

  return 0

# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def digamma(alpha, beta, transitions_matrix, emission_matrix, emission_elements):

  return 0


# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def re_estimate_model_parameters(gamma, di_gamma, transitions_matrix, emission_matrix, pi_matrix, emission_elements):

  return 0

# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def calculate_log_likelihood(scale):
  return 0


def learning_algorithm(transitions_matrix, emission_matrix, pi_matrix, emission_elements, max_iterations):
  """Docstring
  # 1) Do forward algorithm and get alpha and scaling factor
  # Do backward algorithm and get beta
  # Do digamma function and get gamma and di_gamma
  # Do re-estimation
  # do check convergence
  # do output if converged
  """

  alpha, scaling_factor = alpha_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements)

  
  
  return 0


def main():
  # Start by reading all inputs
  A_guess, B_guess, pi_guess, emission_sequence = readInput()

  # Now create the matrices
  transitions_matrix = create_matrix(A_guess)
  emission_matrix = create_matrix(B_guess)
  pi_matrix = create_matrix(pi_guess)
  emission_elements = emission_sequence[1:]
  

  transition_output, emission_output  = learning_algorithm(transitions_matrix, emission_matrix, pi_matrix, emission_elements, 100)
  #print_matrix(transition_output)
  #print_matrix(emission_output)


if __name__ == '__main__':
  main()
