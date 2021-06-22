# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util
import math

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def agentCounter(gameState, index, depth):
            """When index is out of bounds return pacmans index and
            reduce depth by 1"""
            if index == gameState.getNumAgents():
                return [depth-1, 0]
            else:
                return [depth, index]

        def minimax(self, gameState, depth, index):
            """Implement minimax function for pacman game. 
                return an array with score and best move"""
            ultimateMove = None  # The best move the agent can use
            if depth == 0 or gameState.isWin() or gameState.isLose():
                # if leaf node return value.
                return [self.evaluationFunction(gameState), ultimateMove]
            else:
                if index == 0:  # if pacman => agent is max agent
                    value = -math.inf
                    maxValue = value
                    # iterates through max agent w/index=0 moves
                    for action in gameState.getLegalActions(0):
                        depthIndex = agentCounter(gameState, index+1, depth)
                        successorState = gameState.generateSuccessor(
                            index, action)  # generates the next state when move is done
                        value = max(value, minimax(
                            self, successorState, depthIndex[0], depthIndex[1])[0])  # return max of saved value and recursive function
                        if maxValue != value:  # If value has changed update values
                            ultimateMove = action
                            maxValue = value
                    return [value, ultimateMove]
                else:  # is ghost => agent is min agent
                    value = math.inf
                    minValue = value
                    # Iterate through the moves of a min agent w/index not 0
                    for action in gameState.getLegalActions(index):
                        depthIndex = agentCounter(gameState, index+1, depth)
                        successorState = gameState.generateSuccessor(
                            index, action)
                        value = min(value, minimax(
                            self, successorState, depthIndex[0], depthIndex[1])[0])  # return min of saved value and recursive function
                        if minValue != value:  # If value has changed update values
                            ultimateMove = action
                            minValue = value
                    return [value, ultimateMove]

        best = minimax(self, gameState, self.depth, self.index)
        #print("Move: ", best[1], " | Score: ", best[0])
        return best[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth, a, b):
            """Implementation of a=aplha, b=beta pruning in maximizing agent"""
            ultimateMove = None  # The best move the agent can do
            if gameState.isWin() or gameState.isLose():  # if terminal node return gamescore
                return self.evaluationFunction(gameState)
            bestValue = -math.inf
            # for all of max agents moves
            for action in gameState.getLegalActions(0):
                value = minValue(gameState.generateSuccessor(
                    0, action), depth, 1, a, b)  # save value from call to minimizing agent
                if value > bestValue:  # if value has increased, update parametres
                    bestValue = value
                    ultimateMove = action
                a = max(a, bestValue)  # updates a=alpha if bestvalue > alpha
                if bestValue > b:  # if value is greater than connected branch, do prune
                    return bestValue
            if depth == self.depth:  # if top node, return the best move
                return ultimateMove
            else:
                # if not top node (and no pruning) return best value
                return bestValue

        def minValue(gameState, depth, agentCounter, a, b):
            """Implementation of a=aplha, b=beta pruning in minimizing agent"""
            changeToMax = False
            if gameState.isWin() or gameState.isLose():  # if terminal node return gamescore
                return self.evaluationFunction(gameState)
            if agentCounter == gameState.getNumAgents() - 1:  # if last min agent, next call should be max agent
                changeToMax = True
            bestValue = math.inf
            # for all of one min agents moves
            for action in gameState.getLegalActions(agentCounter):
                if changeToMax:  # if next agent is max agent
                    # if next node is leaf node, save score of leaf node (no need to call max agent)
                    if depth == 1:
                        value = self.evaluationFunction(
                            gameState.generateSuccessor(agentCounter, action))
                    else:  # else call max agent at lower depth
                        value = maxValue(
                            gameState.generateSuccessor(agentCounter, action), depth-1, a, b)
                else:  # next agent is min agent, next call to other min agent
                    value = minValue(gameState.generateSuccessor(
                        agentCounter, action), depth, agentCounter + 1, a, b)
                if value < bestValue:  # if lower value, update value
                    bestValue = value
                # update b=beta to lowest value of branch
                b = min(b, bestValue)
                if bestValue < a:  # if value is lower than connected branch, do prune
                    return bestValue
            return bestValue  # if no pruning, return best value

        Move = maxValue(gameState, self.depth, -math.inf, math.inf)
        #print("Move: ", Move)
        return Move


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
