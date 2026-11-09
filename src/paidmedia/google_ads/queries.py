"""Read-only GAQL. Each entry: name -> (gaql, columns). Columns are attribute
paths on the result row and become the CSV headers. Micros stay raw in the CSV;
reports convert. Dates are filled in by the pull command."""

QUERIES = {
    "campaigns": (
        """SELECT campaign.id, campaign.name, campaign.status,
                  campaign.advertising_channel_type, campaign.bidding_strategy_type,
                  campaign_budget.amount_micros,
                  campaign.target_cpa.target_cpa_micros,
                  campaign.maximize_conversions.target_cpa_micros
           FROM campaign WHERE campaign.status != 'REMOVED'""",
        ["campaign.id", "campaign.name", "campaign.status",
         "campaign.advertising_channel_type", "campaign.bidding_strategy_type",
         "campaign_budget.amount_micros", "campaign.target_cpa.target_cpa_micros",
         "campaign.maximize_conversions.target_cpa_micros"],
    ),
    "conversion_actions": (
        """SELECT conversion_action.id, conversion_action.name, conversion_action.type,
                  conversion_action.status, conversion_action.category,
                  conversion_action.primary_for_goal,
                  conversion_action.include_in_conversions_metric, conversion_action.origin
           FROM conversion_action WHERE conversion_action.status != 'REMOVED'""",
        ["conversion_action.id", "conversion_action.name", "conversion_action.type",
         "conversion_action.status", "conversion_action.category",
         "conversion_action.primary_for_goal",
         "conversion_action.include_in_conversions_metric", "conversion_action.origin"],
    ),
    "campaign_daily": (
        """SELECT campaign.id, segments.date, metrics.cost_micros, metrics.clicks,
                  metrics.impressions
           FROM campaign WHERE segments.date BETWEEN '{start}' AND '{end}'""",
        ["campaign.id", "segments.date", "metrics.cost_micros", "metrics.clicks",
         "metrics.impressions"],
    ),
    "campaign_conversions": (
        """SELECT campaign.id, segments.date, segments.conversion_action_name,
                  metrics.conversions, metrics.conversions_value
           FROM campaign WHERE segments.date BETWEEN '{start}' AND '{end}'
             AND metrics.conversions > 0""",
        ["campaign.id", "segments.date", "segments.conversion_action_name",
         "metrics.conversions", "metrics.conversions_value"],
    ),
}
