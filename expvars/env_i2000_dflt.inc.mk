# Configure connection manager params
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MIN=2000000
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MAX=2000000
CFLAGS += -DNIMBLE_RPBLE_CONN_LATENCY=0
CFLAGS += -DNIMBLE_RPBLE_CONN_SUPER_TO=30000000

CFLAGS += -DNIMBLE_AUTOCONN_CONN_ITVL_MS=2000
CFLAGS += -DNIMBLE_AUTOCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_AUTOCONN_CONN_SVTO_MS=30000

CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MS=2000
CFLAGS += -DNIMBLE_STATCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_STATCONN_CONN_SUPERTO_MS=30000

CFLAGS += -DCONFIG_GCOAP_NON_TIMEOUT=25000000
