from flask import Flask, render_template, Response
from fulkod import arbs
import re

# begin IPv4 hack
#--------------------
# do this once at program startup
#--------------------
import socket
origGetAddrInfo = socket.getaddrinfo

def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
    return origGetAddrInfo(host, port, socket.AF_INET, socktype, proto, flags)

# replace the original socket.getaddrinfo by our version
socket.getaddrinfo = getAddrInfoWrapper
# END IPv4 hack

app = Flask(__name__)

re_ids = re.compile('(\w{2}\-\d\-\d{3})(_\d)?')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:cal_ids>')
def get_cal(cal_ids):
    cal = arbs.Fulcalendar()
    resp=""
    for c_id, g_id in re_ids.findall(cal_ids):
        if '' == g_id:
            g_id = 0
        else:
            g_id = int(re.sub('\D', '', g_id))
        resp = "%s\n%s-%s"%(resp, c_id, g_id)
        cal.addCourse(c_id,g_id)
    return Response(cal.getCal().to_ical(), mimetype="text/calendar")


if __name__ == '__main__':
#    app.run()
    app.debug = True

    app.run(host='0.0.0.0', port=8000)

