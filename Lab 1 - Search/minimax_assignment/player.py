#!/usr/bin/env python3
import random
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

        node = initial_tree_node
        best_move = self.find_best_move(node)

        return ACTION_TO_STR[best_move]

    #
    def find_best_move(self, node):
        """
        @param node: initial game tree node
        @return: best move
        """
        children = node.compute_and_get_children()
        best_move = 0
        highest_score = -math.inf
        timeout = False
        start_time = time.time()
        depth = 0
        while not timeout:
            try:
                for child in children:
                    score = self.alphabeta(
                        child, -math.inf, math.inf, depth, start_time)
                    if (score > highest_score):
                        highest_score = score
                        best_move = child.move
                depth += 1
            except:
                timeout = True
        return best_move

    def alphabeta(self, node, alpha, beta, depth, start_time):
        score = 0
        new_children = node.compute_and_get_children()
        # Terminal node
        if depth == 0 or len(node.children) == 0:
            score = self.heuristics(node)
            return score

        elif time.time() - start_time > 0.055:
            raise TimeoutError

        state = node.state
        # Maximizing player
        if state.player == 0:
            score = -math.inf
            for child in new_children:
                score = max(score, self.alphabeta(
                    child, alpha, beta, depth-1, start_time))
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        # Minimizing player
        else:
            score = math.inf
            for child in new_children:
                score = min(score, self.alphabeta(
                    child, alpha, beta, depth-1, start_time))
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return score

    # heuristics that evaluates the score of a state
    def heuristics(self, node):
        """
        @param node: game tree node
        @return: score of the state
        """
        # Different
        diff = node.state.player_scores[0] - node.state.player_scores[1]
        max_score = -math.inf
        min_score = -math.inf
        max_temp = 0
        min_temp = 0

        # Get the fish score of every fish
        for fish in node.state.fish_positions.keys():
            # Get the fish sore and position
            fish_score = node.state.fish_scores[fish]
            fish_pos = node.state.fish_positions[fish]

            # Get the hook positions for MAX and MIN
            hook_max = node.state.hook_positions[0]
            hook_min = node.state.hook_positions[1]

            # Get the distances between the fish and the hooks
            distance_max = self.manhattan_distance(fish_pos, hook_max)
            distance_min = self.manhattan_distance(fish_pos, hook_min)

            # Get the value per distance for the fishes for MAX player
            if distance_max == 0:
                max_temp = fish_score * 2
            else:
                max_temp = fish_score / distance_max

            # Get the value per distance for the fishes for MIN player
            if distance_min == 0:
                min_temp = fish_score
            else:
                min_temp = fish_score / distance_min

            # Pick the best value for MAX and MIN player
            if (max_temp > max_score):
                max_score = max_temp
            if (min_temp > min_score):
                min_score = min_temp

        # Player with the best score wins
        # SE HÄR
        return diff + (max_score-min_score)

    # Get the distance between the fish and the players
    def manhattan_distance(self, pos1, pos2):
        """
        @param pos1: position of the fish
        @param pos2: position of the player
        @return: distance between the fish and the player"""

        y = abs(pos1[1] - pos2[1])
        x1 = abs(pos1[0] - pos2[0])
        x = min(x1, 20 - x1)

        return x + y
