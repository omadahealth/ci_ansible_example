import unittest
import testinfra
import os

from molecule.command import create as molecule_create
from molecule.command import converge as molecule_converge
from molecule.command import destroy as molecule_destroy

class ProofOfConceptTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir('/Users/kevin.phillips/continuous_integration_ansible/roles/proof_of_concept')
        print ''
        molecule_create.Create(dict(), dict()).execute()
        molecule_converge.Converge(dict(), dict()).execute()

    @classmethod
    def tearDownClass(cls):
        os.chdir('/Users/kevin.phillips/continuous_integration_ansible/roles/proof_of_concept')
        print ''
        molecule_destroy.Destroy(dict(), dict()).execute()

    def setUp(self):
        # Configure testinfra backend
        self.conn = testinfra.get_backend('ansible://all', \
                                            ansible_inventory="%s/inventory" % os.path.dirname(os.path.realpath(__file__)))

    def test_subject_hosts_file_unittest(self):
        self.assertEquals(True, True)

    def test_subject_hosts_file_testinfra(self):
        File = self.conn.get_module("File")
        hosts = File('/etc/hosts')

        assert hosts.user == 'root'
        assert hosts.group == 'root'
