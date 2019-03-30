from rest_framework.throttling import AnonRateThrottle


class AnonBurstRateThrottle(AnonRateThrottle):
    scope = 'burst'


class AnonSustainedRateThrottle(AnonRateThrottle):
    scope = 'sustained'
