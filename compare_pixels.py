import sys
import csv

def read_file(filename):
    data = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                x, y, value = map(int, row)
                data[(x, y)] = value
    return data

def compare_files(file1, file2):
    data1 = read_file(file1)
    data2 = read_file(file2)

    all_coords = set(data1.keys()).union(set(data2.keys()))
    
    differences = []
    comparison_count = 0

    for coord in all_coords:
        val1 = data1.get(coord, None)
        val2 = data2.get(coord, None)
        comparison_count += 1
        if val1 != val2:
            differences.append((coord, val1, val2))
    
    return differences, comparison_count

def save_differences(differences, file1_name, file2_name):
    file1_differences = []
    file2_differences = []

    for coord, val1, val2 in differences:
        if val1 is not None:
            file1_differences.append((coord[0], coord[1], val1))
        if val2 is not None:
            file2_differences.append((coord[0], coord[1], val2))

    # Write differences for File 1
    with open(file1_name, 'w') as f1:
        writer = csv.writer(f1)
        for row in file1_differences:
            writer.writerow(row)

    # Write differences for File 2
    with open(file2_name, 'w') as f2:
        writer = csv.writer(f2)
        for row in file2_differences:
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_coordinates.py <file1.txt> <file2.txt>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    differences, comparison_count = compare_files(file1, file2)

    if differences:
        print("Differences found:")
        for coord, val1, val2 in differences:
            print(f"Coordinate {coord}: File1 value = {val1}, File2 value = {val2}")

        # Save differences in two new files
        save_differences(differences, 'differences_in_file1.txt', 'differences_in_file2.txt')
        print("\nDifferences saved to 'differences_in_file1.txt' and 'differences_in_file2.txt'.")
    else:
        print(f"No differences found.")

    print(f"Total comparisons made: {comparison_count}")
