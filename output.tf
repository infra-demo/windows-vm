# output "Public_IP"{
# value = "${azurerm_public_ip.eip.ip_address}"
# }

output "Private_IP"{
 value = "${azurerm_network_interface.networkinterface.private_ip_address}"
}

output "VM_Name"{
value = "${azurerm_virtual_machine.vm.name}"
}

output "OS_Name"{
value = "${azurerm_virtual_machine.vm.storage_os_disk.0.os_type}"
}

output "Technical_Owner"{
value = "${azurerm_virtual_machine.vm.tags.Technical-Owner}"
}

output "Project"{
value = "${azurerm_virtual_machine.vm.tags.Project}"
}

output "Cost_Code"{
value = "${azurerm_virtual_machine.vm.tags.Cost-Code}"
}


output "Schedule_Type"{
value = "${azurerm_virtual_machine.vm.tags.Schedule-Type}"
}

output "Business_Owner"{
value = "${azurerm_virtual_machine.vm.tags.Business-Owner}"
}

output "Infrastructure_Change_Req_ID"{
value = "${azurerm_virtual_machine.vm.tags.Infrastructure-Change-Req-ID}" 
}

output "VM_Size"{
value = "${azurerm_virtual_machine.vm.vm_size}"
}

output "VM_ID"{
value = "${azurerm_virtual_machine.vm.id}"
}

output "VM_Location"{
value = "${azurerm_virtual_machine.vm.location}"
}

output "Resource_Group_Name"{
value = "${data.azurerm_virtual_network.vnet.resource_group_name}"
}

output "VNet"{
value = "${data.azurerm_virtual_network.vnet.name}"
}

output "Subnet"{
value = "${data.azurerm_virtual_network.vnet.subnets.0}"
}

output "Storage_Disk_Size"{
value = "${azurerm_virtual_machine.vm.storage_os_disk.0.disk_size_gb}"
}

output "OS_Disk_Size" {
value = "${azurerm_virtual_machine.vm.storage_data_disk.0.disk_size_gb}"
}
