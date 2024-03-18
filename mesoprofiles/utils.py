import graph_tool.all as gt
import numpy as np
from typing import Optional


def get_block_stats(state: Optional[gt.BlockState] = None,
                    g: Optional[gt.Graph] = None,
                    b: Optional[gt.VertexPropertyMap] = None,
                    verbose: bool = True) -> tuple:
    """
    Get block statistics including block graph, partition, and relevant counts.

    Args:
        state (Optional[gt.BlockState]): A block state representing the partition of the graph.
        g (Optional[gt.Graph]): The input graph.
        b (Optional[gt.VertexPropertyMap]): The vertex property map representing the partition.
        verbose (bool): Flag indicating whether to display verbose output.

    Returns:
        tuple: Tuple containing block graph, partition, and relevant counts.

    Raises:
        Exception: If neither state nor both graph g and partition b are specified.
    """
    if state is None:
        if verbose:
            if g is None or b is None:
                raise Exception("Either state or both graph g and partition b must be specified.")
        if not isinstance(b, gt.VertexPropertyMap):
            if np.max(b) > len(set(b)) - 1:
                b = gt.contiguous_map(np.array(b))
            b_new = g.new_vp('int')
            b_new.a = np.array(b)
            b = b_new.copy()
        else:
            b = gt.contiguous_map(b)
        bg = get_block_graph(g, b)
        B = bg.num_vertices()
        N = g.num_vertices()
        E = g.num_edges()
        ers = bg.ep["count"].a
        nr = bg.vp["count"].a
        er = bg.degree_property_map("out", weight=bg.ep["count"])
        ers_mat = gt.adjacency(bg, bg.ep["count"])
    else:
        if verbose:
            if g is not None or b is not None:
                print('Graph g and or partition b was specified although state was specified -'
                      'state is being used.')
        b = gt.contiguous_map(state.get_blocks())
        state = state.copy(b=b)
        bg = state.get_bg()
        B = state.get_B()
        N = state.get_N()
        ers = state.mrs.a
        nr = state.wr.a
        er = state.mrp
        E = sum(er.a) / 2
        ers_mat = state.get_matrix().todense()
    return bg, b, N, E, B, ers, nr, er, ers_mat


def get_block_graph(g: gt.Graph, b: gt.VertexPropertyMap) -> gt.Graph:
    """
    Get the block graph induced by a partition.

    Args:
        g (gt.Graph): The input graph.
        b (gt.VertexPropertyMap): The vertex property map representing the partition.

    Returns:
        gt.Graph: The block graph induced by the partition.
    """
    B = len(set(b))
    cg, br, vc, ec, av, ae = gt.condensation_graph(g, b,
                                                   self_loops=True)
    cg.vp.count = vc
    cg.ep.count = ec
    rs = np.setdiff1d(np.arange(B, dtype="int"), br.fa,
                      assume_unique=True)
    if len(rs) > 0:
        cg.add_vertex(len(rs))
        br.fa[-len(rs):] = rs

    cg = gt.Graph(cg, vorder=br)
    return cg


def get_density_matrix(block_ms, block_ns):
    """
    Calculates the densities within each block (allowing for self-loops)
    Parameters
    ----------
    block_ms: 2D array
        Matrix counting the number of edges that exist between pairs of blocks
    block_ns: 1D array
        Array counting the number of nodes in each block
    Returns
    -------
    ps: 1D array
        Array of the density between all pairs of blocks
    """
    ps = np.zeros((len(block_ns), len(block_ns)))
    for r in range(len(block_ns)):
        n_r = block_ns[r]
        for s in range(len(block_ns)):
            n_s = block_ns[s]
            m = block_ms[r,s]
            if r == s:
                n = n_r
                if n == 0:
                    ps[r, s] = 0
                else:
                    ps[r, s] = m / (n ** 2)

            else:
                if n_r == 0 or n_s == 0:
                    ps[r, s] = 0
                else:
                    ps[r, s] = m / (n_r * n_s)
    return ps