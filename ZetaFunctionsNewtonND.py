"""
COMPUTING (LOCAL) IGUSA AND TOPOLOGICAL ZETA FUNCTIONS FOR NEWTON NON-DEGENERATED POLYNOMIALS
"""

################################################################################
#                                                                              #
# COMPUTING (LOCAL) IGUSA AND TOPOLOGICAL ZETA FUNCTIONS OF A                  #
# NON-DEGENERATED POLYNOMIAL WITH RESPECT TO ITS NEWTON'S POLYHEDRON.          #
# For Sagemath                                                                 #
#                                                                              #
# Last update: 18-07-2022                                                      #
#                                                                              #
# These functions are based on the work of K. Hoornaert and D. Loots:          #
# "Computer program written  in Maple for the calculation of Igusa local zeta  #
# function".                                                                   #
# http://www.wis.kuleuven.ac.be/algebra/kathleen.htm, 2000.                    #
#                                                                              #
# For any bug or commentary, please contact me.                                #
#                                                                              #
# Juan Viu-Sos                                                                 #
# Universidad Politecnica de Madrid                                            #
# https://jviusos.github.io/                                                   #
# juan.viusos@upm.es                                                           #
#                                                                              #
#                                                                              #
# This program is free software; you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation; either version 2 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,                   #
# MA 02110-1301, USA.                                                          #
#                                                                              #
################################################################################

# TO DO
    # [ ] Set the local case by default
    # [ ] Implementation of formula for germs on quotient singularities
    # [ ] Improve topological and monodromy zeta functions outputs
    # [ ] Implementation of the motivic zeta function
#
#


class ZetaFunctions(object):
    r"""
    The class ``Zetafunctions`` takes a multivariate polynomial as
    argument and allows to calculate its associated (local) Igusa and
    Topological zeta functions.

    This class allows us to get information about the associated
    Newton's polyhedron, their faces, the associated cones, ...

    This class is composed by a multivariate polynomial `f` of degree
    `n` with non-constant term and its associated Newton's polyhedron
    `\Gamma(f)`.

    Methods in ZetaFunctions:

    - cones_plot(self, **kwargs)
    - dict_info_poles(self, d=1, weights=None, local=False)
    - get_newton_polyhedron(self)
    - get_polyfaces_dictionary(self, keys = 'polynomials', compact = False)
    - give_expected_pole_info(self, d=1, local=False, weights=None)
    - give_info_facets(self, compact = False)
    - give_info_newton(self, faces=False, cones=False, compact = False)
    - is_newton_degenerated(self, p=None, local=False, method='default', info = False)
    - newton_plot(self, point_size = 30, **kwargs)
    - igusa_zeta(self, p=None, dict_Ntau={}, local=False, weights=None, info=False, check='ideals')
    - topological_zeta(self, d=1, local=False, weights=None, info=False, check='ideals')
    - monodromy_zeta(self, char=False, info=False, check='ideals')

    .. WARNING::

        These formulas for the Igusa and Topological zeta functions
        only work when the given polynomial is NOT DEGENERATED with
        respect to his associated Newton Polyhedron (see [DH01]_,
        [DL92]_ and [Var76]_).

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: zex = ZetaFunctions(x^2 + y*z)
        sage: zex.give_info_newton()
        Newton's polyhedron of x^2 + y*z:
            support points = [(2, 0, 0), (0, 1, 1)]
            vertices = [(0, 1, 1), (2, 0, 0)]
            number of proper faces = 13
            Facet 0: x + 2*y - 2 >= 0
            Facet 1: x + 2*z - 2 >= 0
            Facet 2: z >= 0
            Facet 3: y >= 0
            Facet 4: x >= 0
        sage: zex.topological_zeta()
        (1/2) * (s + 1)^-1 * (s + 3/2)^-1 * (s + 3)
        sage: zex.give_expected_pole_info()
        The candidate poles of the (local) topological zeta function 
        (with d = 1) of x^2 + y*z in function of s are:
        ======
        -3/2 with expected order: 2
        The responsible face of maximal contribution is ``tau_0`` = minimal face 
        who intersects with the diagonal of ambient space:
             tau4: dim 1,  vertices = [(0, 1, 1), (2, 0, 0)],  rays = [],  
             cone generators = [(1, 0, 2), (1, 2, 0)], partition into simplicial 
             cones = [[(1, 0, 2), (1, 2, 0)]]
        ======
        -1 with expected order: 1
        (If all Vol(tau) are 0, where tau runs through the selected faces that are 
        no vertices, then the expected order of -1 is 0).


    REFERENCES:

    ..  [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's Local
    Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.

    ..  [DL92] Denef, J. and Loeser, F., Caractéristiques d'Euler-Poincaré,
    fonctions zêta locales et modifications analytiques, J. Amer. Math. Soc. 5
    (1992), no. 4, 05–720.

    ..  [HL00] Hoornaert, K. and Loots, D., Computer program written in Maple
    for the calculation of Igusa's local zeta function, (2000).
    http://www.wis.kuleuven.ac.be/algebra/kathleen.htm

    ..  [Var76] Varchenko, A. N., Zeta-function of monodromy and Newton's
    diagram. Invent. Math. 37 (1976), no. 3, 253–262.

    ..  [Viu12] Viu-Sos, J., Funciones zeta y poliedros de Newton: Aspectos teoricos y computacionales, Master Thesis (2012).
    https://zaguan.unizar.es/record/8916/files/TAZ-TFM-2012-749.pdf

    AUTHORS:

    - Kathleen Hoornaert (2000): initial version for Maple

    - Juan Viu-Sos (2012): initial version for Sage
    
    - Frédéric Chapoton (2017): improved outputs, handling errors and symbolic variables 
    
    - Juan Viu-Sos (2022): improved methods and new functions in the class to visualize data
    """
    def __init__(self, poly):
        # Polynomial
        self._f = poly
        # Newton's polyhedron
        self._Gammaf = newton_polyhedron(poly)
    
    def cones_plot(self, **kwargs):
        r"""
        Plots the Fan of cones associated to Newton's polyhedron
        (for n = 2 , 3).
        
        Options:

        - Keyword options for `plot()`.
        """
        return fan_all_cones(self._Gammaf).plot(**kwargs)

    def dict_info_poles(self, d=1, weights=None, local=False):
        r"""
        Return a dictionary where the keys are the candidate real poles of
        the chosen zeta function.

        INFORMATION ABOUT POLES OF THE TOPOLOGICAL ZETA FUNCTION

        Items are lists containing, by order:

        1. The list of perpendicular vectors to the facets that are
           responsible for the candidate real pole.

        2. A list of the faces of maximal dimension that are responsible for
           the expected order.

        3. The expected order.

        4. Boolean: for the candidate pole -1 the factor L_tau or s/(s+1)
           can contribute to the order. If this is is the case, we increase
           the expected order due to the S_Delta_tau by 1 and this record
           gets the value ``True``. In all other cases we do not increase this
           expected order and this record gets the value ``False``.
        """
        f = self._f
        P = self._Gammaf
        PL = P.face_lattice() #We need to keep the face lattice in order to compare faces
        if local:
            faces_set = compact_faces(P)
        else:
            faces_set = proper_faces(P)
        faces_set = face_divisors(d, faces_set, P)

        all_prim_vect = set([])
        for tau in faces_set:
            all_prim_vect = all_prim_vect.union(set(map(tuple,
                                                        primitive_vectors(tau))))

        dict_poles = {}
        for v in all_prim_vect:
            if m_vect(v, P):
                realpole = -sigma_vect(v, weights) / m_vect(v, P)
                # We initialize a list of attributes if the pole is
                # not detected yet
                if dict_poles.get(realpole) is None:
                    dict_poles[realpole] = [set([v]), [], 0, False]
                else:
                    dict_poles[realpole][0].add(v)

        # We calculate the maximal expected of each pole and the faces
        # of higher dimension
        # responsibles of this order
        poles_set = list(dict_poles.keys())
        # If d=1, we have the face tau_0
        # (tau_0 is the smallest face which contains the intersecion
        # between diagonal and polyhedron)
        if d == 1 and not local:
            max_pole = max(poles_set)
            for tau in faces_set:
                gens_cone = [tuple(v) for v in primitive_vectors(tau)]
                if set(gens_cone) == dict_poles[max_pole][0]:
                    dict_poles[max_pole][1] = [tau]
                    dict_poles[max_pole][2] = rank(matrix(gens_cone))
                    dict_poles[max_pole][3] = False
                    break
            poles_set.remove(max_pole)
        for pole in poles_set:
            vects_pole = dict_poles[pole][0] #added
            interscones = [ set([tuple(v) for v in primitive_vectors(tau)]).intersection(vects_pole) for tau in faces_set ]
            orders = [ matrix(QQ, list(ic)).rank() for ic in interscones ]
            maxorder = max(orders)
            max_faces = set([ faces_set[i] for i in range(len(faces_set)) if orders[i] == maxorder ])
            # We find the maximal elements in set of responsible faces
            for face in faces_set:
                if face in max_faces:
                    if any(PL.lt(face, tau) for tau in max_faces): #BUG: "face < tau" did not compare well
                        max_faces.remove(face)
            dict_poles[pole][1] = list(max_faces)
            # Max order of pole is max dim of the associated cones
            dict_poles[pole][2] = maxorder
            # We convert the set of vectors into a list
            dict_poles[pole][0] = list(map(vector, dict_poles[pole][0]))

        # Special pole -1 has sometimes a larger order
        if -1 in dict_poles.keys():
            faces_minus_one = dict_poles[-1][1]
            if max(len(support_points_in_face(f, tau))
                   for tau in faces_minus_one) > 1:
                dict_poles[-1][2] = dict_poles[-1][2] + 1
                dict_poles[-1][3] = True
        return dict_poles
        
    def get_newton_polyhedron(self):
        r"""
        Return Newton's polyhedron.
        """
        return self._Gammaf
    
    def get_polyfaces_dictionary(self, keys = 'polynomials', compact = False):
        r"""
        Return a dictionary with the polynomials associated to each face of the Newton's polyhedron.
        
        Options:

        - ``keys = 'faces'`` keys are faces (by default: 'polynomials').
        
        - ``compact = True`` consider only the compact faces (by default: False).
        """
        if compact:
            faces_set = compact_faces(self._Gammaf)
        else:
            faces_set = proper_faces(self._Gammaf)
        if keys == 'polynomials':
            d = { ftau(self._f, tau): tau for tau in faces_set }
        elif keys == 'faces':
            d = { tau: ftau(self._f, tau) for tau in faces_set }
        else:
            raise ValueError("Not recognized option for 'keys'.")
        return d
    
    def give_expected_pole_info(self, d=1, local=False, weights=None):
        r"""
        Print information about the candidate real poles of the
        topological zeta function `Z_{top, f}^{(d)}(s)` like order of
        poles and responsible faces of highest dimension.

        - ``local = True`` calculates the local (at the origin) topological
          Zeta function.

        - ``weights`` -- a `n`-tuple of non-negative integers `(w_1,\ldots,w_n)` representing
        the volume form `x_1^{w_1-1}\cdots x_n^{w_n-1}\ dx_1\wedge\cdots\wedge dx_n`.

        REFERENCES:

        .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
        """
        f = self._f
        dict_poles = self.dict_info_poles(d, weights, local)
        P = self._Gammaf
        if local:
            faces_set = compact_faces(P)
        else:
            faces_set = proper_faces(P)

        faces_set = face_divisors(d, faces_set, P)
        n_supp_by_face = [len(support_points_in_face(f, tau))
                          for tau in faces_set]
        if not dict_poles:
            if (d == 1 and max(n_supp_by_face) == 1) or d != 1:
                print("There will be no poles for the (local) topological zeta function " + "(with d = " + str(d) + ") of " + str(f) + ".")
            else:
                print("The candidate poles of the (local) topological zeta function (with d = " + str(d) + ") of " + str(f) + " in function of s are:")
                print("=" * 6)
                print("-1 with expected order: 1")
                print("(If all Vol(tau) are 0, where tau runs through the selected faces that are no vertices, then the expected order of -1 is 0)")
        else:
            poles_set = list(dict_poles.keys())
            poles_set.sort(reverse=True)
            ## We reconstruct the list of all faces accessing to element
            #some_face = dict_poles[poles_set[0]][1][0]
            #list_all_faces = list(some_face.polyhedron().face_lattice())[1:-1]
            list_all_faces = proper_faces(P) #debug
            if d == 1 and not local:
                print("The candidate poles of the (local) topological zeta function (with d = " + str(d) + ") of " + str(f) + " in function of s are:")
                max_pole = max(poles_set)
                print("=" * 6)
                print(str(max_pole) + " with expected order: " + str(dict_poles[max_pole][2]))
                if max_pole == -1:
                    if dict_poles[-1][3]:
                        print("(If all the Vol(tau) of the faces tau that are no vertices and contained in Gamma are 0, then the expected order of -1 is " + str(dict_poles[-1][3] - 1) + ").")
                tau_0 = dict_poles[max_pole][1][0]
                print("The responsible face of maximal contribution is ``tau_0`` = "
                      "minimal face who intersects with the diagonal "
                      "of ambient space:")
                i = list_all_faces.index(tau_0)
                print("     tau" + str(i) + ": " + face_info_output(tau_0) + ",  " + cone_info_output(cone_from_face(tau_0)))
                poles_set.remove(max_pole)
                if -1 not in poles_set:
                    print("=" * 6)
                    print("-1 with expected order: 1")
                    print("(If all Vol(tau) are 0, where tau runs through the selected faces that are no vertices, then the expected order of -1 is 0).")
            elif local:
                print("The candidate poles of the local topological zeta function (with d = " + str(d) + ") of " + str(f) + " in function of s are:")
                if max(n_supp_by_face) > 1 and -1 not in poles_set:
                    print("=" * 6)
                    print("-1 with expected order: 1")
                    print("(If all Vol(tau) are 0, where tau runs through the selected faces that are no vertices, then the expected order of -1 is 0).")
            for pole in poles_set:
                print("=" * 6)
                print(str(pole) + " with expected order: " + str(dict_poles[pole][2]))
                if dict_poles[pole][3]:
                    print("(If all the Vol(tau) of the faces that are no vertices and contained")
                    print("one or more of the faces below are 0, then the expected order of -1 is " + str(dict_poles[pole][3] - 1) + ").")
                print("The responsible face(s) of maximal dimension is/are:")
                for tau in dict_poles[pole][1]:
                    i = list_all_faces.index(tau)
                    print("\t" + "=" * 6)
                    print("\t tau" + str(i) + ": " + face_info_output(tau) + ",  " + cone_info_output(cone_from_face(tau)))

    def give_info_facets(self, compact = False):
        r"""
        Print a relation of facets in Newton's polyhedron and the
        inequalities which define them.
        """
        give_all_facets_info(self._f, self._Gammaf, compact)

    def give_info_newton(self, faces=False, cones=False, compact = False):
        r"""
        Print information about the the Newton's polyhedron of ``f``:

        - Support points of f.
        - Vertices of Newton's polyhedron.
        - Number of proper faces.
        - Inequalities defining facets.

        Options:

        - ``faces = True`` prints information about each face in polyhedron.

        - ``cones = True`` prints information about each cone associated
          to faces in polyhedron.
        
        - ``compact = True`` consider only the compact faces (by default: False).
        """
        if compact:
            faces_set = compact_faces(self._Gammaf)
        else:
            faces_set = proper_faces(self._Gammaf)
        print("Newton's polyhedron of " + str(self._f) + ":")
        print("    support points = " + str(self._f.exponents()))
        print("    vertices = " + str(list(map(tuple, self._Gammaf.vertices()))))
        if compact:
            print("    number of compact faces = {}".format(len(faces_set)))
        else:
            print("    number of proper faces = {}".format(len(faces_set)))
        give_all_facets_info(self._f, self._Gammaf, compact)
        if faces or cones:
            print("Information about faces:")
            for tau in faces_set:
                face_info, cone_info = "", ""
                i = faces_set.index(tau)
                if faces:
                    face_info = face_info_output(tau) + "\n"
                if cones:
                    cone_info = cone_info_output(cone_from_face(tau)) + "\n"
                print("tau" + str(i) + ": " + face_info + cone_info)
    
    def is_newton_degenerated(self, p=None, local=False, method='default', info = False):
        r"""
        Checks if the polynomial ``f`` is degenerated over `\mathbb{F}_p` (``p`` prime) with respect \
        the faces of the polyhedron ``P`` (see [DH01]_).

            - ``p = None``, checks degeneration over `\CC` (which is equivalent to be 
            degenerated over `\mathbb{F}_p` with `p>>0`).
            
            - ``local = True`` checks degeneration for local case (only with respect the compact faces).
            
            - ``info = True`` prints the first face for which the polynomial is degenerated.

        For finite fields (``p`` is a given prime):

            - ``method = 'default'`` checks the condition using evaluation over `(\mathbb{F}_p-0)^n` \
        in the system of equations.

            - ``method = 'ideals'`` checks the condition using ideals over the finite field.

        REFERENCES:

        .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
        """
        return is_newton_degenerated(self._f, self._Gammaf, p, local, method, info)

    def newton_plot(self, point_size = 30, **kwargs):
        r"""
        Returns the graphics of the associated Newton's polyhedron (for n = 2 , 3) together with the support of f.
        In 3D, the origin is plotted as a black point.
        
        Options:

        - ``point_size`` size of the ponits in plot (by default: 30).
        
        - Other keyword options for `plot()`.
        """
        n = self._f.parent().ngens()
        pts = self._f.exponents()
        if n == 2:
            plot_pts = sum([point(p, color='red', size=point_size) for p in pts])
        elif n == 3:
            plot_pts = sum([point3d(p, color='red', size=point_size) for p in pts])
            plot_pts += point3d(tuple([0]*3), color='black', size=point_size)
            #print(plot_pts)
        else:
            raise TypeError('Dimension different from 2 and 3.')
        return (self._Gammaf.plot(**kwargs) + plot_pts)

    def igusa_zeta(self, p=None, dict_Ntau={}, local=False, weights=None,
                   info=False, check='ideals'):
        r"""
        Return the expression of the Igusa zeta function for `p` a
        prime number (explicit or abstract), in terms of a symbolic
        variable `s`.

        - ``local = True`` calculates the local Igusa zeta function
          (at the origin).

        - ``weights`` -- a `n`-tuple of non-negative integers `(w_1,\ldots,w_n)` representing
        the volume form `x_1^{w_1-1}\cdots x_n^{w_n-1}\ dx_1\wedge\cdots\wedge dx_n`.

        - ``info = True`` gives information of each face `\tau`, the
            associated cone of `\tau`, and the values ``L_tau`` and
            ``S_tau`` in the process.

        - ``check`` -- choose the method to check the non-degeneracy
            condition ('default' or 'ideals'). If ``check =
            'no_check'``, degeneracy checking is omitted.

        .. WARNING::

            This formula is only valid when the the given polynomial
            is NOT DEGENERATED for `p` with respect to its
            associated Newton Polyhedron (see [DH01]_).

        In the abstract case ``p = None``, you can give a dictionary
        ``dict_Ntau`` where:

        - The keys are the polynomials `f_{\tau}` associated of each
          face `\tau` of the Newton Polyhedron.

        - The items are the associated abstract values \
          `N_{\tau}= \#\{a\in(\mathbb{F}_p - 0)^d \mid f^*_{\tau}(a)=0\}` with \
          `f^*_{\tau}=\mathbb{F}_p(f_{\tau})`,
          depending of a symbolic variable ``p``.

        If the value associated to a face `\tau_k` is not in the
        dictionary, function introduces a new symbolic variable
        ``N_tauk`` to represent `N_{\tau_k}`.

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]; p = var('p')
            sage: zex1 = ZetaFunctions(x^2 - y^2 + z^3)

        For p=3 given::

            sage: zex1.igusa_zeta(p = 3)
            2*3^(2*s)*(3^(2*s + 4) - 3^(s + 1) + 2)/((3^(3*s + 4) - 1)*(3^(s + 1) - 1))

        For p arbitrary, we can give the number of solutions over the faces::

            sage: dNtau1 = { x^2-y^2+z^3 : (p-1)*(p-3), -y^2+z^3 : (p-1)^2, x^2+z^3 : (p-1)^2, x^2-y^2 : 2*(p-1)^2 }
            sage: zex1.igusa_zeta(p = None, dict_Ntau = dNtau1)
            (p + p^(2*s + 4) - p^(s + 1) - 1)*(p - 1)*p^(2*s)/((p^(3*s + 4) - 1)*(p^(s + 1) - 1))

            sage: zex2 = ZetaFunctions(x^2 + y*z + z^2)

        For p=3 mod 4, we can give the number of solutions over the faces::

            sage: dNtau2 = { x^2+y*z+z^2 : (p-1)^2, y*z+z^2 : (p-1)^2,  x^2+y*z : (p-1)^2, x^2+z^2 : 0 }
            sage: zex2.igusa_zeta(p = None, dict_Ntau = dNtau2)
            (p - 1)*p^(2*s)*(p^(s + 3) - 1)/((p^(2*s + 3) - 1)*(p^(s + 1) - 1))

        For p=1 mod 4::

            sage: dNtau2bis = { x^2+y*z+z^2 : (p-1)*(p-3), y*z+z^2 : (p-1)^2,  x^2+y*z : (p-1)^2, x^2+z^2 : 2*(p-1)^2 }
            sage: zex2.igusa_zeta(p = None, dict_Ntau = dNtau2bis)
            (p - 1)*p^(2*s)*(p^(s + 3) - 1)/((p^(2*s + 3) - 1)*(p^(s + 1) - 1))

        REFERENCES:

        .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
        """
        f = self._f
        s = var('s')
        if not isinstance(p, (int, Integer)):
            p = var('p')
        P = self._Gammaf
        abs_Ngamma = None
        abs_Ntau = None
        if check != 'no_check':
            if is_newton_degenerated(f, P, p, local, method=check, info=info):
                raise TypeError('degenerated wrt Newton')
        else:
            print("Warning: not checking the non-degeneracy condition!")
        if local:
            faces_set = compact_faces(P)
            result = 0
        else:
            faces_set = proper_faces(P)
            if p not in ZZ:
                abs_Ngamma = dict_Ntau.get(f)
                if abs_Ngamma is None:
                    abs_Ngamma = var('N_Gamma')
            result = Lgamma(f, p, abs_Ngamma, s)
            if info:
                print("Gamma: total polyhedron\nL_gamma = " + str(result) + "\n")
        for tau in faces_set:
            i = proper_faces(P).index(tau)
            if p not in ZZ:
                f_tau = ftau(f, tau)
                if len(f_tau.exponents()) == 1:
                    abs_Ntau = 0    # If f_tau is a monomial
                else:
                    abs_Ntau = dict_Ntau.get(f_tau)
                    if abs_Ntau is None:
                        abs_Ntau = var('N_tau' + str(i))
            L_tau, N_tau = Ltau(f, tau, p, abs_Ntau, s)
            S_tau, cone_info = Stau(f, P, tau, p, weights, s)
            if info:
                print("tau" + str(i) + ":")
                print(face_info_output(tau))
                print(cone_info)
                print("N_tau = " + str(N_tau))
                print("L_tau = " + str(L_tau))
                print("S_tau = " + str(S_tau))
                print()
            result += L_tau * S_tau
        return result.factor()

    def topological_zeta(self, d=1, local=False, weights=None, info=False,
                         check='ideals'):
        r"""
        Return the expression of the Topological zeta function
        `Z_{top, f}^{(d)}` for `d\geq 1`, in terms of the symbolic
        variable ``s``:

        - ``local = True`` calculates the local Topological
          zeta function (at the origin).

        - ``weights`` -- a `n`-tuple of non-negative integers `(w_1,\ldots,w_n)` representing
        the volume form `x_1^{w_1-1}\cdots x_n^{w_n-1}\ dx_1\wedge\cdots\wedge dx_n`.

        - ``d`` -- (default:1) an integer. We consider only the divisor
          whose multiplicity is a multiple of ``d`` (see [DL92]_).

        - ``info = True`` gives information of each face `\tau`, the
            associated cone of `\tau`, and the values `J_\tau` and
            `\mathop{dim}(\tau)!\cdot\mathop{Vol}(\tau)`
            in the process (see [DL92]_).

        - ``check`` -- choose the method to check the non-degeneracy condition
          ('default' or 'ideals'). If ``check = 'no_check'``, degeneracy
          checking is omitted.

        .. WARNING::

            This formula is only valid when the the given polynomial
            is NOT DEGENERATED with respect to its associated Newton
            Polyhedron (see [DL92]_).

        EXAMPLES::

            sage: R.<x,y,z> = QQ[]
            sage: zex1 = ZetaFunctions(x^2 + y*z)
            sage: zex1.topological_zeta()
            (1/2) * (s + 1)^-1 * (s + 3/2)^-1 * (s + 3)

        For d = 2::

            sage: zex1.topological_zeta(d = 2)
            (1/2) * (s + 3/2)^-1

        REFERENCES::

        .. [DL92] Denef, J. and Loeser, F., Caractéristiques d'Euler-Poincaré,
        fonctions zêta locales et modifications analytiques, J. Amer. Math. Soc.
        5 (1992), no. 4, 05–720.
        """
        f = self._f
        s = polygen(QQ, 's')
        ring_s = s.parent()
        #s = var('s')
        P = self._Gammaf
        if check != 'no_check':
            if local:
                if is_newton_degenerated(f, P, local=True, method=check, info=info):
                    raise TypeError('degenerated wrt Newton')
            else:
                if is_global_degenerated(f, method=check):
                    raise TypeError('degenerated wrt Newton')
        else:
            print("Warning: not checking the non-degeneracy condition!")
        result = ring_s.zero()
        if local:
            faces_set = compact_faces(P)
        else:
            faces_set = proper_faces(P)
            if d == 1:
                total_face = faces(P)[-1]
                dim_gamma = total_face.dim()
                vol_gamma = face_volume(f, total_face)
                result = (s / (s + 1)) * (-1) ** dim_gamma * vol_gamma
                if info:
                    print("Gamma: total polyhedron")
                    print("J_gamma = 1")
                    print("dim_Gamma!*Vol(Gamma) = " + str(vol_gamma))
                    print()

        faces_set = face_divisors(d, faces_set, P)
        for tau in faces_set:
            J_tau, cone_info = Jtau(tau, P, weights, s)
            dim_tau = tau.dim()
            vol_tau = face_volume(f, tau)
            if info:
                i = proper_faces(P).index(tau)
                print("tau" + str(i) + ":")
                print(face_info_output(tau))
                print(cone_info)
                print("J_tau = " + str(J_tau))
                print("dim_tau!*Vol(tau) = " + str(vol_tau))
                print()
            if d == 1:
                if dim_tau == 0:
                    term = J_tau
                else:
                    term = (s / (s + 1)) * ((-1) ** dim_tau) * vol_tau * J_tau
            else:
                term = ((-1) ** dim_tau) * vol_tau * J_tau
            result += term
            result = simplify(expand(result))
            if result != 0:
                result = result.factor()
        return result

    def monodromy_zeta(self, char=False, info=False, check='ideals'):
        r"""
        Return the expression of the Monodromy zeta function at the
        origin, in terms of the symbolic variable ``s``.

            - ``char = True`` prints the characteristic polynomial of
            the monodromy (only if `f` has an isolated singularity
            at the origin).

            - ``info = True`` gives information of each face `\tau`, the associated cone of \
            `\tau`, and the values `J_\tau` and `\mathop{dim}(\tau)!*\mathop{Vol}(\tau)` \
            in the process (see [Var76]_).

            - ``check`` -- choose the method to check the
            non-degeneracy condition ('default' or 'ideals'). If
            ``check = 'no_check'``, degeneracy checking is omitted.

        .. WARNING::

            This formula is only valid when the the given polynomial
            is NOT DEGENERATED with respect to its associated Newton
            Polyhedron (see [Var76]_).

        EXAMPLES::

            sage: R.<x,y> = QQ[]
            sage: zex1 = ZetaFunctions(y^7+x^2*y^5+x^5*y^3)
            sage: zex1.monodromy_zeta(char = True)
            The characteristic polynomial of the monodromy is (t - 1)^3 * 
            (t^6 + t^5 + t^4 + t^3 + t^2 + t + 1) * (t^18 + t^17 + t^16 + 
            t^15 + t^14 + t^13 + t^12 + t^11 + t^10 + t^9 + t^8 + t^7 + 
            t^6 + t^5 + t^4 + t^3 + t^2 + t + 1)
            ======
            (t - 1)^-2 * (t^6 + t^5 + t^4 + t^3 + t^2 + t + 1)^-1 * 
            (t^18 + t^17 + t^16 + t^15 + t^14 + t^13 + t^12 + t^11 +
            t^10 + t^9 + t^8 + t^7 + t^6 + t^5 + t^4 + t^3 + t^2 + t + 1)^-1

            ======
            -1/(-t^26 + t^19 + t^7 - 1)

            sage: S.<x,y,z> = QQ[]
            sage: zex2 = ZetaFunctions(x*y + z^3)
            sage: zex2.monodromy_zeta(char = True)
            The characteristic polynomial of the monodromy is t^2 + t + 1
            ======
            (-1) * (t - 1) * (t^2 + t + 1)

        REFERENCES::

        ..  [Var76] Varchenko, A. N., Zeta-function of monodromy and Newton's
        diagram. Invent. Math. 37 (1976), no. 3, 253–262.
        """
        f = self._f
        n = f.parent().ngens()
        P = self._Gammaf

        t = polygen(QQ, 't')
        ring_t = t.parent()

        if check != 'no_check':
            #if is_global_degenerated(f, method=check):
            if is_newton_degenerated(f, P, local=True, method=check, info=info):
                raise TypeError('degenerated wrt Newton')
        else:
            print("Warning: not checking the non-degeneracy condition!")

        result = ring_t.one()
        for i, tau in enumerate(compact_faces(P)):
            zeta_tau = Mtau(tau)
            dim_tau = tau.dim()
            vol_tau = face_volume(f, tau)
            if info:
                print("tau{}: {}".format(i, tau.ambient_Vrepresentation()))
                print("M_tau = {}".format(zeta_tau))
                print("dim_tau!*Vol(tau) = {}".format(vol_tau))
                print()
            result *= zeta_tau ** ((-1) ** dim_tau * vol_tau)
        if char:
            mn = (-1) ** (n - 1)
            num_deg = ring_t(result.numerator()).degree()
            den_deg = ring_t(result.denominator()).degree()
            mu = mn * (num_deg - den_deg - 1)
            aux = result(t=~t)
            charpoly = factor(t ** mu * (t / (t - 1) * aux) ** mn)
            print("The characteristic polynomial of the monodromy is {}".format(charpoly))
            print("=" * 6)
        return factor(result)

# ------------------------AUXILIARY FUNCTIONS------------------------


# NEWTON'S POLYHEDRON
def newton_polyhedron(f):
    r"""
    Construct an object ``Polyhedra`` that represents the local Newton's
    Polyhedron `\Gamma(f)` of the polynomial ``f``.
    """
    return Polyhedron(vertices=f.exponents(),
                      rays=VectorSpace(QQ, f.parent().ngens()).basis())


# FACES
def faces(P):
    r"""
    Return a ``Lattice`` of the faces in the polyhedron ``P`` with a
    partial relation of order defined by the content relation between
    faces.

    EXAMPLES::

        sage: x,y,z = polygens(QQ,'x,y,z')
        sage: f1 = x**3+y**3+z**4
        sage: P = newton_polyhedron(f1)
        sage: faces(P)
        Finite lattice containing 15 elements
    """
    return P.face_lattice()


def proper_faces(P):
    r"""
    Return a list with the proper faces of the polyhedron ``P`` sorted
    in increasing order dimension.

    EXAMPLES::

        sage: x,y,z = polygens(QQ,'x,y,z')
        sage: f1 = x**3+y**3+z**4
        sage: P = newton_polyhedron(f1)
        sage: proper_faces(P)
        [A 0-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex,
         A 0-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex,
         A 0-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex and 1 ray,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex and 1 ray,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex and 1 ray,
         A 2-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices and 2 rays,
         A 2-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 3 vertices,
         A 2-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices and 2 rays,
         A 2-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices and 2 rays]
    """
    return flatten(P.face_lattice().level_sets()[1:-1])


# Informations about faces
def compact_faces(P):
    r"""
    Return a list with the compact faces of the polyhedron ``P``
    sorted in increasing dimension order.

    EXAMPLES::

        sage: x,y,z = polygens(QQ,'x,y,z')
        sage: f1 = x**3+y**3+z**4
        sage: P = newton_polyhedron(f1)
        sage: compact_faces(P)
        [A 0-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex,
         A 0-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex,
         A 0-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 1 vertex,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 2 vertices,
         A 2-dimensional face of a Polyhedron in QQ^3 defined as the convex hull of 3 vertices]
    """
    return [face for face in proper_faces(P) if not face.rays()]


def vertices(tau):
    r"""
    Return a list with the vertices of the face ``tau``.
    """
    return [i.vector() for i in tau.ambient_Vrepresentation() if i.is_vertex()]


def rays(tau):
    r"""
    Return a list with the rays of the face ``tau``.
    """
    return [i.vector() for i in tau.ambient_Vrepresentation() if i.is_ray()]


def translate_points(points_list):
    r"""
    Return a list of re-parametrized points by affine translation
    consider the first point in points_list as the origin.
    """
    origin = points_list[0]
    return [v - origin for v in points_list]


def facet_info(f, facet):
    r"""
    Return a string with the inequality which define the facet, writed in form
    `a_1 x_1 + a_2 x_2 + ... + a_n x_n + b \geq 0`.
    """
    rep = facet.ambient_Hrepresentation()[0]
    message = str(vector(rep.A()).dot_product(vector(f.parent().gens())) + rep.b())
    message += " >= 0"
    return message


def give_all_facets_info(f, P, compact = False):
    r"""
    Print a relation of facets in ``P`` and their associated inequalities.
    """
    for i, facet in enumerate(P.faces(P.dim() - 1)):
        if not (compact and facet.rays()):
            print("    Facet {}: {}".format(i, facet_info(f, facet)))


def face_info_output(tau):
    r"""
    Return a string containing a description of vertices and rays in
    face `\tau`.
    """
    info = "dim " + str(tau.dim()) + ",  vertices = "
    info += str(vertices(tau)) + ",  rays = " + str(rays(tau))
    return info


# Relations Polyhedron-points
def support_points_in_face(f, tau):
    r"""
    Return a list of support points of ``f`` contained in the face ``tau``.
    """
    return [i for i in f.exponents() if tau.as_polyhedron().contains(i)]


# CONES, FANS AND SIMPLE CONES
def primitivize(v):
    r"""
    Return a linearly dependent vector with ``v`` whose components are
    integers whose greatest common divisor is 1.
    """
    return v / gcd(v)


def primitive_vectors(tau):
    r"""
    Return a list of primitive vectors of a face: primitive normal
    vectors to the hyperplanes defining `\tau`.
    """
    return [primitivize(i.A()) for i in tau.ambient_Hrepresentation()]


def cone_from_face(tau):
    r"""
    Construct an object ``Cone`` which represents the dual cone of the
    face ``tau``.

    .. NOTE::

        For the total face, it gives a cone generated by the zero vector.
    """
    gens = primitive_vectors(tau)
    if not gens:
        return Cone([vertices(tau)[0].parent()(0)])
    else:
        return Cone(gens)


def primitive_vectors_cone(cone):
    r"""
    Return a list of primitive rays generators of ``cone``.
    """
    return [ primitivize(i.sparse_vector()) for i in cone.rays() ]


def all_cones(P):
    r"""
    Return a list with all the cones generated by the faces of ``P``.
    """
    return [cone_from_face(f) for f in faces(P)[1:]]


def fan_all_cones(P):
    r"""
    Construct an object ``Fan`` representing the fan of all associated
    cones of ``P``.
    """
    return Fan(all_cones(P), discard_faces=True)


def same_facet(lcone_gens, p, bcone_gens):
    r"""
    Check if ``lcone_gens`` (a cone represented by its generators)
    and the fixed point ``p`` belongs to the same facet of
    ``bcone_gens``.
    """
    for face_cone in Cone(bcone_gens).facets():
        rays_lcone = set(map(tuple, lcone_gens))
        rays_face = set(map(tuple, primitive_vectors_cone(face_cone)))
        if ({tuple(p)}.union(rays_lcone)).issubset(rays_face):
            return True
    return False


def simplicial_partition(cone):
    r"""
    Return a list with the subcones which forms the simplicial
    partition of ``cone``.

    EXAMPLES::

        sage: x,y,z = polygens(QQ,'x,y,z')
        sage: g = x*y + z^3
        sage: P = newton_polyhedron(g)
        sage: tau = compact_faces(P)[0]
        sage: c = cone_from_face(tau)
        sage: simplicial_partition(c)
        [2-d cone in 3-d lattice N,
         3-d cone in 3-d lattice N,
         3-d cone in 3-d lattice N]

        sage: x,y,z = polygens(QQ,'x,y,z')
        sage: f=x^2 + y*z
        sage: P=newton_polyhedron(f)
        sage: faces_set = proper_faces(P)
        sage: faces_set = face_divisors(1, faces_set, P)
        sage: tau = faces_set[1]
        sage: c = cone_from_face(tau)
        sage: simplicial_partition(c)  # BUG HERE
        [2-d cone in 3-d lattice N,
         3-d cone in 3-d lattice N,
         3-d cone in 3-d lattice N]
    """
    if cone.is_simplicial():
        return [cone]

    dict = {}
    F = Fan([cone])
    P = F.cone_lattice()

    # Ordered list of subcones by increasing dimension
    list_subcones = [ls for i in range(1, F.dim() + 1)
                     for ls in F.cones(i)]

    for subcone in list_subcones:
        if subcone.is_simplicial():
            dict[subcone] = [set(subcone.rays())]
        else:
            partition = []
            fixpoint = subcone.rays()[0]
            for subsubcone in list_subcones:
                if (P.is_less_than(subsubcone, subcone) and
                    not same_facet(subsubcone.rays(), fixpoint,
                                   subcone.rays())):
                    for part in dict[subsubcone]:
                        partition += [part.union({fixpoint})]
            dict[subcone] = partition
    return [Cone(c) for c in dict[list_subcones[-1]]]


def cone_info_output(cone, fan_simplicial=None):
    r"""
    Return a string containing information about the generators of the
    cone and its simplicial partition.

    - ``fan_simplicial`` -- a fan with the simplicial partition of ``cone``
      (if there is already calculated).
    """
    F = fan_simplicial
    if F is None:
        F = simplicial_partition(cone)
    info = "cone generators = " + str(primitive_vectors_cone(cone))
    info += ", partition into simplicial cones = "
    info += str(list(map(primitive_vectors_cone, F)))
    return info


def integral_vectors(scone):
    r"""
    Return a list of integral vectors contained in

    .. MATH::

        \{\sum \lambda_j a_j \mid 0\leq \lambda_j <1\}

    where `\{a_j\}` is a basis of the simple cone ``scone``.
    """
    origin = VectorSpace(QQ, scone.lattice_dim()).zero()
    if not scone.dim():
        integrals = [origin]
    else:
        cone_gens = primitive_vectors_cone(scone)
        ngens = len(cone_gens)
        A = matrix(ZZ, cone_gens).transpose()
        D, U, V = A.smith_form()
        diag = D.diagonal()
        coords = mrange(diag, vector)

        # Aux function to scale the vectors on the list
        def escale(v):
            v = vector(QQ, v)
            for i in range(ngens):
                if diag[i] != 0:
                    v[i] = v[i] / diag[i]
                else:
                    v[i] = 0
            return v

        # Aux function 'floor' for vectors component by component
        def floor(v):
            for i in range(ngens):
                v[i] = v[i] - v[i].floor()
            return v
        # Now, we scale and we return to the canonical basis
        L = map(lambda v: V * v, map(escale, coords))
        # Finally, we find the integral vectors of own region
        integrals = map(lambda v: matrix(QQ, A) * v, list(map(floor, L)))
    return list(integrals)


def multiplicity(scone):
    r"""
    Return the multiplicity of a simple cone.
    """
    L = primitive_vectors_cone(scone)
    A = matrix(ZZ, L)
    S = A.smith_form()[0]
    return prod(S[i, i] for i in range(len(L)))


# Sigma and m functions defined in the loc. cit. article
def sigma_vect(v, weights=None):
    r"""
    Return the weighted sum of the components of ``v`` by ``weights``.
    """
    if weights is None:
        return sum(v)
    return vector(v).dot_product(vector(weights))


def m_vect(v, P):
    r"""
    Return `m(v):=\mathop{min}\{v\cdot x \mid x\in P\}` where ``v`` is
    a vector and ``P`` is a ``Polyhedra`` in the affine space.
    """
    vrat = vector(QQ, v)
    return min(vrat.dot_product(x.vector()) for x in P.vertices())


# MONOMIALS ASSOCIATED TO A FACE
def ftau(f, tau):
    r"""
    Return the polynomial `f_{\tau}` associated to the face `\tau` of
    the Newton's Polyhedron of `f`.

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]; p = var('p')
        sage: f1 = x^2 - y^2 + z^3
        sage: P = newton_polyhedron(f1)
        sage: fa = P.faces(2)[1]
        sage: ftau(f1, fa)
        z^3 - y^2
        sage: [ftau(f1, tau) for tau in P.faces(2)]
        [z^3 + x^2 - y^2, z^3 - y^2, x^2 - y^2, z^3 + x^2]
    """
    from sage.rings.polynomial.polydict import ETuple
    # We take a dictionary between the exponents and the coefficients
    # of monomials.
    D = f.dict()
    ring = f.parent()
    vars = ring.gens()
    g = ring.zero()
    for v in support_points_in_face(f, tau):
        g += D[ETuple(v)] * prod(var ** v[i] for i, var in enumerate(vars))
    return g


def solve_in_Fp_x(f, p):
    r"""
    For ``f`` be an integral polynomial, returns the list `[ \{a\in
    (\mathbb{F}_p-0)^d \mid f^*(a)=0\}, \{` vars of `f^*\}]` where
    `f^*` is consider `f` with coefficients in \ `\mathbb{F}_p`, for a
    given prime number ``p``.
    """
    g = f.change_ring(GF(p))    # We can lose variables in GF(p)
    vars = g.variables()
    nvars = g.nvariables()
    h = (GF(p)[vars])(g)
    if len(h.exponents()) == 1:
        sols = []    # If f_tau is a monomial
    else:
        Fp_x_nvars = list(Tuples(range(1, p), nvars))    # (Fp-0)^nvars
        if h == 0:
            return [Fp_x_nvars, vars]
        sols = [a for a in Fp_x_nvars if h(tuple(a)) == 0]
    return sols, vars


def is_degenerated(f_tau, p=None, method='default'):
    r"""
    Checks if the polynomial ``f_tau`` is degenerated over
    `\mathbb{F}_p`, for ``p`` a given prime number ``p`` (see
    [DH01]_).

    If ``p = None``, checks degeneration over `\CC` (which is
    equivalent to be degenerated \ over `\mathbb{F}_p` with `p>>0`).

    For finite fields (``p`` is a given prime):

    - ``method = 'default'`` checks the condition using evaluation over the \
      `(\mathbb{F}_p-0)^n` in the system of equations.

    - ``method = 'ideals'`` checks the condition using ideals over
      the finite field.

    REFERENCES:

    .. [DH01] J . Denef and K . Hoornaert, "Newton Polyhedra and
       Igusa's Local Zeta Function.", 2001.
    """
    bool = False
    vars = f_tau.parent().gens()
    if p not in ZZ:
        S = QQ[vars]
        I = S(f_tau).jacobian_ideal() + S * (S(f_tau))
        bool = prod(S.gens()) not in I.radical()
    else:
        if method == 'ideals':
            S = GF(p)[vars]
            I = S(f_tau).jacobian_ideal() + S * (f_tau)
            for xi in vars:
                I += S * (xi ** (p - 1) - 1)
                # xi unity in Fp iff xi^{(p-1)-1}=0
            bool = 1 not in I    # True if I in NOT the ring (ie, sist. has a solution)
        else:
            candidates, vars = solve_in_Fp_x(f_tau, p)
            if not vars:
                bool = True
            else:
                S = GF(p)[vars]
                g = f_tau.change_ring(GF(p))
                for xi in S.gens():
                    df_tau = S(g).derivative(xi)
                    candidates = [a for a in candidates
                                  if df_tau(tuple(a)) == 0]
                if candidates:
                    bool = True
    return bool


def is_newton_degenerated(f, P, p=None, local=False, method='default', info = True):
    r"""
    Checks if the polynomial ``f`` is degenerated over `\mathbb{F}_p` (``p`` prime) with respect \
    the faces of the polyhedron ``P`` (see [DH01]_).

    If ``p = None``, checks degeneration over `\CC` (which is equivalent to be
    degenerated over `\mathbb{F}_p` with `p>>0`).

    ``local = True`` checks degeneration for local case (only with respect the compact faces).

    For finite fields (``p`` is a given prime):

        - ``method = 'default'`` checks the condition using evaluation over `(\mathbb{F}_p-0)^n` \
    in the system of equations.

        - ``method = 'ideals'`` checks the condition using ideals over the finite field.

    REFERENCES:

    .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
    """
    if local:
        faces_set = compact_faces(P)
    else:
        faces_set = faces(P)[1:]

    for tau in faces_set:
        f_tau = ftau(f, tau)
        if is_degenerated(f_tau, p, method):
            if info:
                #print("The formula for the Igusa zeta function is not valid:")
                if p not in ZZ:
                    print("The polynomial is degenerated at least with respect to the face tau = {" + face_info_output(tau) + "} over the complex numbers!")
                else:
                    print("The polynomial is degenerated at least with respect to the face tau = {" + face_info_output(tau) + "} over GF(" + str(p) + ")!")
            return True
    return False


# IGUSA ZETA FUNCTION
# Values Ntau, Ltau and Stau defined in paper [DH01]
def Ntau(f, tau, p):
    r"""
    Return the number `N_{\tau}`.

    `N_{\tau} = \#\{a\in(\mathbb{F}_p - 0)^d \mid f^*_{\tau}(a)=0\}`

    with `f^*_{\tau}=\mathbb{F}_p(f_{\tau})`

    for a given face `\tau` and `p` a given prime number.

    (see[DH01]_).

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^2 - y^2 + z^3
        sage: P = newton_polyhedron(f)
        sage: [Ntau(f,tau,5) for tau in P.faces(1)]
        [16, 32, 16, 0, 0, 0]

    REFERENCES:

    .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
    """
    n = f.parent().ngens()
    f_tau = ftau(f, tau)
    if p not in ZZ:
        print("You must to give a 'Dictionary' with the number of solutions in GF(" + str(p) + ")^" + str(n) + " associated to each face.")
    else:
        sols, vars = solve_in_Fp_x(f_tau, p)
        return len(sols) * (p - 1) ** (n - len(vars))


def Ltau(f, tau, p, abs_Ntau, s):
    r"""
    Return a list `[L_{\tau}, N_{\tau}]` in terms of a symbolic
    variable `s`.

    If `p` is an abstract prime number, ``abs_Ntau`` is the given
    symbolic expression of `N_{\tau}` in this case (see [DH01]_).

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^2 - y^2 + z^3
        sage: P = newton_polyhedron(f)
        sage: s = var('s')
        sage: [Ltau(f,tau,5,0,s) for tau in P.faces(1)]
        [(16/125*(3*5^(s + 1) + 1)/(5^(s + 1) - 1), 16),
         (32/125*(5^(s + 1) + 3)/(5^(s + 1) - 1), 32),
         (16/125*(3*5^(s + 1) + 1)/(5^(s + 1) - 1), 16),
         (64/125, 0),
         (64/125, 0),
         (64/125, 0)]

    REFERENCES:

    .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
    """
    if p not in ZZ:
        N_tau = abs_Ntau
    else:
        N_tau = Ntau(f, tau, p)

    n = f.parent().ngens()
    p_power_s = p ** s
    # p_power_s = var('Z')
    result = p ** (-n) * ((p - 1) ** n - p * N_tau * ((p_power_s - 1) / (p_power_s * p - 1)))
    return result.factor(), N_tau


def Lgamma(f, p, abs_Ngamma, s):
    r"""
    Return the value `N_{\tau}` for the total polyhedron `\Gamma` in
    terms of a symbolic variable ``s`.

    ``abs_Ngamma`` is the corresponding ``Ngamma`` value for abstract
    prime ``p`` (see [DH01]_).

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^2 - y^2 + z^3
        sage: P = newton_polyhedron(f)
        sage: s = var('s')
        sage: Lgamma(f,7,0,s)
        -24/49*(7^s - 1)/(7*7^s - 1) + 216/343

    REFERENCES:

    .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
    """
    n = f.parent().ngens()
    if p not in ZZ:
        N_gamma = abs_Ngamma
    else:
        sols, vars = solve_in_Fp_x(f, p)
        N_gamma = len(sols) * (p - 1) ** (n - len(vars))
    p_power_s = p ** s
    # p_power_s = var('Z')
    return p ** (-n) * ((p - 1) ** n - p * N_gamma * ((p_power_s - 1) / (p_power_s * p - 1)))


def Stau(f, P, tau, p, weights, s):
    r"""
    Return a list ``[S_tau, cone_info]`` with ``cone_info`` containing
    a string of information about the cones, simplicial partition,
    multiplicity and integral points (see [DH01]_).

    Value ``S_tau`` is expressed in terms of a symbolic variable ``s``.

    REFERENCES:

    .. [DH01] Denef, J. and Hoornaert, K., Newton Polyhedra and Igusa's
        Local Zeta Function, 2001. J. Number Theory 89 (2001), no. 1, 31–64.
    """
    c = cone_from_face(tau)
    dim_cone = c.dim()
    F = simplicial_partition(c)
    result = 0
    for scone in F:
        num = 0
        den = 1
        for h in integral_vectors(scone):
            num += p ** (sigma_vect(h, weights) + m_vect(h, P) * s)
        for a in primitive_vectors_cone(scone):
            den *= (p ** (sigma_vect(a, weights) + m_vect(a, P) * s) - 1)
        result += num / den
        # result = factor(simplify(expand(result + num/den)))
    info = cone_info_output(c, F) + "\n" + "multiplicities = " + str(list(map(multiplicity, F))) + ", integral points = " + str(list(map(integral_vectors, F)))
    return result, info




# TOPOLOGICAL ZETA FUNCTION
# Calculation of the expression Jtau defined in paper [DL92]
def Jtau(tau, P, weights, s):
    r"""
    Return a list [J_tau, cone_info] with ``cone_info`` containing a
    string of information about the cones, simplicial partition,
    multiplicity and integral points. (see [DenLoe]_)

    Value J_tau is defined in terms of a symbolic variable ``s``.

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f=x^2 + y*z
        sage: s = var('s')
        sage: P=newton_polyhedron(f)
        sage: faces_set = proper_faces(P)
        sage: faces_set = face_divisors(1, faces_set, P)
        sage: Jtau(faces_set[1], P, None, s)[0]
        (2*s + 5)/(2*s + 3)^2

    REFERENCES::

    .. [DL92] Denef, J. and Loeser, F., Caractéristiques d'Euler-Poincaré,
    fonctions zêta locales et modifications analytiques, J. Amer. Math. Soc.
    5 (1992), no. 4, 05–720.
    """
    c = cone_from_face(tau)
    dim_cone = c.dim()
    F = simplicial_partition(c)
    if dim_cone == 0:
        result = 1
    else:
        result = 0
        for scone in F:
            if scone.dim() == dim_cone:
                num = multiplicity(scone)
                den = 1
                for a in primitive_vectors_cone(scone):
                    den *= (m_vect(a, P) * s + sigma_vect(a, weights))
                result = factor(simplify(expand(result + num / den)))
    cone_info = cone_info_output(c, F) + "\n" + "multiplicities = " + str(list(map(multiplicity, F))) + ", integral points = " + str(list(map(integral_vectors, F)))
    return result, cone_info


# MONODROMY ZETA FUNCTION
# Calculation of the expression Mtau defined in [Var76]
def Mtau(tau):
    r"""
    Return the value `M_{\tau}` (the monodromy zeta factor associated to a face) 
    for `\tau` a face in `P` in terms of a symbolic variable `s`.

    INPUT:

    - `\tau` -- a face of a Newton polyhedron `P`

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^2 - y^2 + z^3
        sage: P = newton_polyhedron(f)
        sage: [Mtau(tau) for tau in P.faces(1)]
        [-t^6 + 1, -t^2 + 1, -t^6 + 1, 1, 1, 1]

        sage: g = x*y + z^3
        sage: P = newton_polyhedron(g)
        sage: [Mtau(tau) for tau in P.faces(1)]
        [1, -t + 1, -t^3 + 1, -t + 1, -t^3 + 1, 1]
        sage: [Mtau(tau) for tau in compact_faces(P)]
        [-t^3 + 1, 1, 1]

    REFERENCES::

    .. [Var76] Varchenko, A. N., Zeta-function of monodromy and Newton's
    diagram. Invent. Math. 37 (1976), no. 3, 253–262.
    """
    P = tau.polyhedron()

    t = polygen(QQ, 't')
    ring_t = t.parent()
    s = polygen(QQ, 's')
    ring_s = s.parent()

    c = cone_from_face(tau)
    dim_cone = c.dim()

    result = ring_t.one()
    for scone in simplicial_partition(c):
        if scone.dim() == dim_cone:
            mult = multiplicity(scone)
            den = ring_s.one()
            for a in primitive_vectors_cone(scone):
                den *= (m_vect(a, P) * s + sum(a))
            if den.degree() == 1:
                M = s * den.subs(s=~s)
                result *= (1 - t ** (M.subs(s=0) / mult))
    return result


def face_volume(f, tau):
    r"""
    Return the value `\mathop{Vol}(\tau)\cdot(\mathop{dim}\tau)!`, for
    a given face ``tau`` .

    `\mathop{Vol}(\tau)` is defined as follows:

    Let `\omega_\tau` be the volume form over `\mathop{Aff}(\tau)`,
    the affine space generated \ by `\tau` such that the
    parallelepiped spanned by a lattice basis of
    `\mathop{Aff}(\tau)\cap\ZZ^n`` has volume 1. Then
    `\mathop{Vol}(\tau)` is the volume of `\tau` intersection the
    Global Newton \ Polyhedron of ``f`` with respect to `\omega_\tau`
    (see [DL92]_).

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^2 - y^2 + z^3
        sage: P = newton_polyhedron(f)
        sage: [face_volume(f, tau) for tau in P.faces(1)]
        [1, 2, 1, 0, 0, 0]

    REFERENCES::

    .. [DL92] Denef, J. and Loeser, F., Caractéristiques d'Euler-Poincaré,
    fonctions zêta locales et modifications analytiques, J. Amer. Math. Soc.
    5 (1992), no. 4, 05–720.
    """
    n = f.parent().ngens()
    dim_tau = tau.dim()
    result = 0
    if dim_tau:
        tau_in_global = Polyhedron(vertices=support_points_in_face(f, tau))
        vertices_in_global = [ vector(v) for v in tau_in_global.vertices() ]
        trans_vertices = translate_points(vertices_in_global)
        if matrix(ZZ, trans_vertices).rank() == dim_tau:
            V = QQ ** n
            basis_aff = V.submodule(trans_vertices).intersection(ZZ ** n).basis()
            W = V.submodule_with_basis(basis_aff)
            coords_list = list(map(W.coordinate_vector, trans_vertices))
            p = PointConfiguration(coords_list)
            result = p.volume()    # Return dimtau!*n-volume of tau
    else:
        result = 1
    return result


def face_divisors(d, faces_set, P):
    r"""
    Return a list of faces `\tau` in ``faces_set`` such that ``d`` divides
    `m(\Delta_\tau) = \mathop{gcd}\{m(a) \mid a\in\Delta_\tau\cap\ZZ^n\}`
    where `\Delta_\tau` is the associated cone of `\tau`.

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^2 - y^2 + z^3
        sage: P = newton_polyhedron(f)
        sage: face_divisors(3, P.faces(1), P)
        [A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull 
         of 2 vertices,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull 
         of 2 vertices,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull 
         of 1 vertex and 1 ray,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull 
         of 1 vertex and 1 ray,
         A 1-dimensional face of a Polyhedron in QQ^3 defined as the convex hull
         of 1 vertex and 1 ray]
    """
    if d == 1:
        return faces_set
    L_faces = []
    dim_total = P.dim()
    for tau in faces_set:
        c = cone_from_face(tau)
        F = simplicial_partition(c)
        L_vectors = []
        # We need to evaluate m over the basis of the cone and the
        # integral points views above.
        for scone in F:
            L_vectors += integral_vectors(scone) + primitive_vectors_cone(scone)
        l = gcd(m_vect(i, P) for i in L_vectors)
        if d.divides(l):
            L_faces.append(tau)
    return L_faces


def is_global_degenerated(f, p=None, method='default'):
    r"""
    Check if the polynomial ``f`` is degenerated over `\mathbb{F}_p`
    (``p`` prime) with respect to the faces of the Global Newton
    Polyhedron of ``f`` (see [DL92]_).

    If ``p = None``, checks degeneration over `\CC` (which is equivalent to be
    degenerated over `\mathbb{F}_p` with `p>>0`).

    ``local = True`` checks degeneration for local case (only with respect the compact faces).

    For finite fields (``p`` is a given prime):

    - ``method = 'default'`` checks the condition using evaluation over `(\mathbb{F}_p-0)^n` in the system of equations.

    - ``method = 'ideals'`` checks the condition using ideals over the finite field.

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^2 - y^2 + z^3
        sage: is_global_degenerated(f)
        False
    """
    Q = f.newton_polytope()  # Global Newton Polyhedron of f

    for tau in faces(Q)[1:]:
        f_tau = ftau(f, tau)
        if is_degenerated(f_tau, p, method):
            print("The formula for the Topological zeta function is not valid:")
            if p not in ZZ:
                print("The polynomial is degenerated at least "
                      "with respect to the face tau = {" + face_info_output(tau) + "} over the complex numbers!")
            else:
                print("The polynomial is degenerated at least with respect to the face tau = {" + face_info_output(tau) + "} over GF(" + str(p) + ")!")
            return True
    return False
