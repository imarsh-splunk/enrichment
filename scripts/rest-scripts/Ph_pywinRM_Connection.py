from winrm.protocol import Protocol

p = Protocol(
    endpoint='https://10.0.0.254:5986/wsman',
    transport='ntlm',
    username=r'.\Administrator',
    password='UpperLimit612@',
    server_cert_validation='ignore')

shell_id = p.open_shell()
command_id = p.run_command(shell_id, 'whoami')

# command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
std_out, std_err, status_code = p.get_command_output(shell_id, command_id)

print(std_out)
print(std_err)
print(status_code)

p.cleanup_command(shell_id, command_id)
p.close_shell(shell_id)