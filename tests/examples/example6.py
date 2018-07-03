given_calls = []
when_calls = []

class When_we_have_a_test:

    def given_a_setup_method(self):
        given_calls.append(1)

    def when_things_happen(self):
        when_calls.append(1)

    def it_should_see_the_givens_run_once_from_the_first_assert(self):
        assert sum(given_calls) == 1

    def it_should_also_see_the_givens_run_once_in_the_second(self):
        assert sum(given_calls) == 1

