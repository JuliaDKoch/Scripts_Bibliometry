#!/usr/bin/python3

import csv
import sys
import re

# we have a csv with the following format:
# ['Author_id', 'Coauthor_id', 'Author_name', 'Coauthor_name', 'Year']
def edges_from_file(filename, year):
    edges = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[4] <= year:
                edges.append((row[0], row[1]))
    return edges

members = {}
representative = {}

def component_of(author):
    if author in representative:
        return representative[author]
    else:
        members[author] = [author]
        representative[author] = author
        return author

def merge_components(a, b):
    for author in members[b]:
        members[a].append(author)
        representative[author] = a
    del members[b]

def compute_connected_components(filename, year):
    edges = edges_from_file(filename, year)
    print(year, "Edges: %d" % len(edges))

    for (a, b) in edges:
        a_comp = component_of(a)
        b_comp = component_of(b)
        if a_comp != b_comp:
            merge_components(a_comp, b_comp)

def components_by_size():
    return sorted([len(comp) for comp in members.values()], reverse=True)

def largest_component():
    largest = 0
    for comp in members.values():
        if len(comp) > largest:
            largest = len(comp)
    return largest

def node_count():
    return sum([len(comp) for comp in members.values()])

def isolated_node_count():
    return len([1 for comp in members.values() if len(comp) == 1])

def main(copublications, output = 'output.csv', output_detail = 'output_detail.csv'):
    output_file = open(output, "w")
    output_file_detail = open(output_detail, "w")
    csv.writer(output_file_detail).writerow(['Year', 'Components by Size', 'Largest Component', '# Nodes', '# Isolated Nodes'])
    global members
    global representative
    for j in range (1970,2025):
        members = {}
        representative = {}

        compute_connected_components(copublications, str(j))
        if node_count() == 0:
            print(j,": no data")
        else:
            print(j, ": All components by size: %s" % components_by_size())
            print(j, ": Largest component: %d" % largest_component())
            print(j, ": Number of nodes: %d" % node_count())
            print(j, ": Number of isolated nodes: %d" % isolated_node_count())
            print(j, ": Relative size of largest component: %f" % (largest_component() / node_count()))
            csv.writer(output_file).writerow([j, (largest_component() / node_count())])
            csv.writer(output_file_detail).writerow([j, components_by_size(), largest_component(), node_count(), isolated_node_count()])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s <copublications-file>" % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1])