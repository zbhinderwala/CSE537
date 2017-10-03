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
import random, util

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        "Add more of your code here if you want to"
       # print (legalMoves[chosenIndex])
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        """
        The evaluation function below tries to maximize the score for the action for which the food is closer
        and will reduce the score if the ghost is approaching to the pacman
        """
        manhattanDist = []
        ghostDist = []
        minFoodDist = 0
        minGhostDist = 0
        foodList = newFood.asList()
        # Iterate over all the food points and find their manhattan distance
        for i in range(len(foodList)):
            manhattanDist.append(abs(newPos[0] - foodList[i][0]) + abs(newPos[1] - foodList[i][1]))
        # Get the minimum of all distances i.e closest food
        if manhattanDist:
            minFoodDist = min(manhattanDist)

        if minFoodDist > 0:
            minFoodDist = 10/minFoodDist

        # finding next nearest ghost (not scared ghost) from current position using manhattan distance
        ghostPos = [ghostState for ghostState in newGhostStates if ghostState.scaredTimer == 0]
        for i in range(len(ghostPos)):
            ghostPosition = ghostPos[i].getPosition()
            ghostDist.append(abs(newPos[0] - ghostPosition[0]) + abs(newPos[1] - ghostPosition[1]))
        # Get the minimum of all ghost distances i.e closest ghost
        if ghostDist:
            minGhostDist = min(ghostDist)

        if minGhostDist > 0  :
            minGhostDist  = 10/minGhostDist

        # Maximising the score for the best action and penalising the pacman for Stop action
        score = successorGameState.getScore()
        if action == Directions.STOP:
            score -= 100
        return score + minFoodDist - minGhostDist


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"
        """
        The Minimax agent tries to find the best action for the pacman .This action is decided on the max score of the ghost move.
        The ghost moves are in turn the minimum score of all its actions.
        """
        evaluate = self.evaluationFunction
        maxDepth = self.depth

        #Total number of agents = pacman + ghosts, Max number of ghosts = agents - pacman i.e, agents - 1
        agents = gameState.getNumAgents()
        ghosts = agents - 1

        #The maxMove for the pacman picks up the maximun value of all the minMoves of the ghost for every legal action that is avaialble
        def maxMove(gameState,depth):
            # If terminal state just return the score of the state
            if gameState.isWin() or gameState.isLose() or depth >= maxDepth:
                return evaluate(gameState)

            maxValue = float("-inf")
            legalActions = gameState.getLegalActions(0)
            # Iterate over all the legal actions of Pacman and get the return the max score
            for action in legalActions:
                # For every action of Pacman find the max of minimum score of the next agent i.e ghost with index 1 and at the same depth as pacman
                maxValue = max(maxValue, minMove(gameState.generateSuccessor(0,action),depth,1))
            return maxValue

        #The minMove function for the ghost picks up the minimun value among all actions available in legal actions
        def minMove(gameState,depth,agent):
            # Get the number of ghosts
            ghosts = gameState.getNumAgents() - 1
            # If terminal state just return the score of the state
            if gameState.isWin() or gameState.isLose() or depth >= maxDepth:
                return evaluate(gameState)

            minValue = float("inf")
            # Get all the legal actions of the current ghost agent
            legalActions = gameState.getLegalActions(agent)
            # If it is the last ghost then the minimum value is the score of the Pacman at the next depth
            if agent == ghosts:
                for action in legalActions:
                    minValue = min(minValue, maxMove(gameState.generateSuccessor(agent,action), depth + 1))
            else:
                for action in legalActions:
                    # For every action of ghost find the min score of the next ghost agent at the same depth
                     minValue = min(minValue, minMove(gameState.generateSuccessor(agent, action), depth, agent + 1))
            return minValue

        # Finding the maximum score and best move for the initial state of first Pacman
        legalActions =  gameState.getLegalActions(0)
        actionScores = {}
        # For every action of Pacman get the scores from its successors i.e agent 1 and starting depth is 0
        for action in legalActions:
            actionScores[action] = minMove(gameState.generateSuccessor(0,action),0,1)
        # Of all the scores pick the action corresponding to max score
        bestMove = max(actionScores , key = actionScores.get)

        return bestMove


class AlphaBetaAgent(MultiAgentSearchAgent):


    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """
        The AlphaBeta agent tries to find the best action for the pacman .This action is decided on the max score of the ghost move.
        The ghost moves are in turn the minimum score of all actions.But unlike Minimax it maintains the alpha(Pacman score)
         & beta(Ghost score) values using which the maximum and minimum scores are returned 
        """
        evaluate = self.evaluationFunction
        maxDepth = self.depth

        # Total number of agents = pacman + ghosts, Max number of ghosts = agents - pacman i.e, agents - 1
        agents = gameState.getNumAgents()
        ghosts = agents - 1

        # The maxMove for the pacman picks up the maximun value of all the minMoves for every legal action that is avaialble
        def maxMove(gameState,alpha,beta,depth):
            # If terminal state just return the score of the state
            if gameState.isWin() or gameState.isLose() or depth >= maxDepth:
                return evaluate(gameState)

            maxValue = float("-inf")
            legalActions = gameState.getLegalActions(0)
            # For every action of pacman get the max value of all the minMove of its successor i.e ghost at the same depth
            for action in legalActions:
                maxValue = max(maxValue, minMove(gameState.generateSuccessor(0, action),alpha,beta, depth, 1))
                # If maxValue is more than beta then return this value
                if maxValue > beta:
                    return  maxValue
                # Update alpha with max of maxValue and alpha
                alpha = max(alpha,maxValue)
            return maxValue

        # The minMove function for the ghost picks up the minimun value among all actions available in legal actions
        def minMove(gameState,alpha,beta, depth, agent):
            ghosts = gameState.getNumAgents() - 1
            # If terminal state just return the score of the state
            if gameState.isWin() or gameState.isLose() or depth >= maxDepth:
                return evaluate(gameState)

            minValue = float("inf")
            legalActions = gameState.getLegalActions(agent)
            # For every action of the ghost
            for action in legalActions:
                # If ghost is the last agent then find min of the pacman scores at next depth
                if agent == ghosts:
                    minValue = min(minValue, maxMove(gameState.generateSuccessor(agent, action),alpha,beta, depth + 1))
                else: # Else get the min of all the next ghost actions at the same depth
                    minValue = min(minValue, minMove(gameState.generateSuccessor(agent, action),alpha,beta, depth, agent + 1))
                # If minValue is less than alpha then return minvalue
                if minValue < alpha:
                    return minValue
                # Update beta with min of beta and minValue
                beta = min(beta,minValue)
            return minValue

        # Finding the maximum score and best move for the initial state of first Pacman
        legalActions = gameState.getLegalActions(0)

        # Set alpha as lower bound on Pacman's score and beta is upper bound on Ghost's score
        alpha = float("-inf")
        beta = float("inf")
        currScore = float("-inf")

        # For all the actions in legalActions of Pacman
        for action in legalActions:
            prevScore = currScore
            # Get the max score from the next agent's i,e ghost moves
            currScore = max(currScore, minMove(gameState.generateSuccessor(0, action),alpha,beta,0, 1))
            # If currScore is greater then set the bestMove as this action
            if currScore > prevScore:
                bestMove = action
            # If score is greater than beta then return the bestmove
            if currScore > beta:
                return bestMove
            # Update alpha to max of alpha and currScore
            alpha = max(alpha,currScore)
        return  bestMove


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
        """
        The Expectimax agent tries to find the best action for the pacman .This action is decided on the max score of the ghost move.
        The ghost moves are in turn the average score of all its actions.
        """
        evaluate = self.evaluationFunction
        maxDepth = self.depth

        # Total number of agents = pacman + ghosts, Max number of ghosts = agents - pacman i.e, agents - 1
        agents = gameState.getNumAgents()
        ghosts = agents - 1

        # The maxMove for the pacman picks up the maximun value of all the expectedMoves for every legal action that is avaialble
        def maxMove(gameState,depth):
            # If terminal state just return the score of the state
            if gameState.isWin() or gameState.isLose() or depth >= maxDepth:
                return evaluate(gameState)

            maxValue = float("-inf")
            legalActions = gameState.getLegalActions(0)
            # For every action of Pacman find the max of expected scores of the next agent i.e ghost with index 1 and at the same depth as pacman
            for action in legalActions:
                maxValue = max(maxValue, expectedMove(gameState.generateSuccessor(0,action),depth,1))
            return maxValue

        # The expexted move is calculated by taking the average of all the expected moves( calculated for evry legal action )
        def expectedMove(gameState,depth,agent):
            ghosts = gameState.getNumAgents() - 1
            # If terminal state just return the score of the state
            if gameState.isWin() or gameState.isLose() or depth >= maxDepth:
                return evaluate(gameState)

            expectedValue = 0.0
            legalActions = gameState.getLegalActions(agent)
            # If agent is the last ghost calulate the sum of all score of the Pacman at the next depth
            if agent == ghosts:
                for action in legalActions:
                    expectedValue += maxMove(gameState.generateSuccessor(agent,action), depth + 1)
            else:
                # Else for every action of ghost sum all the expected scores of its successor agents at same depth
                for action in legalActions:
                    expectedValue += expectedMove(gameState.generateSuccessor(agent, action), depth, agent + 1)

            # Return average of all the values as the expectedScore
            return float(expectedValue)/float(len(legalActions))

        # Finding the maximum score and best move for the initial state of first Pacman
        legalActions =  gameState.getLegalActions(0)
        actionScores = {}
        # For every action of Pacman get the scores from its successors i.e agent 1 and starting depth is 0
        for action in legalActions:
            actionScores[action] = expectedMove(gameState.generateSuccessor(0,action),0,1)
        # Get the action corresponding to maximum score
        bestMove = max(actionScores , key = actionScores.get)

        return bestMove


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"


# Abbreviation
better = betterEvaluationFunction

