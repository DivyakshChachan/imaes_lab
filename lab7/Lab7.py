import matplotlib.pyplot as plt

# ==================================================
# 1. PROPOSITIONAL LOGIC
# Rule: If it rains, then the road is wet.
# ==================================================

print("1. PROPOSITIONAL LOGIC")

print("Rain | Road Wet | Rain -> Road Wet")

for rain in [True, False]:
    for road_wet in [True, False]:
        result = (not rain) or road_wet
        print(rain, " | ", road_wet, " | ", result)


# ==================================================
# 2. FIRST-ORDER LOGIC
# All humans are mortal.
# Socrates is a human.
# Therefore, Socrates is mortal.
# ==================================================

print("\n2. FIRST-ORDER LOGIC")

humans = ["Socrates"]

def is_mortal(person):
    return person in humans

person = "Socrates"

if is_mortal(person):
    print(person, "is mortal.")
else:
    print(person, "is not known to be mortal.")


# ==================================================
# 3. PROBABILITY OF EVENTS
# Dataset of 10 students
# ==================================================

print("\n3. PROBABILITY OF EVENTS")

total = 10

# Event A: Student passed
passed = 6

# Event B: Student attended classes
attended = 7

# Students who both passed and attended
passed_and_attended = 5

P_A = passed / total
P_B = attended / total
P_A_and_B = passed_and_attended / total

# P(A union B) = P(A) + P(B) - P(A intersection B)
P_A_or_B = P_A + P_B - P_A_and_B

print("P(A) - Probability of passing:", P_A)
print("P(B) - Probability of attendance:", P_B)
print("P(A and B) - Joint probability:", P_A_and_B)
print("P(A or B) - Union probability:", P_A_or_B)


# ==================================================
# 4. CONDITIONAL PROBABILITY
# P(A|B) and P(B|A)
# ==================================================

print("\n4. CONDITIONAL PROBABILITY")

# Probability of passing given attendance
P_A_given_B = P_A_and_B / P_B

# Probability of attendance given passing
P_B_given_A = P_A_and_B / P_A

print("P(A|B) - Probability of passing given attendance:",
      P_A_given_B)

print("P(B|A) - Probability of attendance given passing:",
      P_B_given_A)


# ==================================================
# 5. BAYES' THEOREM
# Disease diagnosis example
# ==================================================

print("\n5. BAYES' THEOREM")

# Probability of having the disease
P_D = 0.01

# Probability of a positive test given disease
P_positive_given_D = 0.90

# Probability of a positive test without disease
P_positive_given_not_D = 0.05

# Total probability of a positive test
P_positive = (
    P_positive_given_D * P_D
    + P_positive_given_not_D * (1 - P_D)
)

# Bayes' theorem
P_D_given_positive = (
    P_positive_given_D * P_D / P_positive
)

print("Probability of disease given a positive test:",
      round(P_D_given_positive, 4))

print("Percentage:",
      round(P_D_given_positive * 100, 2), "%")


# ==================================================
# 6. VISUALIZATION
# ==================================================

print("\n6. VISUALIZATION")

probabilities = {
    "P(A)": P_A,
    "P(B)": P_B,
    "P(A and B)": P_A_and_B,
    "P(A or B)": P_A_or_B,
    "P(A|B)": P_A_given_B,
    "P(B|A)": P_B_given_A,
    "Bayes Result": P_D_given_positive
}

plt.figure(figsize=(10, 5))

plt.bar(
    probabilities.keys(),
    probabilities.values()
)

plt.title("Visualization of Calculated Probabilities")
plt.xlabel("Probability Events")
plt.ylabel("Probability")
plt.ylim(0, 1)

plt.xticks(rotation=30)
plt.tight_layout()
plt.show()