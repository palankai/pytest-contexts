from textwrap import dedent
import pathlib

def test_basic_given_when_should(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example1.py'
    testdir.makepyfile(example.read_text())

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_two_shoulds_and_one_ignorable_class(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example2.py'
    testdir.makepyfile(example.read_text())
    result = testdir.runpytest()
    result.assert_outcomes(passed=1, failed=1)


def test_we_still_run_regular_pytest_scripts(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example3.py'
    testdir.makepyfile(example.read_text())
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_examples(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example4.py'
    testdir.makepyfile(example.read_text())
    result = testdir.runpytest()
    result.assert_outcomes(passed=1, failed=1)


def test_spec(testdir):
    example = dedent(
        """
        class MyTestSpec:
            def it_should_be_run(self):
                assert True
        """
    )
    testdir.makepyfile(example)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_decorators(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example5.py'
    testdir.makepyfile(example.read_text())
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
