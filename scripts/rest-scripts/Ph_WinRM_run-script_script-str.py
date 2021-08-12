def GetMessageTrace_find_recipients(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('run_script_1() called')

    # collect data for 'run_script_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.fromEmail', 'artifact:*.cef.emailSubject'])
    
    #sender = re.search(r'<(.*?)>', container_data[0][0])
    sender = container_data[0][0]
    subject = container_data[0][1]
    
    parameters = []
    
    # build parameters list for 'run_script_1' call
    parameters.append({
        'shell_id': "",
        'parser': "",
        'ip_hostname': "https://10.0.0.110:5986",
        'async': "",
        'script_str': """
#POWERSHELL SCRIPT
$user = 'Herman@phantomengineering.onmicrosoft.com'
$pw = ConvertTo-SecureString '85Krispydoughnut' -AsPlainText -Force
$creds = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $user, $pw
$msoExchangeURL = 'https://ps.outlook.com/PowerShell-LiveID?PSVersion=4.0' 
$session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri $msoExchangeURL -Credential $creds -Authentication Basic -AllowRedirection 
$null = Import-PSSession $session -AllowClobber

$trace = Get-MessageTrace -SenderAddress '{0}' -Status Delivered | Where {{$_.Subject -like '{1}'}}

foreach($item in $trace){{

    $recipients = Get-Recipient -ResultSize unlimited -Identity $item.RecipientAddress | select PrimarySmtpAddress, RecipientType
    
    if ($recipients.RecipientType -notlike 'UserMailbox'){{
        
        Get-DistributionGroupMember -Identity $recipients.PrimarySmtpAddress | select PrimarySmtpAddress

    }} else {{
        
        $recipients.PrimarySmtpAddress
        
    }}
}}

Remove-PSSession $Session""".format(sender, subject),
        'script_file': "",
        'command_id': "",
        })

    phantom.act("run script", parameters=parameters, assets=['win10vm_homelab'], callback=run_script_2, name="GetMessageTrace_find_recipients")

    return