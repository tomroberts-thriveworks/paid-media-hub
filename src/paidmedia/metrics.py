"""Bookings* = Event 1 (online booking) + Event 4 (call-center booking).
CPB = spend / Bookings*. Never use a campaign's own 'conversions' count,
which for proxy-goaled campaigns includes calls and contacts."""

# Match conversion actions by name; confirm exact names once connected.
BOOKING_EVENT_NAMES = ("Event 1", "Event 4")


def is_booking_action(conversion_action_name: str) -> bool:
    n = conversion_action_name.lower()
    return any(e.lower() in n for e in BOOKING_EVENT_NAMES)


def cpb(spend: float, bookings: float):
    return None if not bookings else spend / bookings
