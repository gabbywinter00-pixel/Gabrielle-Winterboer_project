from data import get_ticketmaster_events

ticketmaster_data = get_ticketmaster_events("2026-07-01T00:00:00Z", "2026-08-01T23:59:59Z")

print(ticketmaster_data)
