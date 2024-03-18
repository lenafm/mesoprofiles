import graph_tool.all as gt
import numpy as np
from collections import Counter
from typing import Optional

from mesoprofiles.utils import get_block_stats, get_density_matrix


def calculate_mesoprofile(state: Optional[gt.BlockState] = None,
                          g: Optional[gt.Graph] = None,
                          b: Optional[gt.VertexPropertyMap] = None):
    _, b, _, _, B, ers, nr, _, ers_mat = get_block_stats(state=state, g=g, b=b)
    ps = get_density_matrix(block_ms=ers_mat, block_ns=nr)
    block_pair_relationships = get_block_pair_relationships(ps=ps, block_ns=nr)
    role_probabilities = calculate_role_probabilities(block_pair_relationships=block_pair_relationships, B=B)
    return calculate_node_role_proabilities(b=b, role_probabilities=role_probabilities)


def get_block_pair_relationships(ps, block_ns):
    """
    Implementation of between community motifs from Betzel et al. (2018), extended for directed case.
    Parameters
    ----------
    ps: 2D array
        Matrix of edge densities between pairs of blocks
    block_ns: 1D array
        Array counting the number of nodes in each block
    directed: boolean
        Directedness of underlying graph (default=False)
    Returns
    -------
    M: dict
        Dictionary of motif for each block pair
    """
    M = {}
    for r in range(len(block_ns)):
        for s in range(len(block_ns)):
            if r < s:
                omega_rr = ps[r, r]
                omega_rs = ps[r, s]
                omega_ss = ps[s, s]
                if min(omega_rr, omega_ss) > omega_rs:
                    M_rs = 'a'
                elif omega_rr > omega_rs > omega_ss:
                    M_rs = 'c_p'
                elif omega_ss > omega_rs > omega_rr:
                    M_rs = 'p_c'
                elif omega_rs > max(omega_rr, omega_ss):
                    M_rs = 'd'
                else:
                    M_rs = 'other'
                if M_rs is not None:
                    M[(r, s)] = M_rs
    return M


def calculate_role_probabilities(block_pair_relationships, B, directed=False):
    roles = {}
    for r in range(B):
        roles_r = []
        for block_pair, relationship in block_pair_relationships.items():
            if r in block_pair:
                idx = block_pair.index(r)
                role = relationship.split("_")[idx] if "_" in relationship else relationship
                roles_r.append(role)
        roles[r] = calculate_block_role_probabilities(roles=roles_r)
    return roles


def calculate_block_role_probabilities(roles):
    possible_roles = ['a', 'c', 'p', 'd', 'other']
    block_roles = dict(Counter(roles))
    n_roles = sum(block_roles.values())
    return {role: block_roles[role]/n_roles if role in block_roles else 0. for role in possible_roles}


def calculate_node_role_proabilities(b, role_probabilities):
    block_labels = b.a
    role_probabilities_nodes = np.array([list(role_probabilities[block].values()) for block in block_labels])
    return np.sum(role_probabilities_nodes, axis=0)/len(role_probabilities_nodes)