

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

