#!/usr/bin/env python3
import math
import time

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        start_time = time.time()
        five_moves = initial_tree_node.compute_and_get_children()
        high_score = -100000
        best_move = 0
        timeout = False
        depth = 0
        while not timeout:
            try:
                for child in five_moves:
                    if (self.illegal_move(child)):
                        continue
                    else:
                        points = self.find_best_move(
                            child, -100000, 100000, start_time, depth)
                    if points > high_score:
                        high_score = points
                        best_move = child.move
                    depth += 1
            except:
                timeout = True
        return ACTION_TO_STR[best_move]

    # A move is illegal is both of the players have the same x positon
    def illegal_move(self, node):
        state = node.state
        if state.hook_positions[0][0] == state.hook_positions[1][0]:
            return True
        return False

    # Alpha beta pruning algorithm to find the best move
    def find_best_move(self, node, alpha, beta, start_time, depth):
        state = node.state
        children = node.compute_and_get_children()
        # Terminal states
        if len(state.fish_positions) == 0 or len(state.fish_scores) == 0 or depth == 0 and not self.illegal_move(node):
            return self.heuristic(state)

        if time.time() - start_time > 0.055:
            raise TimeoutError

        # https://www.youtube.com/watch?v=l-hh51ncgDI min 8:52
        # Check for player 0 --> Maximizer
        if state.player == 0:
            max_points = -math.inf
            for child in children:
                if self.illegal_move(child):
                    continue
                else:
                    max_points = max(
                        max_points, self.find_best_move(child, alpha, beta, start_time, depth-1))
                alpha = max(alpha, max_points)
                if beta <= alpha:
                    break
            return max_points
        # Check for player 1 --> Minimizer
        else:
            min_points = +math.inf
            for child in node.compute_and_get_children():
                min_points = min(
                    min_points, self.find_best_move(child, alpha, beta, start_time, depth-1))
                beta = min(beta, min_points)
                if beta <= alpha:
                    break
            return min_points

    def heuristic(self, state):
        # Simple heuristic function to calculate the points of the state
        max_points = state.player_scores[0]
        min_points = state.player_scores[1]
        diff = max_points - min_points

        # Maximizer
        if (state.player == 0):
            return diff + self.best_fish(0, state)
        else:
            # Minimizer
            return diff - self.best_fish(1, state)

    # Calculate how much a move is worth based on the fish near the hook
    def best_fish(self, player, state):
        """
        @Param player: 0 or 1
        @Param state: state of the game
        @Return: the best points/distance ratio 
        Gives us the best position to catch fishes 
        """
        hook_position = state.hook_positions[player]
        value_per_distance = 0
        value = 0
        for fish in state.fish_positions.keys():
            # Get the fish score
            fish_score = state.fish_scores[fish]

            # Get the fish position
            fish_position = state.fish_positions[fish]

            # Calculate the distance between the fish and the hook
            distance = self.distance(fish_position, hook_position)

            # Calculate the value per distance
            if distance != 0:
                value = fish_score / distance
            else:
                value_per_distance = fish_score

            # Check if the value per distance is higher than the previous value
            if value > value_per_distance:
                value_per_distance = value
        return value_per_distance

    # Finding the best nearest fish for the player
    def nearest_fish(self, player, state):
        hook_position = state.hook_positions[player]
        clostest_fish = math.inf
        # Iterate all fish positions and find the nearest fish
        for fish in state.fish_positions.values():

            if self.distance(fish, hook_position) < clostest_fish:
                clostest_fish = self.distance(fish, hook_position)
        return clostest_fish

    def distance(self, pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
