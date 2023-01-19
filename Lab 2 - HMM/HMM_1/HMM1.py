#Reads user input 
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

# Reads conver
def create_matrix(matrix):
  cols = int(matrix[1])
  matrix = matrix[2:]
  matrix = [matrix[i:i+cols] for i in range(0, len(matrix), cols)]
  return matrix

# Forward Algorithm
"""Here we don't care about which state that produce O. Instead we what to know
the probability of the sequence of observations O. We can do this by summing
over all possible paths that produce O. This is the forward algorithm.
Hence why in the slides we first use Sumrule over all emissions given state then take
Product rule over "Emission given State" then sum them all together. 
"""
def forward_algorithm(transition_matrix, emission_matrix, initial_probabilities, emissions_sequence):
  #Alpha[i]  is the probability of being in state i at time t and emitting the first t observations
  #Alpha[i][t]: t is the time and i is the state 
  # Time complexity for forward algorithm is: LISTA UT DET SJÄLV
  alpha = [[0 for x in range(len(emissions_sequence))] for y in range(len(transition_matrix))]
  T = len(emissions_sequence)
  N = len(transition_matrix)
  # Initial alpha 
  for i in range(N):
    # Initial state times emission probability given emission 
    alpha[i][0] = initial_probabilities[0][i] * emission_matrix[i][emissions_sequence[0]]
  for t in range(1, T):
    for i in range(N):
      for j in range(N):
        alpha[i][t] += alpha[j][t-1] * transition_matrix[j][i] * emission_matrix[i][emissions_sequence[t]]        
  
  answer = 0
  for i in range(N):
    answer += alpha[i][T-1]
  return answer  

def main():
  # --> 
  trans_input, emis_inpus, init_input, emis_seq = readInput()

  # Creating the matrices 
  transition_matrix = create_matrix(trans_input)
  emission_matrix = create_matrix(emis_inpus)
  initial_probabilities = create_matrix(init_input)
  emissions_elements = emis_seq[1:]

  # Forward Algorithm
  answer = forward_algorithm(transition_matrix, emission_matrix, initial_probabilities, emissions_elements)
  print(round(answer, 6))

if __name__ == "__main__":
  main()


  
