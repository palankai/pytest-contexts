class When_we_have_a_test:
    @classmethod
    def examples(cls):
        yield 1
        yield 3

    def when_things_happen(self):
        pass

    def it_should_do_this_test(self, arg):
        assert arg < 3
