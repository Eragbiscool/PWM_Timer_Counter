
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer


# --------------------------
# Clock & Reset Generators
# --------------------------

async def generate_clock(dut, period_ns=10):
    """Generate clock on dut.clk"""
    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())


async def reset_dut(dut, cycles=2):
    """Apply reset to DUT"""
    dut.rst_n.value = 0
    for _ in range(cycles):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)


# --------------------------
# Helpers replacing SV tasks
# --------------------------

def set_ptc_capt(dut, bitr: int):
    """Set ptc_capt signal"""
    dut.ptc_capt.value = bitr


# --------------------------
# Example top-level test
# --------------------------

@cocotb.test()
async def tb_top_test(dut):
    """Top-level cocotb test replacing tb_top.sv"""

    # Start clock and reset
    await generate_clock(dut)
    await reset_dut(dut)

    # Example: drive ptc_capt like SV task
    set_ptc_capt(dut, 0)
    await Timer(50, "ns")
    set_ptc_capt(dut, 1)
    await Timer(50, "ns")

    # Show DUT outputs
    cocotb.log.info(f"uo_out = {dut.uo_out.value}")
    cocotb.log.info(f"data_out = {dut.data_out.value}")