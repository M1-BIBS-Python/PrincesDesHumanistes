# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import collections
import six
import numpy

from .atom import Atom


class Residual(dict):

    def __init__(self, res_id, res_name=None, atoms=None):
        super(Residual, self).__init__(atoms or {})
        self.id = res_id
        self.name = res_name

    def __contains__(self, item):
        """Checks if `item` is contained in the residual.

        Arguments:
            item: either an atom_id (`int`) or an `Atom` object
                to check if present within the residual.
        """
        if isinstance(item, Atom):
            return super(Residual, self).__contains__(item)
        elif isinstance(item, int):
            return any(item == atom.id for atom in self.itervalues())
        else:
            raise TypeError(
                "'in <Residual>' requires Atom or unicode"
                " as left operand, not {}".format(type(item).__name__)
            )

    def itervalues(self):
        """Return an iterator over the atoms of the residual.
        """
        return six.itervalues(self)

    def iteritems(self):
        """Return an iterator over the (atom_id, atom) pairs of the residual.
        """
        return six.iteritems(self)

    @property
    def mass(self):
        """The mass of the residual.

        Computed as sum of the masses of the non-hydrogen
        atoms of the residual.
        """
        return sum(atom.mass for atom in self.itervalues())

    @property
    def mass_center(self):
        """The position of the mass center of the residual.

        Computed as the barycenter of the positions of the
        atoms weighted by their atomic masses.
        """
        mass = self.mass
        return sum((atom.mass/mass)*atom.pos for atom in self.itervalues())

    def distance_to(self, other):
        """The distance of the mass_center of the residual to `other`
        """
        if isinstance(other, Atom):
            return numpy.linalg.norm(self.mass_center - other.pos)
        elif isinstance(other, Residual):
            return numpy.linalg.norm(self.mass_center - other.mass_center)
        else:
            return numpy.linalg.norm(self.mass_center - other)

    def rmsd(self, ref):
        """The RMSD of the atoms of the residual, with ref as reference.

        Arguments:
            ref (numpy.array): the x,y,z coordinates of the reference
                position.
        """
        return numpy.sqrt(
            (1/len(self))*sum(atom.distance_to(ref) for atom in self)
        )
