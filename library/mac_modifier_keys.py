#!/usr/bin/python
# -*- coding: UTF-8

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mac_modifier_keys

short_description: This is my test module

version_added: "2.4"

description:
    - "This is my longer description explaining my test module"

options:
    caps_lock:
        description:
            - This is the message to send to the test module
        required: false
    control:
        description:
            - Control to demo if the result of this module is changed or not
        required: false
    option:
        description:
            - Control to demo if the result of this module is changed or not
        required: false
    command:
        description:
            - Control to demo if the result of this module is changed or not
        required: false
    function:
        description:
            - Control to demo if the result of this module is changed or not
        required: false


extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_test:
    name: fail me
'''

RETURN = ''
# RETURN = '''
# original_message:
#     description: The original name param that was passed in
#     type: str
#     returned: always
# message:
#     description: The output message that the test module generates
#     type: str
#     returned: always
# '''

key_options = dict(
    caps_lock="⇪ Caps Lock",
    command="⌘ Command",
    control="⌃ Command",
    escape="⎋ Escape",
    option="⌥ Option",
    function="fn Function",
)

code = """
tell application "System Preferences"
	activate
	set current pane to pane "com.apple.preference.keyboard"
	delay 0.3
end tell

set changed to false
set keys to {¬
	{name:"Caps Lock (⇪) Key:", state:"⎋ Escape"}, ¬
	{name:"Command (⌘) Key:", state:"⌘ Command"}, ¬
	{name:"Control (⌃) Key:", state:"⌃ Control"}, ¬
	{name:"Option (⌥) Key:", state:"⌥ Option"} ¬
		}
#,{name:"Function (fn) Key:", state:"fn Function"}

# Open The Modifier Keys settings window
tell application "System Events"
	tell process "System Preferences"
		click button "Modifier Keys…" of tab group 1 of window "Keyboard"
		
		# Set all popup buttons to the values described in keys
		repeat with key in keys
			set keyName to name of key
			set keyValue to state of key
			set previous to value of pop up button keyName of sheet 1 of window "Keyboard"
			if previous is not keyValue then
				click pop up button keyName of sheet 1 of window "Keyboard"
				set previous to value of pop up button keyName of sheet 1 of window "Keyboard"
				click menu item keyValue of menu 1 of pop up button keyName of sheet 1 of window "Keyboard"
				set changed to true
			end if
		end repeat
		
		click button "OK" of sheet 1 of window "Keyboard"
	end tell
end tell

quit application "System Preferences"

return changed
"""

from ansible.module_utils.basic import AnsibleModule
import os
import subprocess


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # name=dict(type='str', required=False),
        # new=dict(type='bool', required=False, default=False)
    )

    result = dict(changed=False,
                  # state = key_options,
                  )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    proc = subprocess.Popen(['osascript'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(code.encode())
    stdout = stdout.strip()
    result['changed'] = (stdout == "true".encode())

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    # module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
