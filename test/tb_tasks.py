

import cocotb
from cocotb.triggers import RisingEdge, Timer

from tqv import TinyQV

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
PERIPHERAL_NUM = 0
async def generate_clock(dut, period_ns=8):
    """Generate clock on dut.clk"""
    cocotb.start_soon(Clock(dut.ui_in[0], period_ns, units="ns").start())

async def wr(adr, dat):
    """Write transaction"""
    await RisingEdge(dut.clk)
    await Timer(1, "ns")

    await tqv.write_word_reg(adr, dat)
    
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    
    # dut.data_read_n.value = 0b11

    # # wait 5 cycles
    # for _ in range(5):
    #     await RisingEdge(dut.clk)

    # await Timer(1, "ns")
    # dut.data_write_n.value = we

    # await RisingEdge(dut.clk)
    # await Timer(1, "ns")
    # dut.we.value = 0b11

    await RisingEdge(dut.clk)


async def rd(adr):
    """Read transaction"""

    # await tqv.read_word_reg(adr)


    # await Timer(1, "ns")

    result = await tqv.read_word_reg(adr)

    return result


async def setctrl(val):
    await wr((PTC_RPTC_CTRL << 2), val)


async def sethrc(val):
    await wr((PTC_RPTC_HRC << 2), val)


async def setlrc(val):
    await wr((PTC_RPTC_LRC << 2), val)


async def getcntr():
    tmp = await rd((PTC_RPTC_CNTR << 2))
    return tmp

# ----------------------------------------------------------------------
# Test converted from SV "test_eclk" task
# ----------------------------------------------------------------------

async def test_eclk():
    """Testing control bit RPTC_CTRL[ECLK]"""

    cocotb.log.info("Testing control bit RPTC_CTRL[ECLK] ...")

    # Reset counter
    await setctrl(1 << PTC_RPTC_CTRL_CNTRRST)

    # Set HRC and LRC to max
    await sethrc(0xFFFFFFFF)
    await setlrc(0xFFFFFFFF)

    # Enable PTC
    await setctrl(1 << PTC_RPTC_CTRL_EN)

    # Wait for time to advance
    await Timer(400, "ns")

    l1 = await getcntr()

    # Phase 2
    await setctrl(1 << PTC_RPTC_CTRL_CNTRRST)
    await setctrl((1 << PTC_RPTC_CTRL_EN) | (1 << PTC_RPTC_CTRL_ECLK))

    # Do 100 external clock cycles
    for _ in range(100):
        # dut.ptc_ecgt.value = not dut.ptc_ecgt.value
        await RisingEdge(dut.ui_in[0])
        # await Timer(8, "ns")

    l2 = await getcntr()

    
    cocotb.log.info(f"l1 = {l1} and l2= {l2}")

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
    tqv = TinyQV(dut, PERIPHERAL_NUM)
    # Display banners
    cocotb.log.info("")
    cocotb.log.info("###")
    cocotb.log.info("### PTC IP Core Verification ###")
    cocotb.log.info("###")
    cocotb.log.info("I. Testing correct operation of RPTC_CTRL control bits")
    cocotb.log.info("")

    await test_eclk()

    cocotb.log.info("###")
    cocotb.log.info("")

    # End of simulation
    raise TestSuccess("PTC IP Core Verification completed")
