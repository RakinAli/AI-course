#!/usr/bin/env python3
import random
import math


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

        # Gives us the 4 possible moves for the player
        children = initial_tree_node.compute_and_get_children()
        score = -1000000
        move = 0
        for child in children:
            possible_scores = self.minimax_alpha_beta(child, -1000000, 1000000)
            if possible_scores > score:
                score = possible_scores
                move = child.move
        return ACTION_TO_STR[move]
    """
    Minimax algorithm från youtube
         if depth == 0 or node is a terminal node:
                return the heuristic value of node
        if maximizingPlayer:
            maxEval = -infinity
            for child in node:
                eval = minimax(child, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = +infinity
            for child in node:
                eval = minimax(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
            return minEval
    """

    def minimax_alpha_beta(self, node, alpha, beta,):
        state = node.state
        # We found the last node or the game is over
        if node.depth == 2 or len(state.fish_positions) == 0:
            return self.evaluate_score(state)

        # Min is playing which is us (copying the opponents move) 
        if state.player:
            smallest = 1000000
            children = node.compute_and_get_children()
            for child in children:
                evaluate = self.minimax_alpha_beta(child, alpha, beta)
                smallest = min(smallest, evaluate)
                beta = min(beta, smallest)
                if beta <= alpha:
                    break
            return smallest
        # Max is playing which is us maximating our score
        else:
            largest = -1000000
            children = node.compute_and_get_children()
            for child in children:
                evaluate = self.minimax_alpha_beta(child, alpha, beta)
                largest = max(largest, evaluate)
                alpha = max(alpha, largest)
                if beta <= alpha:
                    break
            return largest

    def evaluate_score(self, state):
        # opponents score
        max_score = state.player_scores[0]
        # our score
        min_score = state.player_scores[1]
        diff = max_score - min_score
        # Min is playing which is us (the player
        if state.player:
            diff = diff + self.nearest_fish(state.player, state)
            return diff
        # Max is playing which is the opponent
        else:
            diff = diff - self.nearest_fish(state.player, state)
            return diff

    def nearest_fish(self, player, state):
        # 1 - > min  or 0 -> max
        hook_pos = state.hook_positions[player]
        distance = 1000000
        # Iterate all fish positions and get the smallest distance
        for fish in state.fish_positions.values():
            dist = self.distance(fish, hook_pos)
            if dist < distance:
                distance = dist
        return distance

    def distance(self, fish_positions, hook_positions):
        answer = math.sqrt(
            (fish_positions[0]-hook_positions[0])**2 + (fish_positions[1]-hook_positions[1])**2)
        return answer