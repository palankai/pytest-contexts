class When_we_have_a_test:

    def given_a_setup_method(self):
        self.given_run = True

    def when_things_happen(self):
        self.when_run = True

    def it_should_run_one_method(self):
        assert 1 == 1
        assert self.given_run is True
        assert self.when_run is True

