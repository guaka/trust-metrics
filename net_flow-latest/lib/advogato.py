"""
Library to calculate trust metrics "the advogato way".
"""

from net_flow import TrustNetwork as FlowNetwork

class AdvogatoTrustNetwork:
    """
    Calculate certification levels the Advogato way, with default parameters
    that mimic advogato.

    Based on code from Raph Levien's mod_virgule.

    Note that the actual seeds and capacities are unknown; I don't have
    access to Raph's config file.
    """
    capacities = [ 3200, 800, 200, 50, 12, 4, 2, 1 ]
    seeds = ['raph', 'miguel', 'federico', 'alan']
    levels = [ 'Observer', 'Apprentice', 'Journeyer', 'Master' ]
    
    def __init__(self):
        """
        Initialize class.  No arguments; this function creates
        the flows & initializes various variables.
        """
        self.flows = []

        # initialize a flow network for each level & seed it.
        for i in range(0, len(self.levels)):
            flow = FlowNetwork()

            for seed_name in self.seeds:
                flow.add_edge("-", seed_name)
                
            self.flows.append(flow)

        ###
            
        levels_d = {}
        levels_rev_d = {}
        for n, level in enumerate(self.levels):
            levels_d[level] = n
            levels_rev_d[n] = level

        self.levels_d = levels_d
        self.levels_rev_d = levels_rev_d

    def add_cert(self, cert_by, user, cert_level):
        """
        Add a certification from 'cert_by' of 'user', at 'cert_level'.
        """
        level = self.levels_d.get(cert_level, 0)

        if level:
            for i in range(1, level + 1):
                flow = self.flows[i]
                flow.add_edge(cert_by, user)

    def calculate_levels(self):
        """
        Calculate the certification level for each user.
        """
        # first, calculate the total flow in each network.
        for flow in self.flows:
            flow.calculate(self.capacities)

        #
        # then, go through and set the highest cert level possible
        #
        
        user_levels = {}
        for (i, flow) in enumerate(self.flows):
            # get the level name
            level = self.levels_rev_d[i]

            # see if the user is auth in this level.
            for user in flow:
                if flow.is_auth(user):
                    user_levels[user] = level

        # store.
        self.user_levels = user_levels
        self.users = self.user_levels.keys()

    def get_level(self, user):
        return self.user_levels.get(user)

class RobotsTrustNetwork(AdvogatoTrustNetwork):
    """
    Calculate certification levels with the parameters used in robots.net.

    c.f. http://robots.net/images/config.xml
    """
    capacities = [ 800, 200, 50, 12, 4, 2, 1 ]
    seeds = ['steve', 'The Swirling Brain', 'Rog-a-matic']
    # levels are the same

def read_certs(fp):
    l = []
    
    for line in fp:
        line = line.strip()
        if line and not line.startswith('#'):
            giver, recipient, level = line.split(',')
            l.append((giver, recipient, level,))

    return l

def fill_certs(certs_list, network):
    for giver, recipient, level in certs_list:
        network.add_cert(giver, recipient, level)

def read_actual(fp):
    d = {}
    for line in fp:
        line = line.strip()
        if line and not line.startswith('#'):
            user, level = line.split(',')
            d[user] = level

    return d
