# Configure connection manager params
CFLAGS += -DNIMBLE_NETIF_CONN_ITVL_SPACING=1

CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MIN_MS=80
CFLAGS += -DNIMBLE_RPBLE_CONN_ITVL_MAX_MS=120
CFLAGS += -DNIMBLE_RPBLE_CONN_LATENCY=0
CFLAGS += -DNIMBLE_RPBLE_CONN_SUPER_TO_MS=1500

CFLAGS += -DNIMBLE_AUTOCONN_CONN_ITVL_MS=80
CFLAGS += -DNIMBLE_AUTOCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_AUTOCONN_CONN_SVTO_MS=1500

CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MIN_MS=80
CFLAGS += -DNIMBLE_STATCONN_CONN_ITVL_MAX_MS=120
CFLAGS += -DNIMBLE_STATCONN_CONN_LATENCY=0
CFLAGS += -DNIMBLE_STATCONN_CONN_SUPERTO_MS=1500

CFLAGS += -DCONFIG_GCOAP_NON_TIMEOUT=25000000
