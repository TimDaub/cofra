# These tests simulate the cache with a 1 and 4 second 
# TTL, which means that they can take up to 10 seconds to run.
# Therefore they are excluded from all other tests

from emotext.models.persistence import MessageCluster
from emotext.models.models import Message
from time import sleep

TEXTS = [
    "Hello. This isn't doge!",
    "Such wow, many pythons!"
]

MESSAGES = [
    Message(entity_name="Testname", text=TEXTS[0]),
    Message(entity_name="OtherTestname", text=TEXTS[1])
]

TOLERANCE_TIME = 1


def test_mc_reset_db():
    """
    Tries to reset the MessageCluster's database.
    """
    mc = MessageCluster()
    mc.reset_db()
    assert len(mc.db.keys()) == 0

def test_mc_add_message():
    """
    Adds multiple messages to the message cluster.
    """
    mc = MessageCluster(TOLERANCE_TIME+3) # 4
    # init message should create a list and start the tolerance counter
    mc.add_message(MESSAGES[0])
    sleep(1)
    # the next message should reset the tolerance counter
    mc.add_message(MESSAGES[1])
    # if it doesn't, conversation should be over after sleep(3)
    sleep(3)
    res = mc.is_conversation_over()
    assert res == False
    sleep(1)
    res = mc.is_conversation_over()
    assert res

def test_mc_counter():
    """
    Initializing a MessageCluster with a custom time.
    """

    mc = MessageCluster(TOLERANCE_TIME)
    mc.start_tolerance()
    sleep(TOLERANCE_TIME+1)

    res = mc.is_conversation_over()
    assert res