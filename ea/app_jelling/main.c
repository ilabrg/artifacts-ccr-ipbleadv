/*
 * Copyright (C) 2020 Freie Universität Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     em6_coapexp
 * @{
 *
 * @file
 * @brief       em6 Coap Exp
 *
 * @author      Hauke Petersen <hauke.petersen@fu-berlin.de>
 *
 * @}
 */

#include "myprint.h"
#include "coapexp.h"
#if IS_USED(MODULE_ALIVE)
#include "alive.h"
#endif
#ifdef MODULE_LLSTATS
#include "llstats.h"
#endif
#include "tramp.h"

int main(void)
{
    myputs(APPNAME);

    tramp_run();

#if IS_USED(MODULE_ALIVE)
    alive_run();
#endif
#ifdef MODULE_LLSTATS
    llstats_run();
#endif
    coapexp_run();

    return 0;
}
