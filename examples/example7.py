asserts = []

class When_we_have_a_test:

    def it_should_run_one_test(self):
        asserts.append(1)

    def it_should_run_the_other_one_too(self):
        asserts.append(1)

    def cleanup(self):
        assert sum(asserts) == 2
