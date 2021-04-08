import unittest
import cepimose
import datetime


class CepimoseTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_vaccinations_by_day(self):
        # Test feature one.
        data = cepimose.vaccinations_by_day()
        self.assertTrue(len(data) > 30)

        def assertRow(row, expected_date, expected_first, expected_second):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.first_dose, expected_first, delta=10)
            self.assertAlmostEqual(row.second_dose, expected_second, delta=5)

        #! NIJZ is changing data tests could fail in the future
        assertRow(data[9], datetime.datetime(2021, 1, 5), 15711, 0)
        assertRow(data[22], datetime.datetime(2021, 1, 18), 48711, 315)

    def test_vaccinations_by_age(self):
        # Test feature one.
        data = {row.age_group: row for row in cepimose.vaccinations_by_age()}

        expected_age_groups = [
            "0-17",
            "18-24",
            "25-29",
            "30-34",
            "35-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            "65-69",
            "70-74",
            "75-79",
            "80-84",
            "85-89",
            "90+",
        ]

        self.assertTrue(len(data), len(expected_age_groups))

        for grp in expected_age_groups:
            self.assertGreater(data[grp].count_first, 0)
            self.assertGreater(data[grp].share_first, 0)
            self.assertGreater(data[grp].count_second, 0)
            self.assertGreater(data[grp].share_second, 0)

    def test_vaccinations_by_region(self):
        # Test feature one.
        data = {row.region: row for row in cepimose.vaccinations_by_region()}

        expected_regions = [
            "Koroška",
            "Zasavska",
            "Goriška",
            "Posavska",
            "Gorenjska",
            "Podravska",
            "Pomurska",
            "Osrednjeslovenska",
            "Jugovzhodna Slovenija",
            "Primorsko-notranjska",
            "Savinjska",
            "Obalno-kraška",
        ]

        print(data.keys())

        self.assertTrue(len(data), len(expected_regions))

        for grp in expected_regions:
            self.assertGreater(data[grp].count_first, 0)
            self.assertGreater(data[grp].share_first, 0)
            self.assertGreater(data[grp].count_second, 0)
            self.assertGreater(data[grp].share_second, 0)

    def test_vaccine_supply_and_usage(self):
        data = cepimose.vaccines_supplied_and_used()
        self.assertTrue(len(data) > 30)

        def assertRow(row, expected_date, expected_supp, expected_used):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.supplied, expected_supp, delta=10)
            self.assertAlmostEqual(row.used, expected_used, delta=10)

        #! NIJZ is changing data tests could fail in the future
        assertRow(data[9], datetime.datetime(2021, 1, 4), 39780, 13248)
        assertRow(data[22], datetime.datetime(2021, 1, 17), 60870, 48799)

    def test_supplied_by_manufacturer(self):
        data = cepimose.vaccines_supplied_by_manufacturer()
        self.assertTrue(len(data) > 10)

        def assertRow(row, expected_date, expected):
            self.assertEqual(row.date, expected_date)
            self.assertEqual(row.pfizer, expected[0])
            self.assertEqual(row.moderna, expected[1])
            self.assertEqual(row.az, expected[2])

        assertRow(data[1], datetime.datetime(2020, 12, 30), [8190, None, None])  # R = 2
        assertRow(data[3], datetime.datetime(2021, 1, 11), [19890, None, None])  # R = 6
        assertRow(
            data[16], datetime.datetime(2021, 2, 25), [None, None, 16800]
        )  # R = None
        assertRow(data[17], datetime.datetime(2021, 2, 25), [None, 8400, None])  # R = 1

    def test_supplied_by_manufacturer_cumulative(self):
        data = cepimose.vaccines_supplied_by_manufacturer_cumulative()
        self.assertTrue(len(data) > 10)

        def assertRow(row, expected_date, expected):
            self.assertEqual(row.date, expected_date)
            self.assertEqual(row.pfizer, expected[0])
            self.assertEqual(row.moderna, expected[1])
            self.assertEqual(row.az, expected[2])

        assertRow(data[3], datetime.datetime(2021, 1, 11), [59670, None, None])
        assertRow(data[7], datetime.datetime(2021, 1, 31), [None, 3600, None])
        assertRow(data[10], datetime.datetime(2021, 2, 6), [None, None, 9600])
        assertRow(data[16], datetime.datetime(2021, 2, 25), [None, 16800, 52800])
        assertRow(
            data[len(data) - 1], datetime.datetime(2021, 4, 2), [285480, 46800, 144000]
        )  # this test will fail in the future

    def test_vaccination_by_age_range_90(self):
        data = cepimose.vaccinations_by_age_range_90()
        data_dose1 = data.dose1
        data_dose2 = data.dose2

        self.assertTrue(len(data_dose1) > 10)
        self.assertTrue(len(data_dose2) > 10)
        self.assertTrue(len(data_dose1) > len(data_dose2))
        self.assertTrue(len(data_dose1) - len(data_dose2) == 12)

        def assertRow(row, expected_date, expected_dose):
            self.assertEqual(row.date, expected_date)
            self.assertAlmostEqual(row.dose, expected_dose, delta=5)

        assertRow(data_dose1[21], datetime.datetime(2021, 1, 17), 3580)
        assertRow(data_dose1[70], datetime.datetime(2021, 3, 7), 7866)
        assertRow(data_dose2[9], datetime.datetime(2021, 1, 17), 1)
        assertRow(data_dose2[58], datetime.datetime(2021, 3, 7), 4821)
