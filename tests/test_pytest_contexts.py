import pathlib

def test_basic_given_when_should(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example1.py'
    testdir.makepyfile(example.read_text())

    result = testdir.runpytest()
    print(vars(result))
    result.assert_outcomes(passed=1)


def test_two_shoulds_and_one_ignorable_class(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example2.py'
    testdir.makepyfile(example.read_text())
    result = testdir.runpytest()
    result.assert_outcomes(passed=1, failed=1)
