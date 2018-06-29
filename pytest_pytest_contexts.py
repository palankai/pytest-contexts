import inspect
import pytest
from contexts.core import (
    NO_EXAMPLE,
    Context,
    PluginComposite,
    TestClass,
    run_with_test_data,
)
from contexts.plugins.identification import NameBasedIdentifier
from contexts.plugins.identification.decorators import DecoratorBasedIdentifier

def pytest_pycollect_makeitem(collector, name, obj):
    if not inspect.isclass(obj):
        return
    if NameBasedIdentifier().identify_class(obj):
        return ContextsCollector(name, obj=obj, parent=collector)


class ContextsCollector(pytest.Collector):

    def __init__(self, name, obj, parent):
        self.name = name
        self.obj = obj
        super().__init__(self.name, parent=parent)

    def reportinfo(self):
        path = inspect.getfile(self.obj)
        return self.name, 0, f'{path}.{self.name}'

    def collect(self):
        plugins = PluginComposite([DecoratorBasedIdentifier(), NameBasedIdentifier()])
        context_class = TestClass(self.obj, plugins)
        for example in context_class.get_examples():
            context = Context(
                context_class.cls(),
                example,
                context_class.unbound_setups,
                context_class.unbound_action,
                context_class.unbound_assertions,
                context_class.unbound_teardowns,
                context_class.plugin_composite,
            )
            for assertion in context.assertions:
                item_name = f'{self.name}.{assertion}'
                if example != NO_EXAMPLE:
                    item_name += f' (example={example})'
                yield ContextsItem(item_name, context, assertion, self.obj, self.parent)



class ContextsItem(pytest.Item):

    def __init__(self, name, context, assertion, obj, parent):
        self.name = name
        self.context = context
        self.assertion = assertion
        self.obj = obj
        super().__init__(name, parent=parent)

    def reportinfo(self):
        path = inspect.getfile(self.obj)
        return self.name, 0, f'{path}:{self.name}'

    def setup(self):
        self.context.run_setup()
        self.context.run_action()

    def runtest(self):
        run_with_test_data(self.assertion.func, self.context.example)

    def teardown(self):
        self.context.run_teardown()
