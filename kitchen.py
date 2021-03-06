import os
import time
import graphlib
from collections import defaultdict
import copy

# {food name, its graph(dictionary:name to requirement)}
foods_recipes = {}
# list all foods
food_menu = []
# {all recipes, preparation time}
food_prep = {}

FILE_NAME = "TestDataKianAdrina"


def initialize():
    # graph initialize
    graph = defaultdict(set)
    # read recipes from file
    with open(os.path.join("Food Recipes", FILE_NAME + ".txt"), "r") as food_input:
        new_food = False
        for line in food_input:
            line = line.strip()

            if line == "New Food:":
                new_food = True
                continue

            if line == "End of instructions":
                # add graph for first food
                foods_recipes[food_menu[-1]] = copy.deepcopy(graph)
                graph.clear()
                continue

            if new_food:
                new_food = False
                # add food name to menu
                food_menu.append(line)

            else:
                # read a line of instruction
                data, temp_food = line.split(), list()
                time_prep = 0

                for food in data[1:]:
                    if not food.isdigit():
                        # add food to graph dict
                        graph[data[0]].add(food)
                        # to calculate all requirements
                        temp_food.append(food)
                    else:
                        # add time to total time
                        time_prep += int(food)

                for tp in temp_food:
                    # get preparation time of each food
                    time_prep += food_prep.get(tp, 0)

                # add time and food name to a dict
                food_prep[data[0]] = time_prep


# calculate time of reading file and call initialize
def start():
    os.system("cls")
    print("Loading Food Recipes... Please Wait")
    start_time = time.time()
    initialize()
    print(f"File Loaded!\nTime = {time.time() - start_time}s")
    input("\nPress Enter to continue")


def main():
    # start()
    os.system("cls")
    print("Please wait for seconds")

    # find the time needed for our main food
    main_food_prep = dict(filter(lambda l: l[0] in food_menu, food_prep.items()))
    # find the requirements for our main food
    main_food_rec = dict(filter(lambda l: l[0] in food_menu, foods_recipes.items()))

    while True:

        os.system("cls")

        if not len(food_menu):
            print("There's no food in our menu!\nThanks for coming :)")
            exit(0)

        print("\n-------------------- Welcome to Kitchen of Kharkhon Bashi Restaurant ---------------------\n")
        print("\n1. Show Foods\n")
        print("\n2. Delete a Food\n")
        print("\n3. Show Food Recipes\n")
        print("\n4. Add a requirement to the food\n")
        print("\n5. Get the food with the most time needed\n")
        print("\n6. Get the food with the least time needed\n")
        print("\n7. Get the food with the most requirements\n")
        print("\n8. Exit\n")
        print("\n-------------------------------------------------------------------------------------------\n")

        try:
            selection = int(input("\nPlease enter a number: "))

            # show menu
            if selection == 1:
                print("\nFood\tTime")
                print("-------------------")

                # get food and time need
                for foods in food_menu:
                    print(foods, "\t", food_prep[foods])

                input("\nPress Enter to go back to menu")

            # delete food
            elif selection == 2:
                print("\nFood\tTime")
                print("-------------------")
                for foods in food_menu:
                    print(foods, "\t", food_prep[foods])

                food_name_to_delete = input("Enter a food name to delete: ")

                if food_name_to_delete not in food_menu:
                    input("The name food you entered is not in menu!")
                    continue

                # open file for reading and writing
                with open(os.path.join("Food Recipes", FILE_NAME + ".txt"), "r") as src, \
                        open(os.path.join("Food Recipes", FILE_NAME + "edited.txt"), "w") as dest:

                    # two flag for finding food
                    new_food_src, food_found = False, False
                    for line_src in src:
                        # remove whitespace from beginning and end of the line
                        line_src = line_src.strip()

                        # new food detected
                        if line_src == "New Food:":
                            new_food_src, food_found = True, False
                            continue

                        # end of recipes
                        if line_src == "End of instructions":
                            # if food couldn't be found write the end
                            if not food_found:
                                dest.write("End of instructions\n")
                            continue

                        # new food detected
                        if new_food_src:
                            new_food_src = False
                            # if food name found
                            if line_src == food_name_to_delete:
                                food_found = True
                            # if didn't find copy file
                            else:
                                dest.write("New Food:\n")
                                dest.write(line_src + "\n")

                        # food didn't find
                        else:
                            if not food_found:
                                dest.write(line_src + "\n")

                # remove former file
                os.remove(os.path.join("Food Recipes", FILE_NAME + ".txt"))
                # rename the new file with the last name
                os.rename(os.path.join("Food Recipes", FILE_NAME + "edited.txt"),
                          os.path.join("Food Recipes", FILE_NAME + ".txt"))

                # clear all data and reload it
                foods_recipes.clear()
                food_menu.clear()
                food_prep.clear()
                main_food_prep.clear()
                main_food_rec.clear()
                start()
                print("Please wait for seconds")

                # find the time needed for our main food
                main_food_prep = dict(filter(lambda l: l[0] in food_menu, food_prep.items()))
                # find the requirements for our main food
                main_food_rec = dict(filter(lambda l: l[0] in food_menu, foods_recipes.items()))

            # show food recipes
            elif selection == 3:
                print()
                # for each food do topological sort for recipes
                for fdr in food_menu:
                    try:
                        print(fdr, "--->", *graphlib.TopologicalSorter(foods_recipes[fdr]).static_order())
                    # if cycle detected raise error
                    except graphlib.CycleError as gce:
                        print("Cycle detected!", gce)

                input("\nPress Enter to go back to menu")

            # add requirement to a food
            elif selection == 4:
                print("\nFood\tTime")
                print("-------------------")
                # show menu
                for foods in food_menu:
                    print(foods, "\t", food_prep[foods])

                # get food name
                food_name = input("Enter a food name: ")
                # get a line of requirement
                req = input("Enter a line of requirement: ").split()

                try:
                    # add requirement to graph dict of food
                    foods_recipes[food_name][req[0]].add(req[1])
                    # calculate time
                    tmp = int(req[2])
                    # add time food to new time
                    tmp += food_prep.get(req[1], 0)
                    # add new time to our dict of food
                    food_prep[req[0]] += tmp
                    print("Successfully added!")

                except KeyError as ke:
                    print(ke, "Not found!!")

                input("\nPress Enter to go back to menu")

            # get the food with the most time needed
            elif selection == 5:
                print("\nFood\tTime")
                print("-------------------")
                # find the maximum food time
                maximum = max(main_food_prep, key=main_food_prep.get)
                print(maximum, "\t", main_food_prep[maximum])
                input("\nPress Enter to go back to menu")

            # get the food with the least time needed
            elif selection == 6:
                print("\nFood\tTime")
                print("-------------------")
                # find the minimum food time
                minimum = min(main_food_prep, key=main_food_prep.get)
                print(minimum, "\t", main_food_prep[minimum])
                input("\nPress Enter to go back to menu")

            # get the food with most requirement
            elif selection == 7:
                maximum_rec_count, maximum_rec_names = 0, []

                # get len of requirement
                for k, v in main_food_rec.items():
                    len_v = len(tuple(graphlib.TopologicalSorter(v).static_order()))

                    # find bigger requirements
                    if len_v > maximum_rec_count:
                        maximum_rec_names.clear()
                        maximum_rec_names.append(k)
                        maximum_rec_count = len_v

                    # if there are more than one show all
                    elif len_v == maximum_rec_count:
                        maximum_rec_names.append(k)

                # show food name and its requirements
                for name in maximum_rec_names:
                    print("\nFood name ---> ", name)
                    print(*graphlib.TopologicalSorter(foods_recipes[name]).static_order())

                input("\nPress Enter to go back to menu")

            # exit
            elif selection == 8:
                print("GoodBye!")
                print("by: Kian & Adrina")
                exit(0)

        except ValueError:
            input("\nOops!  That was no valid number.  Try again...")


if __name__ == "__main__":
    main()
