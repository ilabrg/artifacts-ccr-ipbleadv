
#include <stdlib.h>
#include <string.h>

#include "random.h"
#include "ztimer.h"
#include "fmt.h"

#include "myprint.h"
#include "llstats.h"

#define STARTUP_DELAY       (2 * 1000U)
#define STARTUP_JITTER      (200)
#define INTERVAL            (5 * 1000U)
#define CHAR_NA             '-'

#define PRIO                (THREAD_PRIORITY_MAIN + 2)
static char _stack[THREAD_STACKSIZE_DEFAULT];


// extern struct ble_ll_conn_sm g_ble_ll_conn_sm[MYNEWT_VAL_BLE_MAX_CONNECTIONS];
// static struct ble_ll_conn_sm _smtmp[MYNEWT_VAL_BLE_MAX_CONNECTIONS];

#if IS_USED(MODULE_NIMBLE_JELLING)
llstats_adv_t llstats_adv;
#endif

#if IS_USED(MODULE_NIMBLE_NETIF)
llstats_conn_t llstats_conn[MYNEWT_VAL_BLE_MAX_CONNECTIONS];
static const char _charmap[62] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
static char _outtext[81];

static char _map_u32(unsigned cnt)
{
    if (cnt >= sizeof(_charmap)) {
        return CHAR_NA;
    }
    return _charmap[cnt];
}
#endif

llstats_phy_t llstats_phy;

#if IS_USED(MODULE_NIMBLE_JELLING)
static void _dump_adv(void)
{
    llstats_adv_t tmp;

    unsigned is = irq_disable();
    memcpy(&tmp, &llstats_adv, sizeof(llstats_adv_t));
    memset(&llstats_adv, 0, sizeof(llstats_adv_t));
    irq_restore(is);
    myprintf("ll,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld\n",
                tmp.chan[0].tx, tmp.chan[1].tx, tmp.chan[2].tx, tmp.chan[3].tx,
                tmp.chan[0].rx, tmp.chan[1].rx, tmp.chan[2].rx, tmp.chan[3].rx,
                tmp.jelling_duplicate, tmp.jelling_known_packet, tmp.jelling_unknown_packet,
                tmp.chan[0].rx_err, tmp.chan[1].rx_err, tmp.chan[2].rx_err, tmp.chan[3].rx_err,
                tmp.chan[0].aux_not_schedulable, tmp.chan[1].aux_not_schedulable, tmp.chan[2].aux_not_schedulable, tmp.chan[3].aux_not_schedulable,
                tmp.chan[0].adv_event_dropped, tmp.chan[1].adv_event_dropped, tmp.chan[2].adv_event_dropped, tmp.chan[3].adv_event_dropped,
                tmp.chan[0].crc_phy_err, tmp.chan[1].crc_phy_err, tmp.chan[2].crc_phy_err, tmp.chan[3].crc_phy_err,
                tmp.chan[3].aux_chain_err, tmp.jelling_broken_data,
                tmp.chan[0].rssi, tmp.chan[1].rssi, tmp.chan[2].rssi, tmp.chan[3].rssi,
                tmp.chan[0].rssi_crc, tmp.chan[1].rssi_crc, tmp.chan[2].rssi_crc, tmp.chan[3].rssi_crc);
}
#endif

#if IS_USED(MODULE_NIMBLE_NETIF)
static void _dump_conn(void)
{
    llstats_conn_t tmp;

    for (unsigned i = 0; i < MYNEWT_VAL_BLE_MAX_CONNECTIONS; i++) {
        if (llstats_conn[i].used == 1) {
            unsigned is = irq_disable();
            memcpy(&tmp, &llstats_conn[i], sizeof(llstats_conn_t));
            memset(&llstats_conn[i], 0, sizeof(llstats_conn_t));
            irq_restore(is);

            unsigned pos = 0;
            for (unsigned c = 0; c < BLE_CHAN_NUMOF; c++) {
                _outtext[pos++] = _map_u32(tmp.chan[c].tx);
                _outtext[pos++] = _map_u32(tmp.chan[c].ok);
            }
            _outtext[pos] = '\0';
            myprintf("ll%u,%s\n", (i + 1), _outtext);
        }
    }
}
#endif

static void _dump_phy(void)
{
    uint32_t now = ztimer_now(ZTIMER_USEC);
    uint32_t rx;
    uint32_t tx;
    uint32_t itvl_start;
    uint32_t rx_cnt;
    uint32_t rx_cnt_off;
    uint32_t tx_cnt;
    uint32_t tx_cnt_off;

    /* copy stats */
    unsigned is = irq_disable();
    rx = llstats_phy.rx;
    llstats_phy.rx = 0;
    tx = llstats_phy.tx;
    llstats_phy.tx = 0;
    itvl_start = llstats_phy.itvl_start;
    llstats_phy.itvl_start = now;

    rx_cnt = llstats_phy.rx_cnt;
    llstats_phy.rx_cnt = 0;
    rx_cnt_off = llstats_phy.rx_cnt_off;
    llstats_phy.rx_cnt_off = 0;
    tx_cnt = llstats_phy.tx_cnt;
    llstats_phy.tx_cnt = 0;
    tx_cnt_off = llstats_phy.tx_cnt_off;
    llstats_phy.tx_cnt_off = 0;

#if PHYDBG
    uint32_t cnt_isr = llstats_phy.dbg_cnt_isr;
    llstats_phy.dbg_cnt_isr = 0;
    uint32_t cnt_disable = llstats_phy.dbg_cnt_phydisable;
    llstats_phy.dbg_cnt_phydisable = 0;
    uint32_t cnt_addrisr = llstats_phy.dbg_cnt_addrisr;
    llstats_phy.dbg_cnt_addrisr = 0;
    uint32_t cnt_phyrxrestart = llstats_phy.dbg_cnt_phyrxrestart;
    llstats_phy.dbg_cnt_phyrxrestart = 0;
    uint32_t cnt_rxabort = llstats_phy.dbg_cnt_rxabort;
    llstats_phy.dbg_cnt_rxabort = 0;
    uint32_t cnt_rxdisablefromisr = llstats_phy.dbg_cnt_rxdisablefromisr;
    llstats_phy.dbg_cnt_rxdisablefromisr = 0;
    uint32_t rx_cnt_off_dummy = llstats_phy.rx_cnt_off_dummy;
    llstats_phy.rx_cnt_off_dummy = 0;
#endif
    irq_restore(is);

    uint32_t itvl = now - itvl_start;
    myprintf("ls,%u,%u,%u,%u,%u,%u,%u,%u\n",
             (unsigned)itvl, (unsigned)os_msys_num_free(),
             (unsigned)rx_cnt, (unsigned)rx_cnt_off, (unsigned)rx,
             (unsigned)tx_cnt, (unsigned)tx_cnt_off, (unsigned)tx);
#if PHYDBG
    myprintf("lldbg,%u,%u,%u,%u,%u,%u,%u\n",
             (unsigned)cnt_isr, (unsigned)cnt_disable, (unsigned)cnt_addrisr,
             (unsigned)cnt_phyrxrestart, (unsigned)cnt_rxabort, (unsigned)cnt_rxdisablefromisr,
             (unsigned)rx_cnt_off_dummy);
#endif
}

static void *_printer_worker(void *arg)
{
    (void)arg;

    ztimer_sleep(ZTIMER_MSEC,
                 (STARTUP_DELAY + random_uint32_range(0, STARTUP_JITTER)));

    uint32_t last_wakeup = ztimer_now(ZTIMER_MSEC);
    while (1) {
        ztimer_periodic_wakeup(ZTIMER_MSEC, &last_wakeup, INTERVAL);

#if IS_USED(MODULE_NIMBLE_JELLING)
        _dump_adv();
#endif
#if IS_USED(MODULE_NIMBLE_NETIF)
        _dump_conn();
#endif
        _dump_phy();
    }

    return NULL;        /* never reached */
}

void llstats_run(void)
{
#if IS_USED(MODULE_NIMBLE_JELLING)
    memset(&llstats_adv, 0, sizeof(llstats_adv));
#endif
#if IS_USED(MODULE_NIMBLE_NETIF)
    memset(llstats_conn, 0, sizeof(llstats_conn));
#endif

    memset(&llstats_phy, 0, sizeof(llstats_phy));
    llstats_phy.itvl_start = ztimer_now(ZTIMER_USEC);

    thread_create(_stack, sizeof(_stack),
                  PRIO, THREAD_CREATE_STACKTEST,
                  _printer_worker, NULL, "llstats");
}
