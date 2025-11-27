import unittest

from src.functional_queries import (
    yearly_sales_summary,
    top_towns_by_total_sales,
    residential_type_stats,
    price_to_assessed_ratio,
    total_sales_all,
    total_sales_year,
    top_towns_by_average_price,
    price_distribution,
    outlier_towns,
    quarterly_trend,
)


class RealEstateSmallUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        # Small handcrafted sample that matches your record structure
        # Each record is a dict with:
        #   town, year, quarter, year_quarter, sale_amount,
        #   property_type, residential_type, assessed_value
        self.records = [
            {
                "town": "Alpha",
                "year": 2021,
                "quarter": 1,
                "year_quarter": "2021-Q1",
                "sale_amount": 100_000.0,
                "property_type": "Residential",
                "residential_type": "Single Family",
                "assessed_value": 80_000.0,
            },
            {
                "town": "Alpha",
                "year": 2021,
                "quarter": 2,
                "year_quarter": "2021-Q2",
                "sale_amount": 150_000.0,
                "property_type": "Residential",
                "residential_type": "Single Family",
                "assessed_value": 120_000.0,
            },
            {
                "town": "Beta",
                "year": 2021,
                "quarter": 1,
                "year_quarter": "2021-Q1",
                "sale_amount": 200_000.0,
                "property_type": "Residential",
                "residential_type": "Condo",
                "assessed_value": 150_000.0,
            },
            {
                "town": "Beta",
                "year": 2022,
                "quarter": 1,
                "year_quarter": "2022-Q1",
                "sale_amount": 250_000.0,
                "property_type": "Commercial",
                "residential_type": "",
                "assessed_value": 0.0,
            },
            {
                "town": "Gamma",
                "year": 2022,
                "quarter": 2,
                "year_quarter": "2022-Q2",
                "sale_amount": 300_000.0,
                "property_type": "Residential",
                "residential_type": "Two Family",
                "assessed_value": 200_000.0,
            },
        ]

    # ---------- total_sales_all ----------
    def test_total_sales_all(self) -> None:
        # 100k + 150k + 200k + 250k + 300k = 1,000,000
        self.assertEqual(total_sales_all(self.records), 1_000_000.0)

    def test_total_sales_all_empty(self) -> None:
        self.assertEqual(total_sales_all([]), 0.0)

    # ---------- total_sales_year ----------
    def test_total_sales_year_2021(self) -> None:
        # 2021: 100k + 150k + 200k = 450k
        self.assertEqual(total_sales_year(self.records, 2021), 450_000.0)

    def test_total_sales_year_2022(self) -> None:
        # 2022: 250k + 300k = 550k
        self.assertEqual(total_sales_year(self.records, 2022), 550_000.0)

    def test_total_sales_year_no_data(self) -> None:
        self.assertEqual(total_sales_year(self.records, 2019), 0.0)

    # ---------- yearly_sales_summary ----------
    def test_yearly_sales_summary_basic(self) -> None:
        summary = yearly_sales_summary(self.records)
        # Should have entries for 2021 and 2022
        years = [row["year"] for row in summary]
        self.assertEqual(years, [2021, 2022])

        # Check totals
        totals = {row["year"]: row["total_sales"] for row in summary}
        self.assertEqual(totals[2021], 450_000.0)
        self.assertEqual(totals[2022], 550_000.0)

    # ---------- top_towns_by_total_sales ----------
    def test_top_towns_by_total_sales(self) -> None:
        result = top_towns_by_total_sales(self.records, start_year=2021)
        # Totals:
        #   Beta  = 450k
        #   Gamma = 300k
        #   Alpha = 250k
        self.assertEqual(result[0]["town"], "Beta")
        self.assertEqual(result[0]["total_sales"], 450_000.0)
        self.assertEqual(len(result), 3)

    # ---------- residential_type_stats ----------
    def test_residential_type_stats(self) -> None:
        stats = residential_type_stats(self.records)
        types = [row["type"] for row in stats]

        # We expect three types: Single Family, Condo, Two Family
        self.assertIn("Single Family", types)
        self.assertIn("Condo", types)
        self.assertIn("Two Family", types)

        # Two Family has the highest median (300k)
        self.assertEqual(stats[0]["type"], "Two Family")
        self.assertEqual(stats[0]["median"], 300_000.0)

    # ---------- price_to_assessed_ratio ----------
    def test_price_to_assessed_ratio(self) -> None:
        ratios = price_to_assessed_ratio(self.records, min_count=1)
        towns = {row["town"]: row["avg_ratio"] for row in ratios}

        # Ratios:
        #   Alpha: 100/80=1.25 and 150/120=1.25  -> 1.25
        #   Beta:  200/150 ≈ 1.3333
        #   Gamma: 300/200 = 1.5
        self.assertAlmostEqual(towns["Alpha"], 1.25, places=2)
        self.assertAlmostEqual(towns["Beta"], 4 / 3, places=2)
        self.assertAlmostEqual(towns["Gamma"], 1.5, places=2)

        # Gamma should be highest
        ratios_sorted = sorted(ratios, key=lambda x: x["avg_ratio"], reverse=True)
        self.assertEqual(ratios_sorted[0]["town"], "Gamma")

    # ---------- top_towns_by_average_price ----------
    def test_top_towns_by_average_price_basic(self) -> None:
        # For 2021:
        #   Alpha avg = (100k + 150k) / 2 = 125k
        #   Beta  avg = 200k
        result = top_towns_by_average_price(self.records, year=2021, min_count=1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["town"], "Beta")
        self.assertAlmostEqual(result[0]["avg_price"], 200_000.0)

    def test_top_towns_by_average_price_no_year_data(self) -> None:
        result = top_towns_by_average_price(self.records, year=2019, min_count=1)
        self.assertEqual(result, [])

    # ---------- price_distribution ----------
    def test_price_distribution_insufficient_data_returns_empty(self) -> None:
        # For 2021 there are only 3 Residential + 0 Commercial>=10
        dist = price_distribution(self.records, year=2021)
        self.assertEqual(dist, [])

    def test_price_distribution_basic(self) -> None:
        # Build synthetic 10 Residential records for 2022 to exercise percentile logic
        base_prices = [
            100_000.0,
            150_000.0,
            200_000.0,
            250_000.0,
            300_000.0,
            350_000.0,
            400_000.0,
            450_000.0,
            500_000.0,
            550_000.0,
        ]
        many_records = []
        for p in base_prices:
            many_records.append(
                {
                    "town": "Delta",
                    "year": 2022,
                    "quarter": 1,
                    "year_quarter": "2022-Q1",
                    "sale_amount": p,
                    "property_type": "Residential",
                    "residential_type": "Single Family",
                    "assessed_value": p * 0.8,
                }
            )

        dist = price_distribution(many_records, year=2022)
        self.assertEqual(len(dist), 1)
        row = dist[0]

        self.assertEqual(row["property_type"], "Residential")
        self.assertEqual(row["count"], 10)
        # n = 10 → indices: int(0.25*n)=2, int(0.50*n)=5, int(0.75*n)=7
        self.assertEqual(row["p25"], 200_000.0)
        self.assertEqual(row["median"], 350_000.0)
        self.assertEqual(row["p75"], 450_000.0)
        self.assertEqual(row["iqr"], 250_000.0)

       # ---------- outlier_towns ----------
    def test_outlier_towns_basic(self) -> None:
        records = []

        # HighOutlierTown: 35 normal + 5 extreme outliers
        for _ in range(35):
            records.append(
                {
                    "town": "HighOutlierTown",
                    "year": 2022,
                    "quarter": 1,
                    "year_quarter": "2022-Q1",
                    "sale_amount": 100_000.0,
                    "property_type": "Residential",
                    "residential_type": "Single Family",
                    "assessed_value": 80_000.0,
                }
            )
        for _ in range(5):
            records.append(
                {
                    "town": "HighOutlierTown",
                    "year": 2022,
                    "quarter": 1,
                    "year_quarter": "2022-Q1",
                    "sale_amount": 1_000_000.0,
                    "property_type": "Residential",
                    "residential_type": "Single Family",
                    "assessed_value": 80_000.0,
                }
            )

        # NormalTown: 39 normal + 1 extreme outlier
        for _ in range(39):
            records.append(
                {
                    "town": "NormalTown",
                    "year": 2022,
                    "quarter": 1,
                    "year_quarter": "2022-Q1",
                    "sale_amount": 100_000.0,
                    "property_type": "Residential",
                    "residential_type": "Single Family",
                    "assessed_value": 80_000.0,
                }
            )
        records.append(
            {
                "town": "NormalTown",
                "year": 2022,
                "quarter": 1,
                "year_quarter": "2022-Q1",
                "sale_amount": 1_000_000.0,
                "property_type": "Residential",
                "residential_type": "Single Family",
                "assessed_value": 80_000.0,
            }
        )

        outliers = outlier_towns(records, year=2022)

        # Both towns should appear, ordered by outlier_rate descending
        self.assertEqual(len(outliers), 2)
        self.assertEqual(outliers[0]["town"], "HighOutlierTown")
        self.assertEqual(outliers[1]["town"], "NormalTown")

        # HighOutlierTown: 5/40 = 12.5% outliers
        # NormalTown:      1/40 =  2.5% outliers
        self.assertGreater(outliers[0]["outlier_rate"], outliers[1]["outlier_rate"])
        self.assertEqual(outliers[0]["count"], 40)
        self.assertEqual(outliers[1]["count"], 40)


    def test_outlier_towns_empty(self) -> None:
        self.assertEqual(outlier_towns([], year=2022), [])

    # ---------- quarterly_trend ----------
    def test_quarterly_trend(self) -> None:
        trend = quarterly_trend(self.records, window=2)
        # We have 4 distinct quarters: 2021-Q1, 2021-Q2, 2022-Q1, 2022-Q2
        self.assertEqual(len(trend), 4)

        # First quarter has no moving average
        self.assertIsNone(trend[0]["moving_avg"])
        self.assertEqual(trend[0]["year_quarter"], "2021-Q1")

        # Last quarter should be 2022-Q2 with count = 1
        self.assertEqual(trend[-1]["year_quarter"], "2022-Q2")
        self.assertEqual(trend[-1]["count"], 1)


if __name__ == "__main__":
    unittest.main()
