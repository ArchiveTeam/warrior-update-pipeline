import datetime

import functools

from seesaw.externalprocess import ExternalProcess
from seesaw.pipeline import Pipeline
from seesaw.project import Project
from seesaw.task import Task, LimitConcurrent
from tornado.ioloop import IOLoop

project = Project(
    title='Software Update',
    project_html='''
        <h2>Software Update</h2>
        <p>Select this project, when required, to automatically
        download and install software to update components of the Warrior.
        </p>
        <p>Components: Python3.5 </p>
        '''
)


class WarningTask(Task):
    def __init__(self):
        Task.__init__(self, 'WarningTask')

    def enqueue(self, item):
        self.start_item(item)
        item.may_be_canceled = True
        item.log_output('Software will be automatically downloaded and installed to update components of the Warrior.')
        item.log_output('Update will continue in 10 seconds...')

        IOLoop.instance().add_timeout(
            datetime.timedelta(seconds=10),
            functools.partial(self._finish, item)
        )

    def _finish(self, item):
        item.may_be_canceled = True
        self.complete_item(item)


class IdleTask(Task):
    def __init__(self):
        Task.__init__(self, 'IdleTask')

    def enqueue(self, item):
        self.start_item(item)
        item.may_be_canceled = True
        item.log_output('Pausing for 60 seconds...')

        IOLoop.instance().add_timeout(
            datetime.timedelta(seconds=60),
            functools.partial(self._finish, item)
        )

    def _finish(self, item):
        item.may_be_canceled = True
        self.complete_item(item)


pipeline = Pipeline(
    WarningTask(),
    LimitConcurrent(1, ExternalProcess('Install Python 3.5', ['install-python3.5.sh'])),
    IdleTask(),
)
