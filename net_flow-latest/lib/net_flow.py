import _net_flow

class TrustNetwork(object):
    """
    A single-layer trust network based on Raph Levien's Advogato "network
    flow" implementation.

    c.f. http://www.advogato.org/trust-metric.html for more information.
    """
    def __init__(self, seed_name="-"):
        """
        Initialize the network and set the name of the seed node to '-'
        by default.
        """
        self.seed_name = seed_name
        self.flow = _net_flow.new_flowobj()
        self.nodes = []
        self.auth_info = None

    def _add_node(self, name):
        if name not in self.nodes:
            self.nodes.append(name)
        self.auth_info = None

    def add_edge(self, fr, to):
        """
        Add a certification from 'fr' to 'to'.
        """
        self._add_node(fr)
        self._add_node(to)
        _net_flow.add_edge(self.flow, fr, to)

    def calculate(self, capacities):
        """
        Calculate who is good and who is bad.
        """
        assert self.seed_name in self.nodes
        _net_flow.calc_max_flow(self.flow, self.seed_name, capacities)
        results = _net_flow.extract(self.flow, len(self.nodes))
        
        auth_info = {}
        for i, node in enumerate(self.nodes):
            if results[i]:
                auth_info[node] = True
            else:
                auth_info[node] = False

        self.auth_info = auth_info

    def is_auth(self, name):
        """
        Check to see if a given name is trusted or not.
        """
        return self.auth_info.get(name)

    def __len__(self):
        """
        Return the number of nodes.
        """
        return len(self.nodes)

    def __getitem__(self, i):
        return self.nodes[i]
