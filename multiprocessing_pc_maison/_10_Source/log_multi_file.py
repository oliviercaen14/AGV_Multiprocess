#https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
# You'll need these imports in your own code
import logging
import logging.handlers


# Next two import lines for this demo only

# The worker configuration is done at the start of the worker process run.
# Note that on Windows you can't rely on fork semantics, so each process
# will run the logging configuration code when it starts.
def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.DEBUG)

