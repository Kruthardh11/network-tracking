import socket
import dpkt
import pygeoip

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def main():
    with open('wire.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        kmlheader = '''<?xml version="1.0" encoding="UTF-8"?> 
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<Style id="transBluePoly">
    <LineStyle>
        <width>1.5</width>
        <color>501400E6</color>
    </LineStyle>
</Style>'''

        kmlfooter = '</Document>\n</kml>\n'
        kmldoc = kmlheader + plotIPs(pcap) + kmlfooter

        # Save to a file
        with open("output.kml", "w") as kml_file:
            kml_file.write(kmldoc)
        
        print("KML file has been saved as output.kml")

def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src)
            kmlPts += KML
        except:
            pass
    return kmlPts

def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('202.53.64.156')
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = f'''
        <Placemark>
            <name>{dstip}</name>
            <extrude>1</extrude>
            <tessellate>1</tessellate>
            <styleUrl>#transBluePoly</styleUrl>
            <LineString>
                <coordinates>{dstlongitude},{dstlatitude} {srclongitude},{srclatitude}</coordinates>
            </LineString>
        </Placemark>
        '''
        return kml
    except:
        return ''
    
if __name__ == '__main__':
    main()
