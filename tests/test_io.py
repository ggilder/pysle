import unittest
import os

from pysle import phonetics
from pysle.utilities import isle_io

root = os.path.dirname(os.path.realpath(__file__))
dataRoot = os.path.join(root, "files")


class TestIO(unittest.TestCase):
    def test_opening_isle_files(self):
        sut = isle_io.readIsleDict(os.path.join(dataRoot, "isle_sample.txt"))

        self.assertEqual(23, len(sut.keys()))

        entry = sut.get("another")[0]

        expectedSyllabification = [["ə"], ["n", "ˈʌ"], ["ð", "ɚ"]]
        expectedEntry = phonetics.Entry(
            "another", [expectedSyllabification], ["dt", "nn", "prp"]
        )

        self.assertEqual(expectedEntry, entry)

    def test_groups_entries_with_the_same_word(self):
        sut = isle_io.readIsleDict(os.path.join(dataRoot, "isle_sample.txt"))
        entries = sut.get("with")

        self.assertEqual(2, len(entries))

        expectedPosList = ["in", "nnp", "rp"]
        firstExpectedSyllabification = [["w", "ɪ", "ð"]]
        firstExpectedEntry = phonetics.Entry(
            "with", [firstExpectedSyllabification], expectedPosList
        )
        self.assertEqual(firstExpectedEntry, entries[0])

        secondExpectedSyllabification = [["w", "ɪ", "ɵ"]]
        secondExpectedEntry = phonetics.Entry(
            "with", [secondExpectedSyllabification], expectedPosList
        )
        self.assertEqual(secondExpectedEntry, entries[1])

    def test_can_read_multiword_entries(self):
        sut = isle_io.readIsleDict(os.path.join(dataRoot, "isle_sample.txt"))

        entries = sut.get("pumpkins_parley")
        self.assertEqual(1, len(entries))

        entry = entries[0]
        self.assertEqual(2, len(entry.syllabificationList))

        expectedSyllabificationList = [
            [["p", "ˈʌ", "m"], ["k", "n̩", "z"]],
            [["p", "ˈɑ", "ɹ"], ["l", "i"]],
        ]
        expectedPosList = ["nns"]
        expectedEntry = phonetics.Entry(
            "pumpkins_parley", expectedSyllabificationList, expectedPosList
        )

        self.assertEqual(expectedEntry, entry)
