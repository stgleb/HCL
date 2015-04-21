from models import *
from datetime import datetime

with db_session:
    # Creating objects
    c1 = Component(name="Intel C204 PCH", vendor="Intel", type="Chipset", comments="nothing")
    c2 = Component(name="Intel C602", vendor="Intel", type="Chipset", comments="nothing")
    c3 = Component(name="LSI 2108 SAS2 (6Gbps) w/ Hardware RAID support (BPN-ADP-SAS2-H6iR)",
                   vendor="Intel", type="RAID", comments="nothing")
    c4 = Component(name="Intel 82580",
                   vendor="Intel", type="NIC", comments="nothing")

    cert1 = Certification(fuel_version="Fuel 5.0", date=datetime.now())
    cert2 = Certification(fuel_version="Fuel 6.0", date=datetime.now())
    cert3 = Certification(fuel_version="Fuel 5.1", date=datetime.now())
    cert4 = Certification(fuel_version="Fuel 6.1", date=datetime.now())
    cert5 = Certification(fuel_version="Fuel 4.1", date=datetime.now())

    s1 = Server(name="SuperMicro SuperServer 6027TR-H71RF+", vendor="Supermicro",
                specification_url="http://www.supermicro.com/products/system/3U/5037/SYS-5037MR-H8TRF.cfm")
    s2 = Server(name="SuperMicro SuperServer 6027TR-H71RF+", vendor="Supermicro",
                specification_url="http://www.supermicro.com/products/system/2U/6027/SYS-6027TR-H71RF_.cfm")
    s3 = Server(name="Dell PowerEdge R630", vendor="Dell",
                specification_url="http://www.dell.com/rs/business/p/poweredge-r620/pd")

    #establishing a connections
    s1.certifications.add(cert1)
    s1.certifications.add(cert2)
    cert1.server = s1
    cert2.server = s1

    s2.certifications.add(cert4)
    s2.certifications.add(cert5)

    cert4.server = s2
    cert5.server = s2

    s1.components.add(c1)
    s1.components.add(c3)

    c1.servers.add(s1)
    c3.servers.add(s1)

    s3.components.add(c4)
    c4.servers.add(s3)

    s2.components.add(c1)
    c1.servers.add(s2)

    s2.components.add(c3)
    c3.servers.add(s2)