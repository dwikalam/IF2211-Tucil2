import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets
from convexhull.convexHull import convexHull

print("Welcome to simple program for determining Convex Hull of data")

menu = 0
subMenu = 0
isMenuValid = False
while (not isMenuValid):
    print("What dataset do you want to use?")
    print("1. Iris")
    print("2. Diabetes")
    print("3. California Housing")

    try:
        menu = int(input("Dataset: "))
        assert menu in (1, 2, 3)          
    except ValueError:
        print("\nInvalid input. The input has to be either 1, 2, or 3\n")
    except AssertionError:
        print("\nInvalid input. The input has to be either 1, 2, or 3\n")
    else:
        isMenuValid = True

dataSet_targetName = ["flowerType", "disease-progression", "median-HouseValue(in-$100,000)"]
targetValueBoundaries = [[0,1,2], [0, 100,200], [0, 2]]
plt.figure(figsize = (10, 6))

if (menu == 1):
    data = datasets.load_iris()
    df = pd.DataFrame(data.data, columns = data.feature_names)
    df[dataSet_targetName[0]] = data.target

    isSubMenuValid = False
    while (not isSubMenuValid):
        print("\nWhat to consider?")
        print("1. Sepal-Length vs Sepal-Width")
        print("2. Petal-Length vs Petal-Width")
            
        try:
            subMenu = int(input("Select: "))
            assert subMenu in (1, 2)         

        except ValueError:
            print("\nSelect the valid number! The number has to be either 1 or 2")
        except AssertionError:
            print("\nSelect the valid number! The number has to be either 1 or 2")
        else:
            isSubMenuValid = True
    
    if (subMenu == 1):
        plt.title("Sepal-Length vs Sepal-Width")
        plt.xlabel(data.feature_names[0])
        plt.ylabel(data.feature_names[1])
    else:
        plt.title("Petal-Length vs Petal-Width")
        plt.xlabel(data.feature_names[2])
        plt.ylabel(data.feature_names[3])

elif (menu == 2):
    data = datasets.load_diabetes()
    df = pd.DataFrame(data.data, columns = ["age", "sex", "bmi", "bp", "tc", "ldl", "hdl", "tch", "ltg", "glu"])
    df[dataSet_targetName[1]] = data.target
    plt.title("Avg Blood Pressure (bp) vs Blood Sugar (glu) Level")
    plt.xlabel(df.columns[3])
    plt.ylabel(df.columns[9])

else:
    data = datasets.fetch_california_housing()
    df = pd.DataFrame(data.data, columns = data.feature_names)
    df[dataSet_targetName[2]] = data.target
    plt.title("Median Income vs Population \n per Block Group", multialignment = "center")
    plt.xlabel("Median Income")
    plt.ylabel("Population")

hull = convexHull()
hull_points = []
idx = menu -1

# Determine The Convex Hull
for value in targetValueBoundaries[idx]:
    # ...
    if (menu == 1):
        bucket = df[df[dataSet_targetName[idx]] == value]
        if (subMenu == 1):
            bucket = bucket.iloc[:, [0,1]].values # [[x1, y1], [x2, y2], [x3, y3], ...]
        else:
            bucket = bucket.iloc[:, [2,3]].values
        
        labelName = data.target_names[value]

    elif (menu == 2):
        if (value != 200):        
            bucket = df[df[dataSet_targetName[idx]].between(value, value+100, 'left')]
            labelName = str(value) + " <= " + dataSet_targetName[idx] + " < " + str(value+100)
        else:
            bucket = df[df[dataSet_targetName[idx]] >= value]
            labelName =  dataSet_targetName[idx] + " >= " + str(value)
        
        bucket = bucket.iloc[:, [3,9]].values
    
    else:
        if (value != 2):        
            bucket = df[df[dataSet_targetName[idx]].between(0, value+2, 'left')]
            labelName = str(value) + " <= " + dataSet_targetName[idx] + " < " + str(value+2)
        else:
            bucket = df[df[dataSet_targetName[idx]] >= value]
            labelName =  dataSet_targetName[idx] + " >= " + str(value)

        bucket = bucket.iloc[:, [0,4]].values
    
    # Determine ConvexHull of current bucket
    hull_points = hull.get_hull(bucket)

    # Plotting points to the diagram
    plt.scatter(bucket[:, 0], bucket[:,1], label = labelName)
    plt.plot(hull_points[0], hull_points[1])
    
plt.legend()
plt.show()