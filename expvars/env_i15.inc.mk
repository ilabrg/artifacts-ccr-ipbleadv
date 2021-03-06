# Configure connection manager params
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MIN_MS=15
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MAX_MS=15
CFLAGS += -DNIMBLE_RPBLE_CONN_LATENCY=0
CFLAGS += -DNIMBLE_RPBLE_CONN_SUPER_TO_MS=225

CFLAGS += -DNIMBLE_AUTOCONN_CONN_ITVL_MIN_MS=15
CFLAGS += -DNIMBLE_AUTOCONN_CONN_ITVL_MAX_MS=15
CFLAGS += -DNIMBLE_AUTOCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_AUTOCONN_CONN_SVTO_MS=225

CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MIN_MS=15
CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MAX_MS=15
CFLAGS += -DNIMBLE_STATCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_STATCONN_CONN_SUPERTO_MS=225

CFLAGS += -DCONFIG_GCOAP_NON_TIMEOUT=25000000

