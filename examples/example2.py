class IgnoreMe:
    def given_nothing(self):
        pass

    def it_should_not_see_this_class(self):
        assert 'should not see this'


class When_we_have_a_test:

    def given_a_setup_method(self):
        self.given_run = True

    def when_things_happen(self):
        self.when_run = True

    def it_should_run_one_method(self):
        assert 1 == 1
        assert self.given_run is True
        assert self.when_run is True

    def it_should_run_the_other_one_too_and_see_it_fail(self):
        assert self.given_run is True
        assert self.when_run is True
        assert 1 == 2
