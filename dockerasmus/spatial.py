# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import numpy
from .pdb import Atom, Chain, Protein, Residual


def TranslationMatrix(dx=0, dy=0, dz=0):
    """Returns a translation matrix
    """
    return numpy.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0,  1],
    ])


def RotationMatrix(theta_x=0, theta_y=0, theta_z=0):
    """Returns a rotation matrix
    """

    cos = numpy.cos
    sin = numpy.sin

    rx = numpy.array([
        [1,            0,            0, 0],
        [0, cos(theta_x),-sin(theta_x), 0],
        [0, sin(theta_x), cos(theta_x), 0],
        [0,            0,            0, 1]
    ])

    ry = numpy.array([
        [ cos(theta_y), 0, sin(theta_y), 0],
        [            0, 1,            0, 0],
        [-sin(theta_y), 0, cos(theta_y), 0],
        [            0, 0,            0, 1]
    ])

    rz = numpy.array([
        [cos(theta_z), -sin(theta_z), 0, 0],
        [sin(theta_z),  cos(theta_z), 0, 0],
        [           0,             0, 1, 0],
        [           0,             0, 0, 1]
    ])

    return rx.dot(ry).dot(rz)


def transform_cartesian(protein, x=0, y=0, z=0, sigma=0, rho=0):
    """Rotate and translate the protein

    Arguments:
        protein (`Protein`): a protein to move and rotate in
            the worldspace

    Keyword Arguments:
        x (int): the x cartesian coordinate to move the protein to
        y (int): the y cartesian coordinate to move the protein to
        z (int): the z cartesian coordinate to move the protein to
        sigma (int): the angle to rotate the protein along the x axis,
            **in radians**
        rho (int): the angle to rotate the protein along the y axis,
            **in radians**
    """
    matrix = RotationMatrix(sigma, rho).dot(TranslationMatrix(x, y, z))
    return apply_transformation_matrix(protein, matrix)


def transform_spherical(protein, r=0, phi=0, theta=0, sigma=0, rho=0):
    """Rotate and translate the protein

    Arguments:
        protein (`Protein`): a protein to move and rotate in
            the worldspace

    Keyword Arguments:
        r (int): the radial distance to move the protein to
        phi (int): the inclination to move the protein to
        theta (int): the azimuth to move the protein to
        sigma (int): the angle to rotate the protein along the x axis,
            **in radians**
        rho (int): the angle to rotate the protein along the y axis,
            **in radians**
    """
    x = r * numpy.sin(phi) * numpy.cos(theta)
    y = r * numpy.sin(theta) * numpy.sin(phi)
    z = r * numpy.cos(theta)
    return transform_cartesian(protein, x, y, z, sigma, rho)


def apply_transformation_matrix(protein, matrix):
    """Apply a 4x4 transformation matrix to a protein model
    """
    new_prot = Protein()
    for chain in protein.values():
        new_prot[chain.id] = new_chain = Chain(chain.id, chain.name)
        for res in chain.values():
            new_prot[chain.id][res.id] = new_res = Residual(res.id, res.name)
            for atom in res.values():
                old_pos = numpy.append(atom.pos, [1]) # 4 coords vector
                new_pos = matrix.dot(old_pos)[:3]
                new_prot[chain.id][res.id][atom.name] = Atom(
                    *new_pos, id=atom.id, name=atom.name, residual=new_res
                )
    return new_prot