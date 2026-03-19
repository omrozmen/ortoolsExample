"""Solves a simple assignment problem."""
from ortools.sat.python import cp_model
import os 



def main() -> None:
    # Data
    costs = [
        [90, 76, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 105],
        [45, 110, 95, 115],
        [60, 105, 80, 75],
        [45, 65, 110, 95],
    ]
    num_workers = len(costs)
    num_tasks = len(costs[0])

    team1 = [0, 2, 4]
    team2 = [1, 3, 5]
    # Maximum total of tasks for any team
    team_max = 2

    # Model
    model = cp_model.CpModel()

    # Variables
    x = {}
    for worker in range(num_workers):
        for task in range(num_tasks):
            x[worker, task] = model.new_bool_var(f"x[{worker},{task}]")

    # Constraints
    # Each worker is assigned to at most one task.
    for worker in range(num_workers):
        model.add_at_most_one(x[worker, task] for task in range(num_tasks))

    # Each task is assigned to exactly one worker.
    for task in range(num_tasks):
        model.add_exactly_one(x[worker, task] for worker in range(num_workers))

    # Each team takes at most two tasks.
    team1_tasks = []
    for worker in team1:
        for task in range(num_tasks):
            team1_tasks.append(x[worker, task])
    model.add(sum(team1_tasks) <= team_max)

    team2_tasks = []
    for worker in team2:
        for task in range(num_tasks):
            team2_tasks.append(x[worker, task])
    model.add(sum(team2_tasks) <= team_max)

    # Objective
    objective_terms = []
    for worker in range(num_workers):
        for task in range(num_tasks):
            objective_terms.append(costs[worker][task] * x[worker, task])
    model.minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Total cost = {solver.objective_value}\n")
        for worker in range(num_workers):
            for task in range(num_tasks):
                if solver.boolean_value(x[worker, task]):
                    print(
                        f"Worker {worker} assigned to task {task}."
                        + f" Cost = {costs[worker][task]}"
                    )
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()