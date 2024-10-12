from OpenAiGymSolitaireClass import OpenAiGymSolitaireClass

def test_model(env, num_games=100):
    total_rewards = 0
    max_reward = -1000
    for game in range(num_games):
        state = env.reset()
        state = env.get_state()
        game_reward = 0
        done = False

        while not done:
            action = env.get_action(state)
            observation, reward, terminated, truncated, _ = env.step(action)
            next_state = env.get_state()
            game_reward += reward

            state = next_state
            done = terminated or truncated

        total_rewards += game_reward
        max_reward = max(max_reward, game_reward)
        print(f"Game {game + 1} completed. Reward: {game_reward}")

    average_reward = total_rewards / num_games
    print(f"\nTested {num_games} games.")
    print(f"Average Reward: {average_reward}")
    print(f"Max Reward: {max_reward}")

if __name__ == "__main__":
    # Create environment and load the trained model
    env = OpenAiGymSolitaireClass(verbose=True)
    env.load_model("solitaire_model.pkl")

    # Test the loaded model
    test_model(env)

    env.close()