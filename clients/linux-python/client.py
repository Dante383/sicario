#!/usr/bin/env python
 
import sys, time, os
from daemon import Daemon
import sicario
 
class SicarioDaemon(Daemon):
        interval = 60

        def read_config (self):
                if not os.path.isdir('/etc/sicario') or not os.path.exists('/etc/sicario/sicario.conf'):
                        self.stop()

                with open('/etc/sicario/sicario.conf') as f:
                        config_bare = f.readline()

                self.config = config_bare.split(',')

                if len(self.config) < 2 or len(self.config) > 4:
                        self.stop()

                if len(self.config) == 4:
                        self.interval = int(self.config[3])

        def run(self):
                while True:
                        self.read_config()
                        sicario.Sicario(self, self.config)
                        time.sleep(self.interval)

if __name__ == "__main__":
        daemon = SicarioDaemon('/tmp/daemon-sicario.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)