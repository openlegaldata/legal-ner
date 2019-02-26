from unittest import TestCase

from legal_ner.preprocessing import HtmlConcealer


class HtmlConcealerTestCase(TestCase):

    def test_html_concealing(self):
        html = '<h2>Tenor</h2>\n\n<ul class="ol"><li><p>1. Unter   Ab&#228;nderung des Beschlusses der Kammer'
        concealer = HtmlConcealer(html)
        concealer.conceal()
        self.assertEqual('Tenor\n1. Unter Abänderung des Beschlusses der Kammer', concealer.get_content())

    def test_remove_enumeration_numbers(self):
        html = '1. Unter\n' \
               'a)Unter\n' \
               ' a) Unter\n' \
               'III. Unter\n' \
               '19Unter'
        concealer = HtmlConcealer(html)
        concealer.remove_enumeration_numbers()
        self.assertEqual('Unter\nUnter\nUnter\nUnter\nUnter', concealer.get_content())

    def test_html_concealing_pos_table(self):
        html = '<h2>Tenor</h2>\n<ul class="ol"><li><p>1. Unter Ab&#228;nderung des Beschlusses der Kammer'
        concealer = HtmlConcealer(html)
        concealer.conceal()
        concealed_word = concealer.get_content()[15:25]
        html_word = html[46:61]
        self.assertEqual(concealed_word, 'Abänderung')
        self.assertEqual(html_word, 'Ab&#228;nderung')
        self.assertEqual(concealer.concealed_to_html_pos(15, 25), (46, 61))
