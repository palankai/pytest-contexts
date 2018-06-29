import pathlib

def test_basic_given_when_should(testdir):
    example = pathlib.Path(__file__).parent / '../examples/given.py'
    print(example.read_text())
    testdir.makepyfile(example.read_text())

    result = testdir.runpytest()
    result.assert_outcomes(passed=1, failed=1)
