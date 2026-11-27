"""Detection dates must survive later scans without inventing sheet insertion times."""
from unittest import TestCase, main
from watch_storyboards import observe


class DetectionDates(TestCase):
    def test_legacy_rows_remain_seen_without_a_fabricated_detection_date(self):
        row = {'key': 'legacy', 'driveCreatedAt': '2026-11-23T23:30:00Z'}
        rows, new, state = observe([row], {'seen': ['legacy']}, '2026-11-24T08:00:00Z')
        self.assertEqual(new, [])
        self.assertIsNone(rows[0]['firstDetectedAt'])
        self.assertEqual(rows[0]['driveCreatedLocal'], '24/11/2026 00:30')
        self.assertEqual(state['seen'], ['legacy'])

    def test_new_detection_keeps_its_first_time_and_does_not_repeat_the_alert(self):
        row = {'key': 'new', 'driveCreatedAt': '2026-11-20T08:00:00Z'}
        rows, new, state = observe([row], {}, '2026-11-24T08:00:00Z')
        self.assertEqual(new[0]['firstDetectedLocal'], '24/11/2026 09:00')
        self.assertEqual(new[0]['driveCreatedLocal'], '20/11/2026 09:00')
        again, new, later = observe([row], state, '2026-11-24T10:00:00Z')
        self.assertEqual(new, [])
        self.assertEqual(again, rows)
        self.assertEqual(later, state)

    def test_baseline_suppresses_alerts_and_preserves_unknown_state_fields(self):
        rows, new, state = observe([{'key': 'new'}], {'extra': 'keep'}, '2026-11-24T08:00:00Z', True)
        self.assertEqual(new, [])
        self.assertIsNone(rows[0]['driveCreatedLocal'])
        self.assertEqual(state['extra'], 'keep')
        self.assertEqual(state['firstDetectedAt']['new'], '2026-11-24T08:00:00Z')

    def test_assignment_change_is_reported_without_realerting_the_storyboard(self):
        row = {'key': 'existing', 'motionDesigner': 'Personne B', 'status': 'En cours'}
        rows, new, state = observe([row], {'seen': ['existing']}, '2026-11-27T09:00:00Z')
        self.assertEqual(rows[0]['motionDesigner'], 'Personne B')
        self.assertEqual(new, [])
        self.assertIsNone(rows[0]['firstDetectedAt'])


if __name__ == '__main__':
    main()
