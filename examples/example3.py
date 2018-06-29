class When_we_have_a_test:

    def when_things_happen(self):
        pass

    def it_should_do_this_test(self):
        assert 1 == 1

def test_we_still_run_regular_pytest_scripts():
    assert 2 == 2
