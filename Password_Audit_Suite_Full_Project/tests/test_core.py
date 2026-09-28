import tempfile
import unittest
from pathlib import Path
from suite.core import analyze, estimate, inspect_hash, inspect_shadow_fixture, simulate, variants, audit_csv, report_html

class CoreTests(unittest.TestCase):
    def test_variants_bounded(self):
        self.assertIn('demo123',variants('demo'))
        with self.assertRaises(ValueError): variants('x',5001)
    def test_analysis(self):
        self.assertEqual(analyze('password123')['rating'],'weak')
        self.assertEqual(analyze('Copper!Garden!Lantern!72')['rating'],'stronger')
    def test_hash_format(self):
        self.assertEqual(inspect_hash('$6$salt$example')['format'],'sha512-crypt')
        self.assertIn('ambiguous',inspect_hash('0'*32)['format'])
    def test_simulation(self):
        self.assertEqual(simulate('demo123',variants('demo'))['matched'],True)
        self.assertEqual(simulate('other',variants('demo'),3)['attempts'],3)
    def test_estimate(self):
        self.assertEqual(estimate(2,10,10)['average_seconds'],5)
    def test_report_no_plaintext(self):
        rows=audit_csv('samples/lab_passwords.csv')
        self.assertNotIn('password123',str(rows))
    def test_fixture_redacts_hash(self):
        rows=inspect_shadow_fixture('samples/synthetic_shadow.txt')
        self.assertEqual(rows[0]['format'],'sha512-crypt')
        self.assertNotIn('labSalt',str(rows))
    def test_html_escapes_label(self):
        page=report_html({'sample_count':1,'weak_count':1,
                          'results':[{'label':'<script>','length':3,'rating':'weak','reasons':[]}],
                          'recommendations':['MFA']})
        self.assertNotIn('<script>',page)
        self.assertIn('&lt;script&gt;',page)
    def test_shadow_fixture_handles_bom(self):
        with tempfile.NamedTemporaryFile('w', encoding='utf-8-sig', newline='\n', delete=False) as handle:
            handle.write('demo:$6$labSalt$illustrativeOnly:20000:0:99999:7:::\n')
            path = handle.name
        try:
            rows = inspect_shadow_fixture(path)
            self.assertEqual(rows[0]['account'], 'demo')
            self.assertEqual(rows[0]['format'], 'sha512-crypt')
        finally:
            Path(path).unlink(missing_ok=True)
if __name__=='__main__': unittest.main()
