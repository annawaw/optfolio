from unittest import TestCase
import score


class TestScore(TestCase):
    def test_target_price_score(self):
        self.assertEqual(50, score.target_price_score(4.0, 4.0))
        self.assertEqual(
            [98.2, 84.03, 64.75, 50.0, 36.59, 8.79, 1.8],
            [round(score.target_price_score(x, 1.0), 2) for x in [0.5, 0.75, 0.9, 1.0, 1.1, 1.5, 2.0]]
        )

    def test_pe_score(self):
        self.assertEqual(
            [98.2, 88.08, 69.64, 50.0, 34.44, 23.69, 11.92, 1.8],
            [round(score.pe_score(x), 2) for x in [5, 10, 15, 20, 25, 30, 40, 80]]
        )

    def test_dividend_score(self):
        self.assertEqual(
            [0.03, 3.49, 22.86, 50.0, 75.03, 89.13, 99.08, 99.97],
            [round(score.dividend_score(x, 1.0), 2) for x in [0.5, 0.75, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0]]
        )

    def test_dividend_payout_score(self):
        self.assertEqual(
            [100.0, 100.0, 100.0, 99.78, 88.08, 51.51, 33.92, 11.92, 5.73, 0.0],
            [round(score.dividend_payout_score(x), 2) for x in [0.1, 0.2, 0.25, 0.33, 0.5, 0.66, 0.75, 1.0, 1.25, -0.25]]
        )

    def test_growth_score(self):
        self.assertEqual(
            [0.02, 8.27, 14.19, 23.04, 34.9, 48.69, 62.43, 74.21, 83.15, 89.33, 93.37, 95.91, 97.48, 99.76, 99.97, 100.0],
            [round(score.growth_score(x), 2) for x in [-0.1, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2, 0.3]]
        )