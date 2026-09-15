"""
Decision Tree Lab - Starter Code
=================================
Dataset: "Should I play tennis today?" (a classic tiny teaching dataset)
Each row is a PAST DAY with known weather conditions and whether tennis
was played. This is our LABELED training data -> supervised learning.

Fill in the TODOs. Estimated time: 10-12 minutes.
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.preprocessing import OrdinalEncoder
import matplotlib.pyplot as plt

# -----------------------------------------------------------------
# 1. THE LABELED DATA
# -----------------------------------------------------------------


data = pd.DataFrame({
    "outlook":     ["sunny", "sunny", "overcast", "rain", "rain", "rain",
                     "overcast", "sunny", "sunny", "rain", "sunny",
                     "overcast", "overcast", "rain"],
    "temperature": ["hot", "hot", "hot", "mild", "cool", "cool", "cool",
                     "mild", "cool", "mild", "mild", "mild", "hot", "mild"],
    "humidity":    ["high", "high", "high", "high", "normal", "normal",
                     "normal", "high", "normal", "normal", "normal",
                     "high", "normal", "high"],
    "windy":       [False, True, False, False, False, True, True, False,
                     False, False, True, True, False, True],
    "play_tennis": ["no", "no", "yes", "yes", "yes", "no", "yes", "no",
                     "yes", "yes", "yes", "yes", "yes", "no"],
})

print("Training data (this is what makes it SUPERVISED learning:")
print("every row has an input AND the correct answer/label):\n")
print(data)

from sklearn.datasets import load_iris
iris = load_iris()
data = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)
data["species"] = iris.target_names[iris.target]

# -----------------------------------------------------------------
# 2. TODO #1: Separate inputs (features) from the label (target)
# -----------------------------------------------------------------
# The model needs to learn a function: features -> label
# X = the columns the model is allowed to look at
# y = the column it's trying to predict
X = data.drop(columns=["species"])   # TODO: is this right? check it.
print(X)
y = data["species"] 
print(y)                 # TODO: is this right? check it.

# Decision trees in sklearn need numbers, not text, so we encode.
encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X)


print(X_encoded)

# -----------------------------------------------------------------
# 3. TODO #2: Create and train ("fit") the model
# -----------------------------------------------------------------
# .fit(X, y) is the moment "learning" happens: the tree searches for
# the sequence of yes/no questions about X that best predicts y.
clf = DecisionTreeClassifier(max_depth=10, random_state=42)
clf.fit(X_encoded, y)          # TODO: call fit with the right arguments

# -----------------------------------------------------------------
# 4. Look at what it learned
# -----------------------------------------------------------------
feature_names = list(X.columns)
print("\nLearned decision rules:\n")
print(export_text(clf, feature_names=feature_names))

plt.figure(figsize=(10, 6))
plot_tree(clf, feature_names=feature_names, class_names=clf.classes_,
          filled=True, rounded=True, fontsize=9)
plt.title("Decision Tree: Should I Play Tennis?")
plt.tight_layout()
plt.savefig("tennis_tree.png", dpi=150)
print("\nSaved a picture of the tree to tennis_tree.png")

# -----------------------------------------------------------------
# 5. TODO #3: Predict on a NEW day the model has never seen
# -----------------------------------------------------------------
# This is the payoff of supervised learning: generalizing to new,
# unlabeled examples using the pattern learned from labeled ones.

new_flower = pd.DataFrame({
    "sepal length (cm)": [6],
    "sepal width (cm)": [3],
    "petal length (cm)": [5],
    "petal width (cm)": [2],
})
new_flower_encoded = encoder.transform(new_flower)
prediction = clf.predict(new_flower_encoded)   # TODO: predict on new_flower_encoded

print(f"\nNew flower: {new_flower.to_dict(orient='records')[0]}")
print(f"Prediction: species = {prediction[0]}")


#new_day = pd.DataFrame({
#   "outlook": ["sunny"],
#   "temperature": ["cool"],
#  "humidity": ["normal"],
# "windy": [True],
#})
#new_day_encoded = encoder.transform(new_day)
#prediction = clf.predict(new_day_encoded)   # TODO: predict on new_day_encoded

#print(f"\nNew day: {new_day.to_dict(orient='records')[0]}")
#print(f"Prediction: play_tennis = {prediction[0]}")


# -----------------------------------------------------------------
# 6. STRETCH GOAL (if time remains)
# -----------------------------------------------------------------
# Try changing max_depth to 1, then to 10. Re-run and compare the
# tree diagrams and the training accuracy. What happens? Why?
#1. The thing that makes this task supervised rather than unsupervised is because 
# we already know the right answers with the label, while in unsupervised learning there are no labels at all.
#2. If we added the new feature "day of the week" to the dataset, I think the tree could use this to determine what day of the 
# week people are playing tennis the most which would add to the original question of "Should I play tennis today?"
#3. A very deep, perfectly accurate tree would be a worse model in practice than a shallower, slightly less accurate one 
# because it is not realistic. In real life, there is randomness that can change the outcomes of things.
#4. Another real-world decision that could be modeled as a decision tree could be deciding if 
# you should go swimming. The features would be outlook, temperature, season, and current and the label would be went_swimming.
# accuracy = clf.score(X_encoded, y)
# print(f"Training accuracy: {accuracy:.2%}")
