from enum import StrEnum


class Aggregator(StrEnum):
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    P50 = "p50"
    P90 = "p90"
    P99 = "p99"
    P999 = "p999"
    P9999 = "p9999"
    P99999 = "p99999"
    DEV = "dev"
    ZIMSUM = "zimsum"
    MINMIN = "minmin"
    MINMAX = "minmax"


class FilterType(StrEnum):
    LITERAL_OR = "literal_or"
    ILITERAL_OR = "iliteral_or"
    NOT_LITERAL_OR = "not_literal_or"
    NOT_ILITERAL_OR = "not_iliteral_or"
    WILDCARD = "wildcard"
    IWILDCARD = "iwildcard"
    REGEXP = "regexp"


class MultiFunction(StrEnum):
    HIST_HEATMAP = "hist_heatmap"
    HIST_SUM = "hist_sum"
    HIST_COUNT = "hist_count"
    HIST_AVG = "hist_avg"
    HIST_PERCENTILE = "hist_percentile"
    WEIGHTED_AVG = "weighted_avg"
