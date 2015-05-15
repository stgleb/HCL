import shlex
import subprocess
import re
import xml.etree.ElementTree as ET
import utils
import yaml

def get_data(rr, data):
    match_res = re.search("(?ims)" + rr, data)
    return match_res.group(0)


class HWInfo(object):
    def __init__(self):
        self.hostname = None
        self.cores = []

        # /dev/... devices
        self.disks_info = {}

        # real disks on raid controller
        self.disks_raw_info = {}

        self.net_info = {}
        self.ram_size = 0
        self.sys_name = None
        self.mb = None
        self.raw = None
        self.storage_controllers = []

    def get_summary(self):
        cores = sum(count for _, count in self.cores)
        disks = sum(size for _, size in self.disks_info.values())

        return {'cores': cores, 'ram': self.ram_size, 'storage': disks}

    def __str__(self):
        res = []

        summ = self.get_summary()
        summary = "Summary: {cores} cores, {ram}B RAM, {disk}B storage"
        res.append(summary.format(cores=summ['cores'],
                                  ram=utils.b2ssize(summ['ram']),
                                  disk=utils.b2ssize(summ['storage'])))
        res.append(str(self.sys_name))
        if self.mb is not None:
            res.append("Motherboard: " + self.mb)

        if self.ram_size == 0:
            res.append("RAM: Failed to get RAM size")
        else:
            res.append("RAM " + utils.b2ssize(self.ram_size) + "B")

        if self.cores == []:
            res.append("CPU cores: Failed to get CPU info")
        else:
            res.append("CPU cores:")
            for name, count in self.cores:
                if count > 1:
                    res.append("    {0} * {1}".format(count, name))
                else:
                    res.append("    " + name)

        if self.storage_controllers != []:
            res.append("Disk controllers:")
            for descr in self.storage_controllers:
                res.append("    " + descr)

        if self.disks_info != {}:
            res.append("Storage devices:")
            for dev, (model, size) in sorted(self.disks_info.items()):
                ssize = utils.b2ssize(size) + "B"
                res.append("    {0} {1} {2}".format(dev, ssize, model))
        else:
            res.append("Storage devices's: Failed to get info")

        if self.disks_raw_info != {}:
            res.append("Disks devices:")
            for dev, descr in sorted(self.disks_raw_info.items()):
                res.append("    {0} {1}".format(dev, descr))
        else:
            res.append("Disks devices's: Failed to get info")

        if self.net_info != {}:
            res.append("Net adapters:")
            for name, (speed, dtype) in self.net_info.items():
                res.append("    {0} {2} duplex={1}".format(name, dtype, speed))
        else:
            res.append("Net adapters: Failed to get net info")

        return str(self.hostname) + ":\n" + "\n".join("    " + i for i in res)


def get_hw_info(conn):
    res = HWInfo()

    controller_id = '13'
    process = subprocess.Popen(shlex.split("ssh node-{0} lshw -xml".format(controller_id)), stdout=subprocess.PIPE)
    raw = process.communicate()[0].strip()
    lshw_out = ' '.join(raw.split('\\n'))
    res.raw = lshw_out
    lshw_et = ET.fromstring(lshw_out)

    try:
        res.hostname = lshw_et.find("node").attrib['id']
    except:
        pass

    try:
        res.sys_name = (lshw_et.find("node/vendor").text + " " +
                        lshw_et.find("node/product").text)
        res.sys_name = res.sys_name.replace("(To be fillesudd by O.E.M.)", "")
        res.sys_name = res.sys_name.replace("(To be Filled by O.E.M.)", "")
    except:
        pass

    nodes = lshw_et.findall("node/node")

    for node in nodes:
        if node.attrib.get('id') == 'core':
            core = node
            break
    else:
        core = None

    # core = lshw_et.find("node/node[@id='core']")
    if core is None:
        return

    try:
        res.mb = " ".join(core.find(node).text
                          for node in ['vendor', 'product', 'version'])
    except:
        pass

    for cpu in core.findall("node[@class='processor']"):
        try:
            model = cpu.find('product').text
            threads_node = cpu.find("configuration/setting[@id='threads']")
            if threads_node is None:
                threads = 1
            else:
                threads = int(threads_node.attrib['value'])
            res.cores.append((model, threads))
        except:
            pass

    res.ram_size = 0
    for mem_node in core.findall(".//node[@class='memory']"):
        descr = mem_node.find('description')
        try:
            if descr is not None and descr.text == 'System Memory':
                mem_sz = mem_node.find('size')
                if mem_sz is None:
                    for slot_node in mem_node.find("node[@class='memory']"):
                        slot_sz = slot_node.find('size')
                        if slot_sz is not None:
                            assert slot_sz.attrib['units'] == 'bytes'
                            res.ram_size += int(slot_sz.text)
                else:
                    assert mem_sz.attrib['units'] == 'bytes'
                    res.ram_size += int(mem_sz.text)
        except:
            pass

    for net in core.findall(".//node[@class='network']"):
        try:
            link = net.find("configuration/setting[@id='link']")
            if link.attrib['value'] == 'yes':
                name = net.find("logicalname").text
                speed_node = net.find("configuration/setting[@id='speed']")

                if speed_node is None:
                    speed = None
                else:
                    speed = speed_node.attrib['value']

                dup_node = net.find("configuration/setting[@id='duplex']")
                if dup_node is None:
                    dup = None
                else:
                    dup = dup_node.attrib['value']

                res.net_info[name] = (speed, dup)
        except:
            pass

    for controller in core.findall(".//node[@class='storage']"):
        try:
            description = getattr(controller.find("description"), 'text', "")
            product = getattr(controller.find("product"), 'text', "")
            vendor = getattr(controller.find("vendor"), 'text', "")
            dev = getattr(controller.find("logicalname"), 'text', "")
            if dev != "":
                res.storage_controllers.append(
                    "{0}: {1} | {2} | {3}".format(dev, description,
                                              vendor, product))
            else:
                res.storage_controllers.append(
                    "{0} | {1} | {2}".format(description,
                                         vendor, product))
        except:
            pass

    for disk in core.findall(".//node[@class='disk']"):
        try:
            lname_node = disk.find('logicalname')
            if lname_node is not None:
                dev = lname_node.text.split('/')[-1]

                if dev == "" or dev[-1].isdigit():
                    continue

                sz_node = disk.find('size')
                assert sz_node.attrib['units'] == 'bytes'
                sz = int(sz_node.text)
                res.disks_info[dev] = ('', sz)
            else:
                description = disk.find('description').text
                product = disk.find('product').text
                vendor = disk.find('vendor').text
                version = disk.find('version').text
                serial = disk.find('serial').text

                full_descr = "{0} {1} {2} {3} {4}".format(
                    description, product, vendor, version, serial)

                businfo = disk.find('businfo').text
                res.disks_raw_info[businfo] = full_descr
        except:
            pass

    return res


def get_yaml():
    hw = get_hw_info(0)
    from datetime import datetime
    yaml_dict = {"components": [], "certification" :
        {"date": datetime.now(), "fuel_version": ""}}

    with open('/etc/fuel/version.yaml') as f:
        versions = yaml.load(f)

    yaml_dict['certification']['fuel_version'] = 'fuel ' + versions['VERSION']['release']
    yaml_dict['server_name'] = hw.sys_name

    if hw.storage_controllers != []:
            for descr in hw.storage_controllers:

                lst = descr.split(':')
                if len(lst) == 2:
                    description, vendor, product = lst[1].split('|')
                else:
                    description, vendor, product = lst[0].split('|')
                yaml_dict['components'].append({"name": product,
                                                "type": description, "vendor": vendor})

    for name, _ in hw.net_info.items():
                yaml_dict['components'].append({"name": name, "type": "nic", "vendor": ""})

    return yaml.dump(yaml_dict, default_flow_style=False)


if __name__ == '__main__':
   print get_yaml()