"""
Tests that use mocks tend to be more coupled to the implementation details of the codebase.
That’s because mock tests verify the interactions between things.
This coupling between code and test tends to make tests more fragile.
Overuse of mocks leads to complicated test suites that fail to explain the code.

Let's just use test double instead.
https://github.com/testdouble/contributing-tests/wiki/Test-Double

A good practice is to feel free to throw away tests when thinking they’re not going to add value longer term.
"""
