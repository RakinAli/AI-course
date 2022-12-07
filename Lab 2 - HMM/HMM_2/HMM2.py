# Reads user input
def readInput():
  transition_matrix = []
  emission_matrix = []
  initial_probabilities = []
  emissions_sequence = []
  for x in input().split():
    transition_matrix.append(float(x))
  for x in input().split():
    emission_matrix.append(float(x))
  for x in input().split():
    initial_probabilities.append(float(x))
  for x in input().split():
    emissions_sequence.append(int(x))
  return transition_matrix, emission_matrix, initial_probabilities, emissions_sequence

# Creates matrix from input
def create_matrix(matrix):
  cols = int(matrix[1])
  matrix = matrix[2:]
  matrix = [matrix[i:i+cols] for i in range(0, len(matrix), cols)]
  return matrix

# Viterbi Algorithm --> Calculates the most probable sequence of hidden states
# OBS Code similar to the wikipedia pseudocode
# Link to wikipedia: https://en.wikipedia.org/wiki/Viterbi_algorithm 
def viterbi_algorithm(transition_matrix, emission_matrix, initial_probabilities, emissions_sequence):
  # Initializing the variables
  total_observations = len(emissions_sequence)
  total_states = len(transition_matrix)

  # Initializing the T1 and T2 matrices
  T1 = [[0 for x in range(total_states)] for y in range(total_observations)] # T1 matrix is the probability of the most probable path
  T2 = [[0 for x in range(total_states)] for y in range(total_observations)] # T2 matrix is the most probable path

  # Initializing the first column of the T1 matrix
  for state in range(total_states):
    T1[0][state] = initial_probabilities[0][state] * emission_matrix[state][emissions_sequence[0]]
 
  # Filling the T1 and T2 matrices
  for observation in range(1, total_observations): # OBS observation 2
    for state in range(total_states): 
      # Current_State = Where we were in the previous observation
      # [State] = The state we are heading to
      T1[observation][state] = max(T1[observation-1][current_state] * transition_matrix[current_state][state] * emission_matrix[state][emissions_sequence[observation]] for current_state in range(total_states))
      T2[observation][state] = max((T1[observation-1][current_state] * transition_matrix[current_state][state] * emission_matrix[state][emissions_sequence[observation]], current_state) for current_state in range(total_states))[1]
    
  # Finding the most probable sequence of hidden states
  hidden_states = [0 for x in range(total_observations)] # Initializing the hidden states as zeros in a list
  hidden_states[total_observations-1] = max( (T1[total_observations-1][i], i) for i in range(total_states))[1]  # Finding the most probable state in the last observation
  
 
  for t in range(total_observations-2, -1, -1): 
    hidden_states[t] = T2[t+1][hidden_states[t+1]] # Pick the state with the highest probability in the previous observation and add it to the list of hidden states
  return hidden_states

def main():
  trans_input, emis_inpus, init_input, emis_seq = readInput()

  # Creating the matrices
  transition_matrix = create_matrix(trans_input)
  emission_matrix = create_matrix(emis_inpus)
  initial_probabilities = create_matrix(init_input)
  emissions_elements = emis_seq[1:]

  answer = viterbi_algorithm(transition_matrix, emission_matrix, initial_probabilities, emissions_elements)
  print(" ".join(str(x) for x in answer))


if __name__ == "__main__":
  main()
