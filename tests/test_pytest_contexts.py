from textwrap import dedent
import contexts
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


def test_test_names(testdir):
    example = dedent(
        """
        class WhenWeSeeTestOutput:
            def it_should_have_a_nice_name(self):
                assert 1 == 2
        """
    )
    testdir.makepyfile(example)
    result = testdir.runpytest()
    assert 'test_test_names.py:WhenWeSeeTestOutput.it_should_have_a_nice_name' in result.stdout.str()


def test_sane_traceback(testdir):
    example = dedent(
        """
        class WhenWeFail:
            def it_should_prune_tracebacks(self):
                assert 1 == 2
        """
    )
    testdir.makepyfile(example)
    result = testdir.runpytest()
    assert 'test_sane_traceback.py:WhenWeFail.it_should_prune_tracebacks' in result.stdout.str()
    assert result.stdout.str().count('/pytest_pytest_contexts.py') == 1

