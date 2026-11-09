"""Read-only GAQL. Conversions are segmented by action so Bookings* can be
computed from Event 1 + Event 4 only."""

CAMPAIGN_DAILY = """
SELECT campaign.id, campaign.name, campaign.status, segments.date,
       metrics.cost_micros, metrics.clicks, metrics.impressions
FROM campaign
WHERE segments.date BETWEEN '{start}' AND '{end}'
"""

CAMPAIGN_CONVERSIONS_BY_ACTION = """
SELECT campaign.id, segments.date, segments.conversion_action_name,
       metrics.conversions, metrics.conversions_value
FROM campaign
WHERE segments.date BETWEEN '{start}' AND '{end}'
  AND metrics.conversions > 0
"""
