given_calls = []
when_calls = []

class When_we_have_a_test:

    def given_a_setup_method(self):
        given_calls.append(1)

    def when_things_happen(self):
        when_calls.append(1)

    def it_should_run_one_method(self):
        assert sum(given_calls) == 1

    def it_should_run_the_other_one_too_and_see_it_fail(self):
        assert sum(given_calls) == 1

