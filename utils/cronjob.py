import sched
import time
from controllers.sql import PersonCtrl

def start_cron(num_of_secs):
    """
    In the cofra database, tables can have a column called decay.
    This cronjob that is executed every hour guarantees that every row that is
    affected - meaning 'decay'(date) < 'now'(date) will simply be deleted.
    """
    s = sched.scheduler(time.time, time.sleep) 
    s.enter(num_of_secs, 1, delete_decayed, (s, num_of_secs,))
    s.run()

def delete_decayed(sc, num_of_secs): 
    """
    Triggers the deletion of all decayed tables and renters loop afterwards.
    """
    # Trigger database functionality
    print 'Deleted the following decayed rows: '
    dbctrl = PersonCtrl()
    dbctrl.delete_decayed_rows()
    dbctrl.close()
    # rerun timer
    sc.enter(num_of_secs, 1, delete_decayed, (sc, num_of_secs))