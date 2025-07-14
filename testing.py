
students = ["John", "Lisa", "Chris", "Linda", "Matt"]

test_performance = {
    "John": 87,
    "Lisa": 90,
    "Mary": 75,
    "Chris": 100,
    "Linda": 100,
    "Matt": 70
}

scores = []

for student in students:
    scores.append(test_performance[student])

def bubble_sort(scores):
    return sorted(scores)

sorted_scores = bubble_sort(scores)

print(sorted_scores)