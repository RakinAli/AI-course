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
  for state in range(total_states):
    # Initial probability of observing the first emission element given the initial state
    alpha[0][state] = pi_matrix[0][state] * emission_matrix[state][emission_elements[0]]
    scale[0] += alpha[0][state]
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
        # Calculate the probability of being in state i at time t given the previous observations
        beta[t][i] += transitions_matrix[i][j] * emission_matrix[j][emission_elements[t+1]] * beta[t+1][j]
      # Scale beta at time t like Mark Stamp
      beta[t][i] = scale[t] * beta[t][i]
  return beta

# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def digamma(alpha, beta, transitions_matrix, emission_matrix, emission_elements):
  """@docstring
  Gamma and Di_gamma are used to calculate the re-estimation of the model parameters.
  Gamma specifically is used to calculate the probability of being in a state at a given time.
  di_gamma is used to calculate the probability of transitioning from one state to another (don't care which state) at a given time.
  """
  total_observations = len(emission_elements)
  total_states = len(transitions_matrix)

  # Create digamma and di_gamma matrices
  gamma = [[0 for x in range(total_states)] for y in range(total_observations)]
  di_gamma = [[[0 for x in range(total_states)] for y in range(total_states)] for z in range(total_observations)]
  for observation in range(total_observations):
    for from_state in range(total_states):
      for to_state in range(total_states):
        # Calculate the probability of being in state i at time t given the previous observations
        di_gamma[observation][from_state][to_state] = alpha[observation][from_state] * transitions_matrix[from_state][to_state] * emission_matrix[to_state][emission_elements[observation]] * beta[observation][to_state]
        # Calculate the probability of being in state i at time t given the previous observations
        gamma[observation][from_state] += di_gamma[observation][from_state][to_state]

  for i in range(total_states):
    gamma[total_observations-1][i] = alpha[total_observations-1][i]
  return gamma, di_gamma


# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def re_estimate_model_parameters(gamma, di_gamma, transitions_matrix, emission_matrix, pi_matrix, emission_elements):
  """@docstring
  Re-estimate the model parameters using the gamma and di_gamma matrices.
  """
  total_observations = len(emission_elements)
  total_states = len(transitions_matrix)

  # Re-estimate the initial state probabilities
  for i in range(total_states):
    pi_matrix[0][i] = gamma[0][i]

  # Re-estimate the transition probabilities
  for state in range(total_states):
    denominator = 0
    for observation in range(total_observations-1):
      # 
      denominator += gamma[observation][state]
    for next_state in range(total_states):
      numerator = 0
      for observation in range(total_observations-1):
        numerator += di_gamma[observation][state][next_state]
      transitions_matrix[state][next_state] = numerator / denominator
    
  # Re-estimate the emission probabilities
  for state in range(total_states):
    denominator = 0
    for observation in range(total_observations):
      denominator += gamma[observation][state]
    for emission in range(len(emission_matrix[0])):
      numerator = 0
      # Loop through all observations
      for observation in range(total_observations):
        # Check if the emission is the same as the observation
        if emission_elements[observation] == emission:
          # If so, add it to the numerator
          numerator += gamma[observation][state]
      emission_matrix[state][emission] = numerator / denominator
    
  return transitions_matrix, emission_matrix, pi_matrix

# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def calculate_log_likelihood(scale):
  """@docstring
  Calculate the log likelihood of the model given the observations.
  """
  total_observations = len(scale)
  log_likelihood = 0
  for observation in range(total_observations):
    log_likelihood += math.log(scale[observation])
  log_likelihood = -log_likelihood
  return log_likelihood


def learning_algorithm(transitions_matrix, emission_matrix, pi_matrix, emission_elements, max_iterations):
  """@docstring
  The Baum-Welch algorithm is used to re-estimate the model parameters given a sequence of observations.
  """
  # The log likelihood of the model given the observations
  log_prob = -math.inf

  for iterations in range(max_iterations):
    # Calculate the alpha, beta, gamma and di_gamma matrices
    alpha, scale = alpha_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements)
    beta = beta_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements, scale)
    gamma, di_gamma = digamma(alpha, beta, transitions_matrix, emission_matrix, emission_elements)

    # Re-estimate the model parameters
    transitions_matrix, emission_matrix, pi_matrix = re_estimate_model_parameters(gamma, di_gamma, transitions_matrix, emission_matrix, pi_matrix, emission_elements)

    # Given the initial model parameters, calculate the log likelihood of the observations
    probabilitiy = log_likelihood = calculate_log_likelihood(scale)

    if probabilitiy > log_prob:
      old_log_prob = log_prob
      #print("Hi I work")
    else:
      break
  
  print("Transition Matrix: ", transitions_matrix)
  print("Emission Matrix: ", emission_matrix)


def main():
  # Start by reading all inputs
  A_guess, B_guess, pi_guess, emission_sequence = readInput()

  # Now create the matrices 
  transitions_matrix = create_matrix(A_guess)
  emission_matrix = create_matrix(B_guess)
  pi_matrix = create_matrix(pi_guess)
  emission_elements = emission_sequence[1:]

  learning_algorithm(transitions_matrix, emission_matrix, pi_matrix, emission_elements, 100)



if __name__ == '__main__':
  main()