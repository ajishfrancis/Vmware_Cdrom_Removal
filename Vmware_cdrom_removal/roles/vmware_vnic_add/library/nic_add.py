#!/usr/bin/env python
import atexit
import requests
#from serials import tools
#from serials.tools import cli
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
from tools import tasks
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text, to_native
from ansible.module_utils.vmware import (find_obj, gather_vm_facts, get_all_objs, compile_folder_path_for_object, serialize_spec,vmware_argument_spec, set_vm_power_state, PyVmomi)

# disable  urllib3 warnings
if hasattr(requests.packages.urllib3, 'disable_warnings'):
    requests.packages.urllib3.disable_warnings()


def add_nic(si, vm, network):
    
    spec = vim.vm.ConfigSpec()
    nic_changes = []

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

    nic_spec.device = vim.vm.device.VirtualE1000()

    nic_spec.device.deviceInfo = vim.Description()
    nic_spec.device.deviceInfo.summary = 'vCenter API test'

    nic_spec.device.backing = \
        vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nic_spec.device.backing.useAutoDetect = False
    content = si.RetrieveContent()
    nic_spec.device.backing.network = get_obj(content, [vim.Network], network)
    nic_spec.device.backing.deviceName = network

    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.allowGuestControl = True
    nic_spec.device.connectable.connected = False
    nic_spec.device.connectable.status = 'untried'
    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = 'assigned'

    nic_changes.append(nic_spec)
    spec.deviceChange = nic_changes
    e = vm.ReconfigVM_Task(spec=spec)
    return True


def get_args():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(hostname=dict(type='str', required=True),
                              username=dict(type='str', required=True),
                              password=dict(type='str', required=True),
                              port=dict(type='int', default='443'),
                              port_group=dict(type='str'),
                              name=dict(type='str', required=True),
                              uuid=dict(type='str', required=True),
                              nic_state=dict(type='str'),
                              nic_number=dict(type='str')))
    module = AnsibleModule(argument_spec=argument_spec)
    return module


def get_obj(content, vim_type, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vim_type, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def main():
    args = get_args()

    # connect to vc
    si = SmartConnect(
        host=args.params['hostname'],
        user=args.params['username'],
        pwd=args.params['password'],
#        port_group=args.params['port_group'],
        port=args.params['port'])
    # disconnect vc
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    print ('Searching for VM {}').format(args.params['name'])
    vm_obj = get_obj(content, [vim.VirtualMachine], args.params['name'])

    if vm_obj:
        result = add_nic(si, vm_obj, args.params['port_group'])
        msg = ('VM NIC SUccessfully Added')
        args.exit_json(msg=msg ,changed=False)
    else:
        msg = ("VM not found")
        args.fail_json(msg=msg)
# start
if __name__ == "__main__":
    main()
