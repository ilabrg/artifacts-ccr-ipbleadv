# Configure connection manager params
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MIN=10000
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MAX=10000
CFLAGS += -DNIMBLE_RPBLE_CONN_LATENCY=0
CFLAGS += -DNIMBLE_RPBLE_CONN_SUPER_TO=1000000

CFLAGS += -DNIMBLE_AUTOCONN_CONN_ITVL_MS=10
CFLAGS += -DNIMBLE_AUTOCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_AUTOCONN_CONN_SVTO_MS=1000

CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MS=10
CFLAGS += -DNIMBLE_STATCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_STATCONN_CONN_SUPERTO_MS=1000
