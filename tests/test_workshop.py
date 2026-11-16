"""Dependency-free checks for the static workshop and its worked examples."""

from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import unittest
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.slides = []
        self.stack = []
        self.errors = []
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'section' and 'slide' in attrs.get('class', '').split():
            self.slides.append(attrs)
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f'Unexpected closing {tag}; open: {self.stack[-3:]}')
        else:
            self.stack.pop()


def scripts(source):
    return '\n'.join(re.findall(r'<script[^>]*>(.*?)</script>', source, re.S))


class WorkshopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deck = (ROOT / 'index.html').read_text()
        cls.reference = (ROOT / 'workshop.html').read_text()
        cls.doc = Document(cls.deck)
        # Pure template functions can be tested without a browser or DOM library.
        runner = """
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(0, 'utf8');
const context = {document: {addEventListener() {}}};
vm.createContext(context);
vm.runInContext(source, context);
const pages = vm.runInContext(`({
  home: buildHome(), pair: buildPairProgrammingTab(),
  mock: buildMockInterviewsTab(), resources: buildResourcesTab(),
  ...Object.fromEntries(['universal','bada','ds','demle','swe','aiswe'].map(key =>
    [key, buildStreamTab(key, key, '')]))
})`, context);
process.stdout.write(JSON.stringify(pages));
"""
        result = subprocess.run(['node', '-e', runner], input=scripts(cls.reference),
                                text=True, capture_output=True, check=True)
        cls.pages = json.loads(result.stdout)

    def test_html_is_balanced_and_ids_are_unique(self):
        for name, source in [('deck', self.deck), ('reference', self.reference), *self.pages.items()]:
            with self.subTest(name=name):
                doc = Document(source)
                self.assertEqual(doc.errors, [])
                self.assertEqual(doc.stack, [])
                self.assertEqual(len(doc.ids), len(set(doc.ids)))

    def test_javascript_parses(self):
        for source in [self.deck, self.reference]:
            result = subprocess.run(['node', '--check'], input=scripts(source),
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_local_links_and_fragments_exist(self):
        for source in [self.deck, self.reference, *self.pages.values()]:
            for link in Document(source).links:
                url = urlsplit(link)
                if url.scheme or url.netloc:
                    continue
                target = ROOT / (url.path or 'index.html')
                self.assertTrue(target.is_file(), link)
                if url.fragment:
                    self.assertIn(url.fragment, Document(target.read_text()).ids, link)

    def test_main_flow_ends_before_optional_practice(self):
        main = [s['id'] for s in self.doc.slides if 'data-extra' not in s]
        extra = [s['id'] for s in self.doc.slides if 'data-extra' in s]
        self.assertEqual(main[-1], 's-final')
        self.assertEqual(extra[0], 's-extra')
        for slide in ['s-mock-pvalue', 's-mock-etl', 's-start', 's-timer-pitch', 's-timer-mock']:
            self.assertIn(slide, extra)
            self.assertNotIn(slide, main)
        self.assertLess(main.index('s-retry'), main.index('s-pair-agents'))
        self.assertIn("extended || !s.hasAttribute('data-extra')", self.deck)
        self.assertIn('.slide[data-extra]{display:none}', self.deck)

    def test_timers_match_the_agenda(self):
        timers = dict((name, int(seconds)) for name, seconds in
                      re.findall(r"toggleTimer\('([^']+)',(\d+)\)", self.deck))
        self.assertEqual(sum(timers[n] for n in ['think', 'explain', 'followup', 'feedback']), 360)
        self.assertEqual(timers['retry'], 180)
        self.assertEqual(3 * 360, 18 * 60)
        self.assertEqual(3 * 180 + 60, 10 * 60)
        for name, seconds in timers.items():
            self.assertIn(f'id="timer-{name}-display">{seconds // 60}:{seconds % 60:02}',
                          self.deck.replace(' style="font-size:5rem"', ''))

    def test_documented_agenda_covers_one_hour(self):
        for path in ['README.md', 'guides/facilitator-runbook.md']:
            blocks = [(int(a), int(b)) for a, b in
                      re.findall(r'^\| (\d+)–(\d+) min \|', (ROOT / path).read_text(), re.M)]
            self.assertEqual(blocks[0][0], 0)
            self.assertEqual(blocks[-1][1], 60)
            self.assertTrue(all(a < b for a, b in blocks))
            self.assertEqual([b for _, b in blocks[:-1]], [a for a, _ in blocks[1:]])

    def test_lab_removed_and_no_stale_setup_links(self):
        for path in ['lab/app.py', 'pyproject.toml', 'uv.lock', '.marimo.toml',
                     'solutions/case_1.sql', 'guides/candidate-guide.md']:
            self.assertFalse((ROOT / path).exists(), path)
        for source in [self.deck, self.reference]:
            for stale in ['marimo', 'uv sync', 'SQL Debugging Lab', '35:00', 'localhost:2718']:
                self.assertNotIn(stale, source)

    def test_pair_programming_content_is_in_reference(self):
        pair = self.pages['pair']
        for phrase in ['AI agents', 'interview\'s policy', '10 minutes', '24h exactly',
                       'dragon', 'independent', 'Staff Data Engineer', 'endorsement']:
            self.assertIn(phrase, pair)
        self.assertIn("{id:'pair',label:'Pair Programming'}", self.reference)
        self.assertNotIn("{id:'debug'", self.reference)

    def test_date_comparison_and_elapsed_comparison_disagree(self):
        start = datetime(2026, 1, 10, 23, 55, tzinfo=timezone.utc)
        end = datetime(2026, 1, 11, 0, 5, tzinfo=timezone.utc)
        self.assertEqual(end - start, timedelta(minutes=10))
        self.assertGreater(end.date(), start.date())
        self.assertFalse(end - start >= timedelta(hours=24))
        for source in [self.deck, self.pages['pair']]:
            self.assertIn('23:55', source)
            self.assertIn('00:05', source)
            self.assertIn('10 minutes', source)

    def test_duration_table_matches_independent_expectations(self):
        # Expected results are computed from duration, not copied from the table.
        for label, minutes in [('23h 59m', 1439), ('24h exactly', 1440), ('24h 01m', 1441)]:
            expected = 'Yes' if timedelta(minutes=minutes) >= timedelta(hours=24) else 'No'
            for source in [self.deck, self.pages['pair']]:
                self.assertIn(f'<td>{label}</td><td>{expected}</td>', source)


if __name__ == '__main__':
    unittest.main()
