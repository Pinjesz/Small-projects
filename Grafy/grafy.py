class Graf():

    number_of_vertices = 0

    def __init__(self, vertices, neighbours):
        self.vertices = []
        self.neighbours = []
        if len(vertices) == len(neighbours):
            self.vertices = vertices
            self.neighbours = neighbours
            self.number_of_vertices += len(vertices)

    def add_vertex(self, name, neighbours):
        if (name not in self.vertices) and (neighbours in self.vertices):
            self.vertices += [name]
            self.neighbours += [neighbours]
            for vertex in neighbours:
                self.neighbours[self.vertices.find(vertex)] += [name]
            self.number_of_vertices += 1
            return True
        return False

    def del_vertex(self, name):
        if name in self.vertices:
            pos = self.vertices.find(name)
            self.vertices.pop(pos)
            self.neighbours.pop(pos)
            for i, vertex in enumerate(self.neighbours[pos]):
                self.neighbours[i].remove(name)
            self.number_of_vertices -= 1
            return True
        return False

    def num_of_vertices(self):
        return Graf.number_of_vertices

    def num_of_edges(self):
        sum = 0
        for vertex in self.neighbours:
            sum += len(vertex)
        return sum/2

    def degree_of_vertex(self, name):
        if name in self.vertices:
            pos = self.vertices.find(name)
            return len(self.neighbours[pos]), True
        return False

    def is_dense(self):
        if self.num_of_edges() > 0.9 * self.num_of_vertices()**2:
            return True
        return False


if __name__ == "__main__":
    graf_1 = Graf(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], [['B'], ['A', 'D', 'C'], [
                  'B'], ['B', 'E'], ['D', 'F', 'H'], ['E', 'G'], ['F'], ['E']])

    graf_1.add_vertex('I', ['D'])
