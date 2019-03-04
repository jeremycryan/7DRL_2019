class Map(object):

    def __init__(self, size = (60, 60)):

        self.cells = []

        for i in range(size[0]):
            self.cells.append([])
            for j in range(size[1]):
                self.cells[i].append([])


    def add_to_cell(self, new_item, pos):

        self.cells[pos[0]][pos[1]].append(new_item)
        self.sort_cell(pos)


    def sort_cell(self, pos):
        self.cells[pos[0]][pos[1]].sort(key=lambda a: a.layer)


    def remove_from_cell(self, remove_item, pos):
        if remove_item in self.cells[pos[0]][pos[1]]:
            self.cells[pos[0]][pos[1]].remove(remove_item)
            return remove_item


    def get(self, pos, *args):
        """ Example usage:

        map.get((0, 1), ("layer", 3), ("hidden", 0), "blocking")
        """
        
        things_at_pos = self.cells[pos[0]][pos[1]]
        return_list = []
        for thing in things_at_pos:
            add_to_list = True
            for arg in args:
                if type(arg) == str:
                    if not hasattr(thing, arg):
                        add_to_list = False
                else:
                    if getattr(thing, arg[0]) != arg[1]:
                        add_to_list = False
            if add_to_list:
                return_list.append(thing)
        return return_list


if __name__=="__main__":

    m = Map()
    a = Map()
    a.hidden = True

    m.add_to_cell(a, (3, 3))

