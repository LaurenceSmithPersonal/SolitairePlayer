# ... (keep existing imports)
import numpy as np

class OpenAiGymSolitaireClass(Env):
    # ... (keep existing code)

    def __init__(self, render_mode="ansi") -> None:
        # ... (keep existing initialization)

        # Add Q-learning components
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1

    # ... (keep existing methods)

    def get_state(self):
        # Convert the current game state to a hashable representation
        return tuple(map(tuple, self.positionClass_to_observation()))

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return self.action_space.sample()
        else:
            if state not in self.q_table:
                self.q_table[state] = np.zeros(self.action_space.n)
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_space.n)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.action_space.n)

        current_q = self.q_table[state][action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def train(self, num_episodes):
        for episode in range(num_episodes):
            state = self.get_state()
            total_reward = 0
            done = False

            while not done:
                action = self.get_action(state)
                observation, reward, terminated, truncated, _ = self.step(action)
                next_state = self.get_state()
                total_reward += reward

                self.update_q_table(state, action, reward, next_state)

                state = next_state
                done = terminated or truncated

            if episode % 100 == 0:
                print(f"Episode {episode}, Total Reward: {total_reward}")

            self.reset()

        print("Training completed.")

if __name__ == "__main__":
    # ... (keep existing code)

    # Add training code
    env = OpenAiGymSolitaireClass()
    env.train(num_episodes=10000)

    # Test the trained agent
    state = env.get_state()
    total_reward = 0
    done = False

    while not done:
        action = env.get_action(state)
        observation, reward, terminated, truncated, _ = env.step(action)
        next_state = env.get_state()
        total_reward += reward

        state = next_state
        done = terminated or truncated

    print(f"Test game completed. Total Reward: {total_reward}")
    env.close()