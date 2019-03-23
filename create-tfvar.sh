echo -e  'data_resource_group="'$ResourceGroupName'"\n'\
	 'data_vnet="'$VnetName'"\n'\
        'data_subnet="'$SubnetName'"\n'\
        'image_publisher="'$ImagePublisher'"\n'\
        'image_offer="'$ImageOffer'"\n'\
        'image_sku="'$ImageSku'"\n'\
        'vm_size="'$VmSize'"\n'\
        'vm_name="'$VmName'"\n'\
        'managed_disk_size="'$ManagedDiskSize'"\n'\
        'subscription_id="'$SubscriptionId'"\n'\
        'business_owner_tag="'$BusinessOwner'"\n'\
        'technical_owner_tag="'$TechnicalOwner'"\n'\
        'cost_code_tag="'$CostCode'"\n'\
        'schedule_type_tag="'$ScheduleType'"\n'\
        'project_tag="'$Project'"\n'\
	'infrastructure_change_id_tag="'$CrNumber'"\n'> variables.tfvars
        

 
echo $CrNumber > cr.txt
