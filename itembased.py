import csv
import pickle
import numpy as np
from sortedcontainers import SortedList

# load in the data
import os
if not os.path.exists('venv/include/user2categorytokyo.json') or \
   not os.path.exists('venv/include/category2usertokyo.json') or \
   not os.path.exists('venv/include/usercategory2ratingtokyo.json'):
   import preprocess2dict


with open('venv/include/user2categorytokyo.json', 'rb') as f:
  user2category = pickle.load(f)

with open('venv/include/category2usertokyo.json', 'rb') as f:
  category2user = pickle.load(f)

with open('venv/include/usercategory2ratingtokyo.json', 'rb') as f:
  usercategory2rating = pickle.load(f)



N = np.max(list(user2category.keys())) + 1
M = np.max(list(category2user.keys())) +1
print("N:", N, "M:", M)

if M > 247:
  print("N =", N, "are you sure you want to continue?")
  print("Comment out these lines if so...")
  exit()


K = 20
limit = 5
neighbors = []
averages = []
deviations = []

for i in range(M):
  users_i = category2user[i]
  users_i_set = set(users_i)

  ratings_i = { user:usercategory2rating[(user, i)] for user in users_i }
  avg_i = np.mean(list(ratings_i.values()))
  dev_i = { user:(rating - avg_i) for user, rating in ratings_i.items() }
  dev_i_values = np.array(list(dev_i.values()))
  sigma_i = np.sqrt(dev_i_values.dot(dev_i_values))

  averages.append(avg_i)
  deviations.append(dev_i)

  sl = SortedList()
  for j in range(M):
    if j != i:
      users_j = category2user[j]
      users_j_set = set(users_j)
      common_users = (users_i_set & users_j_set)
      if len(common_users) > limit:
        ratings_j = { user:usercategory2rating[(user, j)] for user in users_j }
        avg_j = np.mean(list(ratings_j.values()))
        dev_j = { user:(rating - avg_j) for user, rating in ratings_j.items() }
        dev_j_values = np.array(list(dev_j.values()))
        sigma_j = np.sqrt(dev_j_values.dot(dev_j_values))

        numerator = sum(dev_i[m]*dev_j[m] for m in common_users)
        w_ij = numerator / (sigma_i * sigma_j)


        sl.add((-w_ij, j))
        if len(sl) > K:
          del sl[-1]

  neighbors.append(sl)

  if i % 1 == 0:
    print(i)




def predict(i, u):
  numerator = 0
  denominator = 0
  for neg_w, j in neighbors[i]:
    try:
      numerator += -neg_w * deviations[j][u]
      denominator += abs(neg_w)
    except KeyError:
      pass

  if denominator == 0:
    prediction = averages[i]
  else:
    prediction = numerator / denominator + averages[i]
  return prediction



predictionArray = []
train_predictions = []
train_targets = []
for (u, m), target in usercategory2rating.items():
    prediction = predict(m,u)
    predictionArray.append([u, m, target , prediction])
    print("prediction", prediction, u, m)
    if (target == 0):
        train_predictions.append(prediction)
        train_targets.append(target)

with open('venv/include/predictionTokyoItem.csv', 'w') as file:
  writer = csv.writer(file, delimiter=',')
  writer.writerow(["userId","categoryId","target","prediction"])
  for item in predictionArray:
    writer.writerow(item)


# calculate accuracy
def mse(p, t):
  p = np.array(p)
  t = np.array(t)
  return np.mean((p - t)**2)

print('train mse:', mse(train_predictions, train_targets)),
print(len(train_predictions),len(train_targets))
