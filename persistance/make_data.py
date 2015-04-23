from models import *
from datetime import datetime


with db_session:
    # Creating objects
    driver1 = Driver(name="aaa", version="0.0")
    driver2 = Driver(name="bb", version="0.1")
    driver3 = Driver(name="ccc", version="1.0")

    type1 = Type(name="nic")
    type2 = Type(name="raid")
    type3 = Type(name="chipset")
    type4 = Type(name="motherboard")
    type5 = Type(name="cpu")

    c1 = Component(name="Intel C204 PCH", vendor="Intel",
                   type="Chipset", comments="nothing",
                   driver=driver3)
    c2 = Component(name="Intel C602", vendor="Intel",
                   type="Chipset", comments="nothing",
                   driver=driver2)
    c3 = Component(name="LSI 2108 SAS2 (6Gbps) w/ "
                        "Hardware RAID support (BPN-ADP-SAS2-H6iR)",
                   vendor="Intel", type="RAID", comments="nothing",
                   driver=driver1)
    c4 = Component(name="Intel 82580", vendor="Intel",
                   type="NIC", comments="nothing", driver=driver1)

    c1.driver = driver1
    c2.driver = driver2
    c3.driver = driver3
    c4.driver = driver1

    fv1 = FuelVersion(name="Fuel 4.1")
    fv2 = FuelVersion(name="Fuel 5.0")
    fv3 = FuelVersion(name="Fuel 5.1")
    fv4 = FuelVersion(name="Fuel 6.0")
    fv5 = FuelVersion(name="Fuel 6.1")

    fv1.drivers.add(driver1)
    fv2.drivers.add(driver2)
    fv3.drivers.add(driver3)

    s1 = Server(name="SuperMicro SuperServer 6027TR-H71RF+", vendor="Supermicro",
                specification_url="http://www.supermicro.com/products/system/3U/5037/SYS-5037MR-H8TRF.cfm")
    s2 = Server(name="SuperMicro Super mega server", vendor="Supermicro",
                specification_url="http://www.supermicro.com/products/system/2U/6027/SYS-6027TR-H71RF_.cfm")
    s3 = Server(name="Dell PowerEdge R630", vendor="Dell",
                specification_url="http://www.dell.com/rs/business/p/poweredge-r620/pd")

    s4 = Server(name="Cisco UCS-C Series Blade Server", vendor="Cisco")

    s5 = Server(name="Huawei RH2288", vendor="Huawei")

    s6 = Server(name="Lenovo RD530", vendor="Lenovo",
                specification_url="http://shop.lenovo.com/us/en/servers/thinkserver/racks/rd530/#tab-tech_specs")

    s7 = Server(name="Some server which is not certified", vendor="Lenovo",
                specification_url="http://shop.lenovo.com/us/en/servers/thinkserver/racks/rd530/#tab-tech_specs")

    cert1 = Certification(server=s1, fuel_version=fv1, date=datetime.now())
    cert2 = Certification(server=s1, fuel_version=fv2, date=datetime.now())
    cert3 = Certification(server=s3, fuel_version=fv3, date=datetime.now())
    cert4 = Certification(server=s2, fuel_version=fv5, date=datetime.now())
    cert5 = Certification(server=s2, fuel_version=fv1, date=datetime.now())
    cert6 = Certification(server=s4, fuel_version=fv1, date=datetime.now())
    cert7 = Certification(server=s5, fuel_version=fv5, date=datetime.now())
    cert8 = Certification(server=s6, fuel_version=fv3, date=datetime.now())
    cert9 = Certification(server=s6, fuel_version=fv4, date=datetime.now())
    #establishing a connections
    s1.certifications.add(cert1)
    s1.certifications.add(cert2)
    s2.certifications.add(cert4)
    s2.certifications.add(cert5)
    s3.certifications.add(cert3)
    s4.certifications.add(cert6)
    s5.certifications.add(cert7)
    s6.certifications.add(cert8)
    s6.certifications.add(cert9)

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