# Proof-of-concept module
DOCUMENTATION='''
'''

EXAMPLES='''
'''

class ProofOfConceptClass:
    def __init__(self, **kwargs):
        self.initialized = True

    def __eq__(self, other):
        assert isinstance(other, ProofOfConceptClass), "Incompatible equiv comparision."
        return self.initialized == other.initialized

def main():
    module = AnsibleModule(
            argument_spec=dict(
                    param=dict(type='str',default='foobar')
                ),
            supports_check_mode=True
            )

    changed=False
    try:
        module.exit_json(changed=changed, param=module.params['param'])
    except Exception as e:
        module.fail_json(msg=e.message)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
