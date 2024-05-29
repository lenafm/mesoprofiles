# Mesoprofiles

Let $R_{rs}$ denote the role that a blocks $r$ has with respect to its relationship to another block $s$. Depending on the relative edge densities within- and between blocks $r$ and $s$, $R_{rs}$ can take on one of the following roles: 

* a = assortative
* d = disassortative
* c = core
* p = periphery
* n = none (if within- and between-block densities between this block and the other block are all equal)

For example, if two blocks are assortative communities (higher within- than between block edge densities), than $R_{rs} = R_{sr} = \text{a}$. If block $r$ is the core to a periphery $s$, then $R_{rs} = \text{c}$ and $R_{sr} = \text{p}$. 

Blocks can take on different roles in different block-pair relationships. For example, block $r$ might be in an assortative community relationship with block $s$ ($R_{rs} = \text{a}$) it might be the core in the core-periphery relationship with another block $t$ ($R_{rt} = \text{c}$). $R_{rs}$ and $R_{sr}$ are therefore calculated for each block pair. 

Note that in the case of (dis-)assortative relationships $R_{rs} = R_{sr}$, which does not hold for core-periphery relationships. 

Blocks are categorise into roles with respect to all other blocks based on the elements of the edge density matrix $\omega = \{\omega_{rs}\}$. 

* $\min(\omega_{rr}, \omega_{ss}) > \omega_{rs} \iff R_{rs} = \text{a}$
* $\omega_{rr} \geq \omega_{rs} > \omega_{ss} \text{ or } \omega_{rr} > \omega_{rs} \geq \omega_{ss} \iff R_{rs} = \text{c}, R_{sr} = \text{p}$
* $\omega_{ss} \geq \omega_{rs} > \omega_{rr} \text{ or } \omega_{ss} > \omega_{rs} \geq \omega_{rr} \iff R_{rs} = \text{p}, R_{sr} = \text{c}$
* $\omega_{rs} > \max(\omega_{rr}, \omega_{ss}) \iff R_{rs} = \text{d}$
