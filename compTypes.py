import json
import requests


metadataTypes = {
"applications":"CustomApplication",
"approvalProcesses":"ApprovalProcess",
"audience":"Audience",
"aura":"AuraDefinitionBundle",
"brandingSets":"BrandingSet",
"classes":"ApexClass",
"contentassets":"ContentAsset",
"customMetadata":"CustomMetadata",
"customPermissions":"CustomPermission",
"dashboards":"Dashboard",
"delegateGroups":"DelegateGroup",
"duplicateRules":"DuplicateRule",
"email":"EmailTemplate",
"experiences":"ExperienceBundle",
"flexipages":"FlexiPage",
"flowDefinitions":"FlowDefinition",
"flows":"Flow",
"globalValueSets":"GlobalValueSet",
"groups":"Group",
"labels":"CustomLabels",
"layouts":"Layout",
"LeadConvertSettings":"LeadConvertSettings",
"letterhead":"Letterhead",
"lightningExperienceThemes":"LightningExperienceTheme",
"lwc":"LightningComponentBundle",
"matchingRules":"MatchingRule",
"messageChannels":"LightningMessageChannel",
"navigationMenus":"NavigationMenu",
"networks":"Network",
"objectTranslations":"CustomObjectTranslation",
"objects":"CustomObject",
"pages":"ApexPage",
"pathAssistants":"PathAssistant",
"permissionsets":"PermissionSet",
"platformEventChannelMembers":"PlatformEventChannelMember",
"profilePasswordPolicies":"ProfilePasswordPolicy",
"profileSessionSettings":"ProfilePasswordPolicy",
"profiles":"Profile",
"queues":"Queue",
"quickActions":"QuickAction",
"reportTypes":"ReportType",
"reports":"Report",
"remoteSiteSettings": "RemoteSiteSetting",
"prompts": "Prompt",
"roles":"Role",
"settings":"Settings",
"sharingRules":"sharingRules",
"sharingSets":"SharingRules",
"sites":"CustomSite",
"standardValueSets":"StandardValueSet",
"staticresources":"StaticResource",
"tabs":"CustomTab",
"territory2Models":"Territory2Model",
"territory2Types":"Territory2Type",
"triggers":"ApexTrigger",
"wave":"wave",
"workflows":"Workflow",
}




folder_reqd_items = ['Report', 'Dashboard', 'Document','EmailTemplate' ]


def read_metadata_file(url):
    response = requests.get(url)
    data = json.loads(response.text)
    return data

 
