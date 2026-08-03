import unittest

from ui_theme import maximize_window, remember_window_state, restore_window


class FakeWindow:
    def __init__(self, state_error=False):
        self.state_error = state_error
        self.states = []
        self.attributes_calls = []
        self.geometry_calls = []
        self.deiconify_calls = 0
        self.after_calls = []
        self.updated = False
        self._state = "normal"

    def state(self, value):
        if self.state_error:
            raise RuntimeError("state not supported")
        self.states.append(value)
        self._state = value

    def attributes(self, name, value):
        self.attributes_calls.append((name, value))

    def wm_state(self):
        return self._state

    def winfo_screenwidth(self):
        return 1920

    def winfo_screenheight(self):
        return 1080

    def geometry(self, value):
        self.geometry_calls.append(value)

    def deiconify(self):
        self.deiconify_calls += 1

    def update_idletasks(self):
        self.updated = True

    def after(self, delay, callback):
        self.after_calls.append((delay, callback))


class MaximizeWindowTests(unittest.TestCase):
    def test_maximize_window_uses_zoomed_state_when_supported(self):
        window = FakeWindow()

        maximize_window(window)

        self.assertIn("zoomed", window.states)
        self.assertEqual(window.attributes_calls[0], ("-zoomed", True))

    def test_maximize_window_falls_back_to_geometry_when_state_is_not_supported(self):
        window = FakeWindow(state_error=True)

        maximize_window(window)

        self.assertEqual(window.geometry_calls, ["1920x1080+0+0"])

    def test_restore_window_remaximizes_after_reshowing(self):
        window = FakeWindow()
        window._saved_window_state = "zoomed"

        restore_window(window)

        self.assertEqual(window.deiconify_calls, 1)
        self.assertTrue(window.updated)
        self.assertEqual(window.after_calls[0][0], 0)

        window.after_calls[0][1]()

        self.assertIn("zoomed", window.states)

    def test_remember_window_state_preserves_previous_state(self):
        window = FakeWindow()
        window.state("zoomed")

        remember_window_state(window)
        restore_window(window)

        self.assertEqual(window._saved_window_state, "zoomed")


if __name__ == "__main__":
    unittest.main()
