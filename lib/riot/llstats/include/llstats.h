
#ifndef LLSTATS_H
#define LLSTATS_H


#define PHYDBG      0

#include "controller/ble_ll_conn.h"
#include "net/ble.h"

#include "myprint.h"


#ifdef __cplusplus
extern "C" {
#endif

#if IS_USED(MODULE_NIMBLE_JELLING)
typedef struct {
    struct {
        unsigned tx;        /* # of all packets transmitted */
        unsigned rx; /* all packets received in phy, even faulty */
        unsigned rx_err; /* faulty marked */
        unsigned aux_not_schedulable;
        unsigned adv_event_dropped;
        unsigned crc_phy_err; /* only for sanity! should be included in rx_err */
        unsigned aux_chain_err;
        int32_t rssi;
        int32_t rssi_crc;
    } chan[4];
    unsigned jelling_unknown_packet;
    unsigned jelling_known_packet;
    unsigned jelling_broken_data;
    unsigned jelling_duplicate;
} llstats_adv_t;

extern llstats_adv_t llstats_adv;
#endif

#if IS_USED(MODULE_NIMBLE_NETIF)
typedef struct {
    struct {
        unsigned tx;        /* # of all packets transmitted */
        unsigned ok;        /* # of valid ACKS received */
    } chan[BLE_CHAN_NUMOF];
    uint8_t used;
} llstats_conn_t;

extern llstats_conn_t llstats_conn[MYNEWT_VAL_BLE_MAX_CONNECTIONS];
#endif

typedef struct {
    uint32_t itvl_start;
    uint8_t rx_active;
    uint32_t rx_start;
    uint32_t tx_start;
    uint32_t rx;
    uint32_t tx;
    uint32_t rx_cnt;
    uint32_t rx_cnt_off;
    uint32_t tx_cnt;
    uint32_t tx_cnt_off;
#if PHYDBG
    uint32_t dbg_cnt_isr;
    uint32_t dbg_cnt_phydisable;
    uint32_t dbg_cnt_addrisr;
    uint32_t dbg_cnt_phyrxrestart;
    uint32_t dbg_cnt_rxabort;
    uint32_t dbg_cnt_rxdisablefromisr;
    uint32_t rx_cnt_off_dummy;
#endif
} llstats_phy_t;

extern llstats_phy_t llstats_phy;


void llstats_run(void);

#if IS_USED(MODULE_NIMBLE_NETIF)
static inline void llstats_inc_tx(uint16_t conn, uint16_t chan)
{
    /* note: nimble uses connection handles starting from 1 */
    llstats_conn[conn - 1].used = 1;
    llstats_conn[conn - 1].chan[chan].tx++;
}

static inline void llstats_inc_tx_comp(uint16_t conn, uint16_t chan)
{
    /* note: nimble uses connection handles starting from 1 */
    llstats_conn[conn - 1].used = 1;
    llstats_conn[conn - 1].chan[chan].ok++;
}
#else
#define llstats_inc_tx(x,y)
#define llstats_inc_tx_comp(x,y)
#endif


#if IS_USED(MODULE_NIMBLE_JELLING)
static inline void llstats_inc_unknown_packet(void)
{
    llstats_adv.jelling_unknown_packet++;
}

static inline void llstats_inc_known_packet(void)
{
    llstats_adv.jelling_known_packet++;
}

static inline void llstats_inc_duplicate(void)
{
    llstats_adv.jelling_duplicate++;
}

static inline void llstats_inc_chan_tx(uint8_t chan)
{
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].tx++;
}

static inline void llstats_inc_chan_rx(uint8_t chan)
{
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].rx++;
}

static inline void llstats_inc_chan_rssi(uint8_t chan, int8_t rssi)
{
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].rssi += rssi;
}

static inline void llstats_inc_chan_rx_err(uint8_t chan)
{
    /* summarize data channels into one */
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].rx_err++;
}

static inline void llstats_inc_chan_crc_phy_err(uint8_t chan, int8_t rssi)
{
    /* summarize data channels into one */
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].crc_phy_err++;
    llstats_adv.chan[chan].rssi_crc += rssi;
}

static inline void llstats_inc_chan_adv_event_dropped(uint8_t chan)
{
    /* summarize data channels into one */
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].adv_event_dropped++;
}

static inline void llstats_inc_aux_chain_err(uint8_t chan) {
    /* summarize data channels into one */
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].aux_chain_err++;
}

static inline void llstats_inc_aux_not_schedulable(uint8_t chan) {
    chan = (chan < 37) ? 3 : (chan - 37);
    llstats_adv.chan[chan].aux_not_schedulable++;
}

static inline void llstats_jelling_broken_data(void) {
    llstats_adv.jelling_broken_data++;
}
#else
#define llstats_inc_unknown_packet()
#define llstats_inc_known_packet()
#define llstats_inc_duplicate()
#define llstats_inc_chan_tx(c)
#define llstats_inc_chan_rx(c)
#define llstats_inc_chan_rssi(c, r)
#define llstats_inc_chan_rx_err(c)
#define llstats_inc_chan_crc_phy_err(c, r)
#define llstats_inc_chan_adv_event_dropped(c)
#define llstats_inc_aux_chain_err(c)
#define llstats_inc_aux_not_schedulable(c)
#define llstats_jelling_broken_data()
#endif



static inline void llstats_dump_conn_tim(struct ble_ll_conn_sm *connsm, unsigned resched)
{
    myprintf("ll%u,%u(%u)\n",
             (unsigned)connsm->conn_handle,
             (unsigned)connsm->anchor_point, resched);
}

static inline void llstats_dump_slave_latency(struct ble_ll_conn_sm *connsm, uint16_t latency)
{
    myprintf("ll%u,sl%u,is%u\n",
             (unsigned)connsm->conn_handle,
             (unsigned)connsm->slave_latency,
             (unsigned)latency);
}

static inline void llstats_rxon(void)
{
#if PHYDBG
    if (llstats_phy.rx_active) {
        ++llstats_phy.rx_cnt_off_dummy;
    }
#endif
    llstats_phy.rx_active = 1;
    llstats_phy.rx_start = ztimer_now(ZTIMER_USEC);
    ++llstats_phy.rx_cnt;
}

static inline void llstats_rxoff(void)
{
    if (llstats_phy.rx_active == 1) {
        llstats_phy.rx_active = 0;
        llstats_phy.rx += (ztimer_now(ZTIMER_USEC) - llstats_phy.rx_start);
        ++llstats_phy.rx_cnt_off;
    }
}

static inline void llstats_txon(void)
{
    llstats_phy.tx_start = ztimer_now(ZTIMER_USEC);
    ++llstats_phy.tx_cnt;
}

static inline void llstats_txoff(void)
{
    llstats_phy.tx += (ztimer_now(ZTIMER_USEC) - llstats_phy.tx_start);
    ++llstats_phy.tx_cnt_off;
}

#if PHYDBG
static inline void llstats_phydbg_isrcnt(void)
{
    llstats_phy.dbg_cnt_isr++;
}

static inline void llstats_phydbg_disablecnt(void)
{
    llstats_phy.dbg_cnt_phydisable++;
}

static inline void llstats_phydbg_addrisr(void)
{
    llstats_phy.dbg_cnt_addrisr++;
}

static inline void llstats_phydbg_rxrestart(void)
{
    llstats_phy.dbg_cnt_phyrxrestart++;
}

static inline void llstats_rxabort(void)
{
    llstats_phy.dbg_cnt_rxabort++;
}

static inline void llstats_rxdisablefromisr(void)
{
    llstats_phy.dbg_cnt_rxdisablefromisr++;
}
#else
static inline void llstats_phydbg_isrcnt(void) {}
static inline void llstats_phydbg_disablecnt(void) {}
static inline void llstats_phydbg_addrisr(void) {}
static inline void llstats_phydbg_rxrestart(void) {}
static inline void llstats_rxabort(void) {}
static inline void llstats_rxdisablefromisr(void) {}
#endif

#ifdef __cplusplus
}
#endif

#endif /* LLSTATS_H */
/** @} */
