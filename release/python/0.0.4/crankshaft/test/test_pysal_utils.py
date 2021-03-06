import unittest

import crankshaft.pysal_utils as pu
from crankshaft import random_seeds


class PysalUtilsTest(unittest.TestCase):
    """Testing class for utility functions related to PySAL integrations"""

    def setUp(self):
        self.params = {"id_col": "cartodb_id",
                       "attr1": "andy",
                       "attr2": "jay_z",
                       "subquery": "SELECT * FROM a_list",
                       "geom_col": "the_geom",
                       "num_ngbrs": 321}

    def test_query_attr_select(self):
        """Test query_attr_select"""

        ans = "i.\"{attr1}\"::numeric As attr1, " \
              "i.\"{attr2}\"::numeric As attr2, "

        self.assertEqual(pu.query_attr_select(self.params), ans)

    def test_query_attr_where(self):
        """Test pu.query_attr_where"""

        ans = "idx_replace.\"{attr1}\" IS NOT NULL AND " \
              "idx_replace.\"{attr2}\" IS NOT NULL AND " \
              "idx_replace.\"{attr2}\" <> 0"

        self.assertEqual(pu.query_attr_where(self.params), ans)

    def test_knn(self):
        """Test knn neighbors constructor"""

        ans = "SELECT i.\"cartodb_id\" As id, " \
                     "i.\"andy\"::numeric As attr1, " \
                     "i.\"jay_z\"::numeric As attr2, " \
                     "(SELECT ARRAY(SELECT j.\"cartodb_id\" " \
                                   "FROM (SELECT * FROM a_list) As j " \
                                   "WHERE " \
                                    "i.\"cartodb_id\" <> j.\"cartodb_id\" AND " \
                                    "j.\"andy\" IS NOT NULL AND " \
                                    "j.\"jay_z\" IS NOT NULL AND " \
                                    "j.\"jay_z\" <> 0 " \
                                   "ORDER BY " \
                                    "j.\"the_geom\" <-> i.\"the_geom\" ASC " \
                      "LIMIT 321)) As neighbors " \
              "FROM (SELECT * FROM a_list) As i " \
              "WHERE i.\"andy\" IS NOT NULL AND " \
                    "i.\"jay_z\" IS NOT NULL AND " \
                    "i.\"jay_z\" <> 0 " \
              "ORDER BY i.\"cartodb_id\" ASC;"

        self.assertEqual(pu.knn(self.params), ans)

    def test_queen(self):
        """Test queen neighbors constructor"""

        ans = "SELECT i.\"cartodb_id\" As id, " \
                     "i.\"andy\"::numeric As attr1, " \
                     "i.\"jay_z\"::numeric As attr2, " \
                     "(SELECT ARRAY(SELECT j.\"cartodb_id\" " \
                                   "FROM (SELECT * FROM a_list) As j " \
                                   "WHERE " \
                                   "i.\"cartodb_id\" <> j.\"cartodb_id\" AND " \
                                   "ST_Touches(i.\"the_geom\", " \
                                              "j.\"the_geom\") AND " \
                                   "j.\"andy\" IS NOT NULL AND " \
                                   "j.\"jay_z\" IS NOT NULL AND " \
                                   "j.\"jay_z\" <> 0)" \
                                  ") As neighbors " \
              "FROM (SELECT * FROM a_list) As i " \
              "WHERE i.\"andy\" IS NOT NULL AND " \
                    "i.\"jay_z\" IS NOT NULL AND " \
                    "i.\"jay_z\" <> 0 " \
              "ORDER BY i.\"cartodb_id\" ASC;"

        self.assertEqual(pu.queen(self.params), ans)

    def test_construct_neighbor_query(self):
        """Test construct_neighbor_query"""

        # Compare to raw knn query
        self.assertEqual(pu.construct_neighbor_query('knn', self.params),
                         pu.knn(self.params))

    def test_get_attributes(self):
        """Test get_attributes"""

        ## need to add tests

        self.assertEqual(True, True)

    def test_get_weight(self):
        """Test get_weight"""

        self.assertEqual(True, True)

    def test_empty_zipped_array(self):
        """Test empty_zipped_array"""
        ans2 = [(None, None)]
        ans4 = [(None, None, None, None)]
        self.assertEqual(pu.empty_zipped_array(2), ans2)
        self.assertEqual(pu.empty_zipped_array(4), ans4)
