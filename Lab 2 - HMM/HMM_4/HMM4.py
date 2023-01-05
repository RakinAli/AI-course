import math

# Reads user input
def readsInput():

  transition_matrix_guess = []
  emission_matrix_guess = []
  initial_probabilities_guess = []
  emissions_sequence_guess = []
  for x in input().split():
    transition_matrix_guess.append(float(x))
  print("Transiton Matrix:" ,transition_matrix_guess)
  for x in input().split():
    emission_matrix_guess.append(float(x))
  print("Emission Matrix:" ,emission_matrix_guess)
  for x in input().split():
    initial_probabilities_guess.append(float(x))
  print("Initial Probabilities:" ,initial_probabilities_guess)
  for x in input().split():
    emissions_sequence_guess.append(int(x))
  print("Emissions Sequence:" ,emissions_sequence_guess)
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
  scale[0]  = (1/scale[0])
  for state in range(total_states):
    alpha[state][0] = scale[0] * alpha[state][0]
  
  # Calculate alpha matrix for all observations
  for observation in range(1, total_observations):
    for from_state in range(total_states):
      # Calculate scaling factor --> sum of all alpha values for each observation
      for to_state in range(total_states):
        # Calculate the probability of being in state i at time t given the observations up to current observation
        alpha[from_state][observation] += alpha[to_state][observation -1]  * transitions_matrix[to_state][from_state]
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
def beta_pass(transitions_matrix, emission_matrix, emission_elements, scale):
    
  total_observations = len(emission_elements)
  total_states = len(transitions_matrix)

  # Create beta matrix
  # [ 1= [ALLA OBSERVATIONER], 2= [ALLA OBSERVATIONER] ] 1 och 2 är states
  beta = [[0 for x in range(total_observations)] for y in range(total_states)]

  # Initialize beta matrix with last observation
  for state in range(total_states):
    beta[state][total_observations-1] = scale[total_observations-1]
  
  # Calculate beta matrix for all observations
  for observation in range(total_observations-2, -1, -1):
    for from_state in range(total_states):
      beta[from_state][observation] = 0
      for to_state in range(total_states):
        beta[from_state][observation] += transitions_matrix[from_state][to_state] * emission_matrix[to_state][emission_elements[observation+1]] * beta[to_state][observation+1]
      # Scale beta matrix for current observation like Mark Stamp (A Reavaling introduction to Hidden Markov Models)
      beta[from_state][observation] = scale[observation] * beta[from_state][observation]
  return beta


# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def digamma(alpha, beta, transitions_matrix, emission_matrix, emission_elements):
  """@docstring
  The digamma function is used to calculate the probability of being in state i at time t and state j at time t+1 given the observations up to time t+1.
  The digamma function is a dynamic programming algorithm that uses the following recursion:
  digamma_t(i,j) = alpha_t(i) * a_ij * b_j(o_t+1) * beta_t+1(j)
  where:
  alpha_t(i) = the probability of being in state i at time t given the observations up to time t
  a_ij = the probability of transitioning from state i to state j
  b_j(o_t+1) = the probability of observing o_t+1 given that we are in state j
  beta_t+1(j) = the probability of being in state j at time t+1 given the observations from time t+1 to the end of the sequence
  """
  total_observation = len(emission_elements)
  total_states = len(transitions_matrix)

  # Create digamma and gamma matrix
  gamma = [[0 for x in range(total_observation)] for y in range(total_states)]
  di_gamma = [[[ 0 for x in range(total_observation)] for y in range(total_states)] for z in range(total_states)]

  # Calculate digamma and gamma matrix
  for observation in range(total_observation-1):
    for from_state in range(total_states):
      for to_state in range(total_states):
        # Calculate the probability of being in state i at time t and state j at time t+1 given the observations up to time t+1
        di_gamma[to_state][from_state][observation] = alpha[from_state][observation] * transitions_matrix[from_state][to_state] * emission_matrix[to_state][emission_elements[observation+1]] * beta[to_state][observation+1]
        # Calculate the probability of being in state i at time t given the observations up to time t
        gamma[from_state][observation] += di_gamma[to_state][from_state][observation]
  
  for state in range(total_states):
    gamma[state][total_observation-1] = alpha[state][total_observation-1]
  return gamma, di_gamma
  
# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def re_estimate_model_parameters(gamma, di_gamma, transitions_matrix, emission_matrix, pi_matrix, emission_elements):
  """@docstring
  The re-estimation step is used to update the model parameters. The re-estimation step is a dynamic programming algorithm that uses the following recursion:
  a_ij = sum_t(digamma_t(i,j)) / sum_t(gamma_t(i))
  b_j(o_t) = sum_t(digamma_t(i,j)) / sum_t(gamma_t(i))
  pi_i = gamma_1(i)
  where:
  digamma_t(i,j) = the probability of being in state i at time t and state j at time t+1 given the observations up to time t+1
  gamma_t(i) = the probability of being in state i at time t given the observations up to time t
  """
  total_observation = len(emission_elements)
  total_states = len(transitions_matrix)

  # Re-estimate the initial state probabilities
  for state in range(total_states):
    pi_matrix[0][state] = gamma[state][0]
  
  # Re-estimate the transition probabilities
  for from_state in range(total_states):
    denominator = 0
    for observation in range(total_observation-1):
      # Calculate the denominator for the transition probabilities
      denominator += gamma[from_state][observation]
    for to_state in range(total_states):
      numerator = 0
      for observation in range(total_observation-1):
        # Calculate the numerator for the transition probabilities
        numerator += di_gamma[to_state][from_state][observation]
      # Calculate the transition probabilities
      transitions_matrix[from_state][to_state] = numerator / denominator
  
  # Re-estimate the emission probabilities
  for from_state in range(total_states):
    denominator = 0
    for observation in range(total_observation):
      # Calculate the denominator for the emission probabilities
      denominator += gamma[from_state][observation]
    for emission in range(len(emission_matrix[0])):
      numerator = 0
      for observation in range(total_observation):
        # Check if the emission is the same as the observation
        if emission_elements[observation] == emission:
          numerator += gamma[from_state][observation]
      # Calculate the emission probabilities
      emission_matrix[from_state][emission] = numerator / denominator      

  return transitions_matrix, emission_matrix, pi_matrix
      

# Heavily inspired by Mark Stamp (A Reavaling introduction to Hidden Markov Models)
def log_likelyhood(scale):
  """@docstring
  The log likelyhood is the sum of the log of the scaling factor
  """
  total_observation = len(scale)
  log_prob = 0
  for observation in range(total_observation):
    log_prob += math.log(scale[observation])
  log_prob = -log_prob
  return log_prob
  
def learning_algorithm(transitions_matrix, emission_matrix, pi_matrix, emission_elements, max_iterations):
  """Docstring
  # 1) Do forward algorithm and get alpha and scaling factor
  # Do backward algorithm and get beta
  # Do digamma function and get gamma and di_gamma
  # Do re-estimation
  # do check convergence
  # do output if converged
  """
  log_prob = -math.inf
  alpha, scaling_factor = alpha_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements)

  for iteration in range(max_iterations):
    # Calculate the alpha, beta and gamma matrix
    alpha, scaling_factor = alpha_pass(transitions_matrix, emission_matrix, pi_matrix, emission_elements)
    beta = beta_pass(transitions_matrix, emission_matrix, emission_elements, scaling_factor)
    gamma, di_gamma = digamma(alpha, beta, transitions_matrix, emission_matrix, emission_elements)

    # Re-estimate the model parameters
    transition_new, emission_new, pi_new = re_estimate_model_parameters(gamma, di_gamma, transitions_matrix, emission_matrix, pi_matrix, emission_elements)

    probability = log_likelyhood(scaling_factor)

    if probability > log_prob:
      log_prob = probability
    else:
      break
    if iteration % 100 == 0:
      print("Iteration: " + str(iteration) + " Log likelyhood: " + str(log_prob))

  return transition_new, emission_new

def answer(matrix):
  print(str(len(matrix)) + ' ' + str(len(matrix[0])), end=' ')
  for row in matrix:
    for element in row:
      print(round(element, 6), end=" ") 

def main():
  # Start by reading all inputs
  A_guess, B_guess, pi_guess, emission_sequence = readsInput()
  print("Done reading input")

  # Now create the matrices
  transitions_matrix = create_matrix(A_guess)
  emission_matrix = create_matrix(B_guess)
  pi_matrix = create_matrix(pi_guess)
  emission_elements = emission_sequence[1:]
  transition_output, emission_output  = learning_algorithm(transitions_matrix, emission_matrix, pi_matrix, emission_elements, 10000)

  # Print the output
  print("Answer:")
  answer(transition_output)
  print()
  answer(emission_output)


main()


