# Configure connection manager params
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MIN=500000
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MAX=500000
CFLAGS += -DNIMBLE_RPBLE_CONN_LATENCY=0
CFLAGS += -DNIMBLE_RPBLE_CONN_SUPER_TO=7500000

CFLAGS += -DNIMBLE_AUTOCONN_CONN_ITVL_MS=500
CFLAGS += -DNIMBLE_AUTOCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_AUTOCONN_CONN_SVTO_MS=7500

CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MS=500
CFLAGS += -DNIMBLE_STATCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_STATCONN_CONN_SUPERTO_MS=7500

CFLAGS += -DCONFIG_GCOAP_NON_TIMEOUT=25000000
