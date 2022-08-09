# suitsToUnicode = {
#     "clubs": u'\u2663'
#     ,"diamonds": u'\u2666'
#     ,"hearts": u'\u2665'
#     ,"spades": u'\u2660'
# }

# print(suitsToUnicode.keys())
# print(suitsToUnicode.values())

# print("hello \u2660")
       
# print("{0}{1}".format("A",suitsToUnicode["clubs"]))

# print(type(u'\u2660'))

#import pandas as pd

#deckDetails = pd.read_csv("deckdetails.csv")

#print(deckDetails)

#print(chr(deckDetails["SuitUnicode"][0]))
#print(("u'"+str(deckDetails["SuitUnicode"][0]+"'")).decode("utf-8"))

#print(2663.decode("utf-8"))

# print("clubs: ", ord('\u2663'))
# print("diamonds: ", ord('\u2666'))
# print("hearts: ", ord('\u2665'))
# print("spades: ", ord('\u2660'))
# print("A"+chr(9824))

# OpenAI Gym example:
import gym
env = gym.make("BreakoutNoFrameskip-v4")

print("Observation Space: ", env.observation_space)
print("Action Space       ", env.action_space)


obs = env.reset()

for i in range(1000):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
    time.sleep(0.01)
env.close()
