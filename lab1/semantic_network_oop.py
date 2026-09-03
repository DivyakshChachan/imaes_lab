class SemanticNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parents = [parent] if parent else []
        self.properties = {}
        self.exceptions = set()

    def add_parent(self, parent):
        self.parents.append(parent)

    def set_property(self, relation, value):
        self.properties[relation] = value

    def add_exception(self, relation, value):
        # We store exception as 'cannot <value>' for the relation 'can'
        self.exceptions.add((relation, value))

class SemanticNetwork:
    def __init__(self):
        self.nodes = {}

    def get_or_create(self, name):
        if name not in self.nodes:
            self.nodes[name] = SemanticNode(name)
        return self.nodes[name]

    def add_triple(self, subj, rel, obj):
        subject = self.get_or_create(subj)
        if rel == 'is-a':
            parent = self.get_or_create(obj)
            subject.add_parent(parent)
        elif rel == 'cannot':
            # Specifically handling exception for 'can'
            subject.add_exception('can', obj)
        else:
            subject.set_property(rel, obj)

    def get_inheritance_chain(self, node_name):
        node = self.get_or_create(node_name)
        chain = []
        current = node
        while current:
            chain.append(current.name)
            if current.parents:
                current = current.parents[0] # Single inheritance path for basic algo
            else:
                break
        return chain

    def query(self, node_name, relation):
        node = self.get_or_create(node_name)
        
        # Traverse up the single inheritance chain
        current = node
        while current:
            # Check exceptions first
            for exc_rel, exc_val in current.exceptions:
                if exc_rel == relation:
                    return f"cannot {exc_val}"
            
            # Check local properties
            if relation in current.properties:
                return current.properties[relation]
            
            if current.parents:
                current = current.parents[0]
            else:
                break
                
        return 'unknown'

class Frame:
    def __init__(self, **kwargs):
        self.slots = kwargs

    def get(self, key, default=None):
        return self.slots.get(key, default)

class FrameSystem:
    def __init__(self):
        self.frames = {}
        
    def add_frame(self, name, **slots):
        self.frames[name] = Frame(**slots)
        
    def query(self, node_name, slot):
        # Multiple Inheritance Support using Breadth First Search (C3 is complex for simple demo)
        queue = [node_name]
        visited = set()
        
        while queue:
            current = queue.pop(0)
            if current in visited: continue
            visited.add(current)
            
            if current not in self.frames:
                continue
                
            frame = self.frames[current]
            
            # Check exception
            if slot == 'can' and 'cannot' in frame.slots:
                return f"cannot {frame.slots['cannot']}"
                
            # Check local
            if slot in frame.slots:
                return frame.slots[slot]
                
            # Get parents
            parents = frame.get('ako', [])
            if isinstance(parents, list):
                queue.extend(parents)
            elif parents:
                queue.append(parents)
                
        return 'unknown'


def main():
    print("--- Experiment 1: Semantic Network (OOP Variation) ---")
    
    net = SemanticNetwork()
    triples = [
        ('animal', 'has', 'skin'),
        ('fish', 'is-a', 'animal'),
        ('shark', 'is-a', 'fish'),
        ('bird', 'is-a', 'animal'),
        ('bird', 'can', 'fly'),
        ('penguin', 'is-a', 'bird'),
        ('penguin', 'cannot', 'fly'),
        ('ostrich', 'is-a', 'bird'),
        ('ostrich', 'cannot', 'fly'),
        ('ostrich', 'can', 'run fast')
    ]
    
    for subj, rel, obj in triples:
        net.add_triple(subj, rel, obj)

    print("\nInheritance chain for 'penguin':", net.get_inheritance_chain('penguin'))
    print("Inheritance chain for 'ostrich':", net.get_inheritance_chain('ostrich'))
    print("Inheritance chain for 'shark':", net.get_inheritance_chain('shark'))

    queries = [
        ('shark', 'has'),
        ('bird', 'can'),
        ('penguin', 'can'),
        ('ostrich', 'can'),
        ('ostrich', 'has'),
        ('fish', 'can')
    ]
    
    print("\nQuery Results:")
    for q_node, q_rel in queries:
        print(f"  net.query('{q_node}', '{q_rel}') -> {net.query(q_node, q_rel)}")


    print("\n--- Exercise 2 & 3: Frames & Multiple Inheritance ---")
    fs = FrameSystem()
    fs.add_frame('animal', has='skin')
    fs.add_frame('bird', ako=['animal'], can='fly')
    fs.add_frame('fish', ako=['animal'])
    fs.add_frame('shark', ako=['fish'])
    fs.add_frame('swimmer', can='swim')
    # Penguin inherits from both bird and swimmer
    fs.add_frame('penguin', ako=['bird', 'swimmer'], cannot='fly')
    fs.add_frame('ostrich', ako=['bird'], cannot='fly', can='run fast')

    for q_node, q_rel in queries:
        print(f"  fs.query('{q_node}', '{q_rel}') -> {fs.query(q_node, q_rel)}")

    print(f"  fs.query('penguin', 'can') (tests swimmer inheritance after exception checked) -> {fs.query('penguin', 'can')}")
    # Note: BFS returns 'cannot fly' first since it's an exception on 'penguin'. 

if __name__ == "__main__":
    main()
