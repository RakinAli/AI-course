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
        seen_moves = dict()

        while not timeout:
            try:
                for child in children:
                    score = self.alphabeta(
                        child, -math.inf, math.inf, depth, start_time, seen_moves)
                    if (score > highest_score):
                        highest_score = score
                        best_move = child.move
                depth += 1
            except:
                #print("Depth, ", depth)
                timeout = True
        return best_move

    def alphabeta(self, node, alpha, beta, depth, start_time, seen_moves):

        # Check if the time is up or if the depth limit is reached
        if depth == 0 or (time.time() - start_time) > 0.055:
            if depth == 0:
                return self.heuristics(node)
            else:
                raise TimeoutError

        # Check if Max player we won early
        if self.game_check(node.state) == 1:
            return math.inf
    
        # Check if Min player won early
        elif self.game_check(node.state) == -1:
            return -math.inf

        # Terminal node
        new_children = node.compute_and_get_children()
        if (len(new_children) == 0):
            score = self.heuristics(node)
            return score
        """"
        # If we have seen this state before in a deeper branch we can use the score from that branch
        key = self.hasher(node.state)
        if key in seen_moves and seen_moves[key][0] >= depth:
            return seen_moves[key][1]
        """

        score = 0
        state = node.state
        # Maximizing player
        if state.player == 0:
            score = -math.inf
            for child in new_children:
                score = max(score, self.alphabeta(
                    child, alpha, beta, depth-1, start_time, seen_moves))
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        # Minimizing player
        else:
            score = math.inf
            for child in new_children:
                score = min(score, self.alphabeta(
                    child, alpha, beta, depth-1, start_time, seen_moves))
                beta = min(beta, score)
                if beta <= alpha:
                    break

        seen_moves.update({key: [depth, score]})
        return score

    # heuristics that evaluates the score of a state
    def heuristics(self, node):
        """
        @param node: game tree node
        @return: score of the state
        """
        # Different
        diff = node.state.player_scores[0] - node.state.player_scores[1]
        max_score = 0
        min_score = 0

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
                max_score = max_score + fish_score * 2
            else:
                max_score = max_score + (fish_score / distance_max)

            # Get the value per distance for the fishes for MIN player
            if distance_min == 0:
                min_score = min_score + fish_score * 2
            else:
                min_score = min_score + (fish_score / distance_min)

        # Player with the best score wins
        # SE HÄR
        return diff + (max_score-min_score)

    def game_check(self, state):
        """
        @param state: game state
        @return: True if the game is over
        """
        remaining_fish_sum = 0
        fish_scores = state.fish_scores

        Max_score = state.player_scores[0]
        Max_hook = state.hook_positions[0]

        Min_score = state.player_scores[1]
        Min_hook = state.hook_positions[1]

        fish_score = 0
        # If a hook is on a fish -> just add it to the score
        for fish_id, fish_pos in state.fish_positions.items():
            fish_score = fish_scores[fish_id]
            if (fish_pos == Max_hook):
                Max_score += fish_score
            elif (fish_pos == Min_hook):
                Min_score += fish_score
            else:
                remaining_fish_sum += fish_score

        # These are the remaining fishes and the scores.
        # If the difference between the scores is greater than the sum of the remaining fishes --> We lost or won
        if (Max_score - Min_score) > remaining_fish_sum:
            return 1
        elif (Min_score - Max_score) > remaining_fish_sum:
            return -1
        # Else nothing happens and we continue
        else:
            return 0

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

    def hasher(self, state):
        """
        @Param state: current state
        @return: Key in hash_table
        """
        x = str(state.hook_positions) + str(state.fish_positions)
        return x
