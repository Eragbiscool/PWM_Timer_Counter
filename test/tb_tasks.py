

import cocotb
from cocotb.triggers import RisingEdge, Timer

# ----------------------------------------------------------------------
# Macro definitions (replace these with your actual values if different)
# ----------------------------------------------------------------------

PTC_RPTC_CNTR      = 0
PTC_RPTC_HRC       = 1
PTC_RPTC_LRC       = 2
PTC_RPTC_CTRL      = 3


PTC_RPTC_CTRL_EN      = 0
PTC_RPTC_CTRL_ECLK    = 1
PTC_RPTC_CTRL_CNTRRST = 7
# ----------------------------------------------------------------------
# Task translations
# ----------------------------------------------------------------------

async def wr(dut, adr, dat, we):
    """Write transaction"""
    await RisingEdge(dut.clk)
    await Timer(1, "ns")

    dut.adr.value = adr
    dut.data_in.value = dat
    dut.re.value = 0b11

    # wait 5 cycles
    for _ in range(5):
        await RisingEdge(dut.clk)

    await Timer(1, "ns")
    dut.we.value = we

    await RisingEdge(dut.clk)
    await Timer(1, "ns")
    dut.we.value = 0b11

    await RisingEdge(dut.clk)


async def rd(dut, adr):
    """Read transaction"""
    dut.adr.value = adr
    dut.re.value = 0b10
    dut.we.value = 0b11

    await Timer(1, "ns")
    result = int(dut.data_out.value)

    dut.re.value = 0b11
    return result


async def setctrl(dut, val):
    await wr(dut, (PTC_RPTC_CTRL << 2), val, 0b10)


async def sethrc(dut, val):
    await wr(dut, (PTC_RPTC_HRC << 2), val, 0b10)


async def setlrc(dut, val):
    await wr(dut, (PTC_RPTC_LRC << 2), val, 0b10)


async def getcntr(dut):
    tmp = await rd(dut, (PTC_RPTC_CNTR << 2))
    return tmp

# ----------------------------------------------------------------------
# Test converted from SV "test_eclk" task
# ----------------------------------------------------------------------

async def test_eclk(dut):
    """Testing control bit RPTC_CTRL[ECLK]"""

    cocotb.log.info("Testing control bit RPTC_CTRL[ECLK] ...")

    # Reset counter
    await setctrl(dut, 1 << PTC_RPTC_CTRL_CNTRRST)

    # Set HRC and LRC to max
    await sethrc(dut, 0xFFFFFFFF)
    await setlrc(dut, 0xFFFFFFFF)

    # Enable PTC
    await setctrl(dut, 1 << PTC_RPTC_CTRL_EN)

    # Wait for time to advance
    await Timer(400, "ns")

    l1 = await getcntr(dut)

    # Phase 2
    await setctrl(dut, 1 << PTC_RPTC_CTRL_CNTRRST)
    await setctrl(dut, (1 << PTC_RPTC_CTRL_EN) | (1 << PTC_RPTC_CTRL_ECLK))

    # Do 100 external clock cycles
    for _ in range(100):
        dut.ptc_ecgt.value = not dut.ptc_ecgt.value
        await Timer(4, "ns")

    l2 = await getcntr(dut)

    # Compare
    if l2 - l1 == 49:
        cocotb.log.info("OK")
    else:
        cocotb.log.error(f"FAILED: expected 49, got {l2 - l1}")


# test_ptc.py
#
# Top-level cocotb test converted from SV "initial begin" block
#

@cocotb.test()
async def ptc_verification(dut):
    """Top-level PTC IP Core Verification"""

    # Equivalent of SV variable initializations

    # Display banners
    cocotb.log.info("")
    cocotb.log.info("###")
    cocotb.log.info("### PTC IP Core Verification ###")
    cocotb.log.info("###")
    cocotb.log.info("I. Testing correct operation of RPTC_CTRL control bits")
    cocotb.log.info("")

    await test_eclk(dut)

    cocotb.log.info("###")
    cocotb.log.info("")

    # End of simulation
    raise TestSuccess("PTC IP Core Verification completed")
