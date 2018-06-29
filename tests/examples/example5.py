import contexts

@contexts.spec
class Anything:

    @contexts.action
    def thing(self):
        self.done = True

    @contexts.assertion
    def other_thing(self):
        assert self.done
