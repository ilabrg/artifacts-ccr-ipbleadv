# Configure gcoap
CFLAGS += -DCONFIG_GCOAP_PDU_BUF_SIZE=1400
CFLAGS += -DCONFIG_GCOAP_RESEND_BUFS_MAX=5
CFLAGS += -DCONFIG_GCOAP_REQ_WAITING_MAX=5

# Configure NimBLE buffers
CFLAGS += -DNIMBLE_NETIF_MTU=1400
