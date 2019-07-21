from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter

logger = logging.getLogger(__name__)


def run_restaurant_bot():
    interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
    agent = Agent.load('./models/dialogue', interpreter=interpreter)

    agent.handle_channel(ConsoleInputChannel())

    return agent


if __name__ == '__main__':
    run_restaurant_bot()
