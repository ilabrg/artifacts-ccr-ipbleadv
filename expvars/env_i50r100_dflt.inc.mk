# Configure connection manager params
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MIN=500000
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MAX=500000
CFLAGS += -DNIMBLE_RPBLE_CONN_LATENCY=0
CFLAGS += -DNIMBLE_RPBLE_CONN_SUPER_TO=1500000

CFLAGS += -DNIMBLE_AUTOCONN_CONN_ITVL_MS=75
CFLAGS += -DNIMBLE_AUTOCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_AUTOCONN_CONN_SVTO_MS=1500


CFLAGS += -DNIMBLE_STATCONN_CONNITVLRAND=1
CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MIN_MS=50
CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MAX_MS=100
CFLAGS += -DNIMBLE_STATCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_STATCONN_CONN_SUPERTO_MS=1500
