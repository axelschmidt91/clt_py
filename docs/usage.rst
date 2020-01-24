=====
Usage
=====

To use CLT Calculation for Python in a project::

    import clt_py

or::

    from clt_py import *

or any other format you prefer.

--------------------
Setting up materials
--------------------

::

    # Matrix material:
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    # Fiber material:
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    # Composite Material:
    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

-------------------
Set up plies/layers
-------------------

::

    ply0 = Ply(mat_FRM, rotation=0, thickness=1)
    plyP45 = Ply(mat_FRM, rotation=45, thickness=1)
    plyN45 = Ply(mat_FRM, rotation=-45, thickness=1)

-------------------------
Arrange plies to laminate
-------------------------

::

    laminate = Laminate()

    laminate.addPly(plyP45)
    laminate.addPly(ply0)
    laminate.addPly(plyN45)

--------------------
Output material data
--------------------

Calculation of complete stiffness matrix (ABD-matrix) [#CLT]_.

.. [#CLT] according to CLT_

.. _CLT: https://en.wikipedia.org/wiki/Composite_laminate


::

    np.set_printoptions(precision=3, suppress=True)
    print(laminate.get_stiffnessMatrix())
