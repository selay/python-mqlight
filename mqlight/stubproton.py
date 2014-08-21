from mqlightlog import get_logger, NO_CLIENT_ID
import mqlightexceptions as mqlexc

LOG = get_logger(__name__)


class _MQLightMessage(object):

    """
    Wrapper for the Proton Message class
    """

    def __init__(self, message=None):
        """
        MQLight Message constructor
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage.constructor called')

    def _set_tracker(self, tracker):
        """
        Sets the tracker
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage._set_tracker called')

    def _get_tracker(self):
        """
        Returns the tracker
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage._get_tracker called')
        return None

    tracker = property(_get_tracker, _set_tracker)

    def _set_link_address(self, link_address):
        """
        Sets the link address
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage._set_link_address called')

    def _get_link_address(self):
        """
        Returns the link address
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage._get_link_address called')
        return None

    link_address = property(_get_link_address, _set_link_address)

    def _set_time_to_live(self, ttl):
        """
        Sets the ttl
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage._set_time_to_live called')

    def _get_time_to_live(self):
        """
        Returns the ttl
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage._get_time_to_live called')
        return None

    ttl = property(_get_time_to_live, _set_time_to_live)

    def _get_message(self):
        """
        Returns the Proton Message object
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessage._get_message called')
        return None

    message = property(_get_message)


class _MQLightMessenger(object):

    """
    Wrapper for the Proton Messenger class
    """

    def __init__(self, name, username=None, password=None):
        """
        MQLightMessenger constructor
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.constructor called')
        self.connect_status = 0
        self._stopped = True
        self.stop_count = 2
        self.send_status = 7
        self.remote_idle_timeout = -1
        self.work_callback = None

    def connect(self, service, ssl_trust_certificate, ssl_verify_name):
        """
        Connects to the specified service
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.connect called')
        if not self.stopped:
            raise mqlexc.MQLightError('already connected')
        if 'bad' in service.netloc:
            raise TypeError('bad service ' + service.netloc)
        if ssl_trust_certificate == 'BadCertificate':
            raise mqlexc.SecurityError('Bad certificate')
        elif ssl_trust_certificate == 'BadVerify' and ssl_verify_name:
            raise mqlexc.SecurityError('Bad verify name')
        else:
            if self.connect_status != 0:
                raise mqlexc.NetworkError(
                    'connect error: ' + self.connect_status)
            else:
                self.stopped = False
                LOG.data(NO_CLIENT_ID, 'successfully connected')

    def stop(self):
        """
        Calls stop() on the proton Messenger
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.stop called')
        if not self.stopped:
            self.stop_count -= 1
            if self.stop_count == 0:
                self.stopped = True
                self.stop_count = 2
        return self.stopped

    def _is_stopped(self):
        """
        Returns True
        """
        return True

    def _set_stopped(self, state):
        """
        Set the state
        """
        self._stopped = state
    stopped = property(_is_stopped, _set_stopped)

    def has_sent(self):
        """
        Returns True
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.has_sent called')
        return True

    def block_send_completion(self):
        """
        Temporarily blocks message sends from completing by forcing the status
        to return as PN_STATUS_PENDING.
        """
        LOG.data(
            NO_CLIENT_ID,
            '_MQLightMessenger.block_send_completion called')
        self.send_status = 1

    def unblock_send_completion(self):
        """
        Removes a block on message sends by forcing the status to
        PN_STATUS_SETTLED.
        """
        LOG.data(
            NO_CLIENT_ID,
            '_MQLightMessenger.unblock_send_completion called')
        self.send_status = 7

    def set_connect_status(self, status):
        """
        Override the proton connection status.
        """
        self.connect_status = status

    def status_error(self, message):
        """
        Finds the reason why the message has been rejected
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.status_error called')
        return ''

    def get_remote_idle_timeout(self, address):
        """
        Returns the idle timeout of the Messenger
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.get_remote_idle_timeout called')
        return self.remote_idle_timeout

    def set_remote_idle_timeout(self, interval, callback):
        """
        Sets a remoteIdleTimeout value to return.
        """
        LOG.data(
            NO_CLIENT_ID,
            '_MQLightMessenger.set_remote_idle_timeout called')
        self.remote_idle_timeout = interval
        self.work_callback = callback

    def work(self, timeout):
        """
        Sends or receives any outstanding messages
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.work called')
        if self.work_callback:
            self.work_callback()
        return 0

    def flow(self, address, credit):
        """
        Process messages based on the number of credit available
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.flow called')

    def put(self, msg, qos):
        """
        Puts a message on the outgoing queue
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.put called')
        return True

    def send(self):
        """
        Sends the messages on the outgoing queue
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.send called', )

    def receive(self, timeout):
        """
        Retrieves messages from the incoming queue
        """
        return []

    def settle(self, message):
        """
        Settles a message
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.settle called')
        return True

    def accept(self, message):
        """
        Accepts a message
        """
        LOG.data(NO_CLIENT_ID, '_MQLightMessenger.accept called')

    def status(self, message):
        """
        Get the status of a message
        """
        LOG.data(
            NO_CLIENT_ID,
            '_MQLightMessenger.status called',
            self.send_status)
        return self.send_status

    def subscribe(self, address, qos, ttl, credit):
        """
        Subscribes to a topic
        """
        return True

    def unsubscribe(self, address, ttl):
        """
        Unsubscribes from a topic
        """
        return True