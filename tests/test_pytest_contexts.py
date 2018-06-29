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


def test_cleanup(testdir):
    example = dedent(
        """
        class WhenWeSeeTestOutput:
            def it_should_have_a_nice_name(self):
                assert 1 == 2

            def cleanup_temp_file(self):
                print('CLEEEEEANING')
        """
    )
    testdir.makepyfile(example)
    result = testdir.runpytest()
    assert 'CLEEEEEANING' in result.stdout.str()


def test_Spec_works(testdir):
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


def test_only_runs_givens_and_cleanups_once_for_multiple_shoulds(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example6.py'
    testdir.makepyfile(example.read_text())
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_runs_cleanups_after_all_the_tests(testdir):
    example = pathlib.Path(__file__).parent / '../examples/example7.py'
    testdir.makepyfile(example.read_text())
    result = testdir.runpytest()
    result.assert_outcomes(passed=2)


def test_test_names(testdir):
    example = dedent(
        """
        class WhenWeSeeTestOutput:
            def it_should_have_a_nice_name(self):
                assert 1 == 2
        """
    )
    expected_test_name = 'test_test_names.py:WhenWeSeeTestOutput.it_should_have_a_nice_name'

    testdir.makepyfile(example)
    result = testdir.runpytest()
    assert expected_test_name in result.stdout.str()


def test_sane_traceback(testdir):
    example = dedent(
        """
        def myfn():
            assert 1 == 2

        class WhenWeFail:
            def it_should_prune_tracebacks(self):
                myfn()
        """
    )
    testdir.makepyfile(example)
    output = testdir.runpytest().stdout.str()
    assert 'assert 1 == 2' in output
    assert 'test_sane_traceback.py:6:' in output
    assert 'test_sane_traceback.py:2:' in output
    assert '/_pytest' not in output
    assert '/pluggy/' not in output
    assert '/pytest_pytest_contexts.py' not in output

