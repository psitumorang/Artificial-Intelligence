# Include your imports here, if any are used.

student_name = "Philip Situmorang"

# 1. Value Iteration
class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.discount = discount
        self.states_values = {}
        
        # initialize states values to 0
        for state in game.states:
            self.states_values[state] = 0

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        return self.states_values[state]

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        qsum = 0
        transitions = self.game.get_transitions(state, action)
        for t in transitions:
            if t in self.game.states:
                q = transitions[t] * ((self.game.get_reward(state, action, t)) + self.discount * self.states_values[t])
                qsum += q
            else:
                q = transitions[t] * (self.game.get_reward(state, action, t))
                qsum += q
        return qsum 

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        max_action = None
        max_q = None
        for action in self.game.Action:
            q = self.get_q_value(state, action)
            if max_q is None:
                max_q = q
                max_action = action
            elif q > max_q:
                max_q = q
                max_action = action
        return max_action  # TODO

    def iterate(self):
        """Run single value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        for state in self.states_values:
            best_policy = self.get_best_policy(state)
            q = self.get_q_value(state, best_policy)
            self.states_values[state] = q

# 2. Policy Iteration
class PolicyIterationAgent(ValueIterationAgent):
    """Implement Policy Iteration Agent.

    The only difference between policy iteration and value iteration is at
    their iteration method. However, if you need to implement helper function or
    override ValueIterationAgent's methods, you can add them as well.
    """

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.discount = discount
        self.states_values = {}
        
        # initialize states values to 0
        for state in game.states:
            self.states_values[state] = 0

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        return self.states_values[state]

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        qsum = 0
        transitions = self.game.get_transitions(state, action)
        for t in transitions:
            if t in self.game.states:
                q = transitions[t] * ((self.game.get_reward(state, action, t)) + self.discount * self.states_values[t])
                qsum += q
            else:
                q = transitions[t] * (self.game.get_reward(state, action, t))
                qsum += q
        return qsum 

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        max_action = None
        max_q = None
        for action in self.game.Action:
            q = self.get_q_value(state, action)
            if max_q is None:
                max_q = q
                max_action = action
            elif q > max_q:
                max_q = q
                max_action = action
        return max_action  # TODO

    def iterate(self):
        """Run single policy iteration.
        Fix current policy, iterate state values V(s) until |V_{k+1}(s) - V_k(s)| < ε
        """
        epsilon = 1e-6
        
        pi = {}
        for state in self.states_values:
            pi[state] = self.get_best_policy(state)
        
        pi_plus_1 ={}
        
        while True:
            for state in self.states_values:
                while abs(self.get_q_value(state, pi[state])- self.get_value(state)) > epsilon:
                    q = self.get_q_value(state, pi[state])
                    self.states_values[state] = q
            
            for state in self.states_values:
                best_policy = self.get_best_policy(state)
                pi_plus_1[state] = best_policy
                
            if pi == pi_plus_1:
                break
            else:
                pi = pi_plus_1

# 3. Bridge Crossing Analysis
def question_3():
    discount = 0.9
    noise = 0.01
    return discount, noise

# 4. Policies
def question_4a():
    discount = 0.9
    noise = 0.1
    living_reward = -3
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = 0.5
    noise = 0.4
    living_reward = -2 
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = 0.9
    noise = 0.1
    living_reward = -1
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = 0.9
    noise = 0.1
    living_reward = 0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = 0.9
    noise = 0.2
    living_reward = 20
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'

# 5. Feedback
# Just an approximation is fine.
feedback_question_1 = 10

feedback_question_2 = """
Very hard to figure out in the beginning how to set up the homework. The guidelines were vague in helping make sense of the initial setup.
"""

feedback_question_3 = """
Type of algorithm learned was pretty good. Once the hurdle of the initial setup was over the assignment was relatively straightforward.
"""
