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
    print('colllecting', name, obj)
    if not inspect.isclass(obj):
        return
    if not name.lower().startswith('when'):
        return
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
            item_name = self.name if example is NO_EXAMPLE else f'{self.name} (example={example})'
            yield ContextsItem(item_name, context, self.obj, self.parent)



class ContextsItem(pytest.Item):

    def __init__(self, name, context, obj, parent):
        self.context = context
        self.name = name
        self.obj = obj
        super().__init__(name, parent=parent)

    def reportinfo(self):
        path = inspect.getfile(self.obj)
        return self.name, 0, f'{path}.{self.name}'

    def setup(self):
        self.context.run_setup()
        self.context.run_action()

    def runtest(self):
        # self.context.run_assertions()  #  this is swallowing exceptions by default
        for assertion in self.context.assertions:
            run_with_test_data(assertion.func, self.context.example)

    def teardown(self):
        self.context.run_teardown()
