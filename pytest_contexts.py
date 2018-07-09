import inspect
import pathlib
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

PLUGINS = PluginComposite([DecoratorBasedIdentifier(), NameBasedIdentifier()])

def pytest_pycollect_makeitem(collector, name, obj):
    if not inspect.isclass(obj):
        return
    if PLUGINS.identify_class(obj):
        return ContextsCollector(name, obj=obj, parent=collector)


class ContextsCollector(pytest.Collector):

    def __init__(self, name, obj, parent):
        self.name = name
        self.obj = obj
        self.path = inspect.getfile(self.obj)
        super().__init__(self.name, parent=parent)

    def reportinfo(self):
        return self.name, 0, f'{self.path}.{self.name}'

    def collect(self):
        context_class = TestClass(self.obj, PLUGINS)
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
                item_name = f'{self.name}.{assertion.name}'
                if example != NO_EXAMPLE:
                    item_name += f' (example={example})'
                yield ContextsItem(item_name, context, assertion, self.path, self.parent)



class ContextsItem(pytest.Item):

    def __init__(self, name, context, assertion, path, parent):
        self.name = name
        self.context = context
        self.assertion = assertion
        self.path = path
        super().__init__(name, parent=parent)
        self.context.assertions_run = 0

    def reportinfo(self):
        return self.name, 0, f'{self.path}:{self.name}'

    def setup(self):
        if self.context.assertions_run > 0:
            return
        self.context.run_setup()
        self.context.run_action()

    def runtest(self):
        self.context.assertions_run += 1
        run_with_test_data(self.assertion.func, self.context.example)

    def teardown(self):
        if self.context.assertions_run < len(self.context.assertions):
            return
        self.context.run_teardown()

    def _prunetraceback(self, excinfo):
        super()._prunetraceback(excinfo)
        excinfo.traceback = excinfo.traceback.filter()
        this_filename = pathlib.Path(__file__).name
        excinfo.traceback = excinfo.traceback.filter(
            lambda t: this_filename not in str(t.path)
        )
        excinfo.traceback = excinfo.traceback.filter(
            lambda t: '/_pytest' not in str(t.path)
        )
        excinfo.traceback = excinfo.traceback.filter(
            lambda t: '/pluggy/' not in str(t.path)
        )
