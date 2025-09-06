<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

The peripheral index is the number TinyQV will use to select your peripheral.  You will pick a free
slot when raising the pull request against the main TinyQV repository, and can fill this in then.  You
also need to set this value as the PERIPHERAL_NUM in your test script.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

# PWM/Timer/Counter

Author: Eraz Ahmed

Peripheral index: nn

## What it does

This is an IP to do it all, starting from counting, generating a PWM signal, and measuring the time between two instances. Why is it different? Because you can supply your own clock to do the counting. The design is fully parameterized to make sure we can control most of it until it's hardened. There are multiple type of registers that controls the behavior of this IP. There is also an interrupt behavior implemented in it that can output an interrupt signal as per the registered count being overtaken.

## Register map

Document the registers that are used to interact with your peripheral

| Address | Name           | Access | Width | Description                                                            |
|---------|----------------|--------|-------|------------------------------------------------------------------------|
| 0x00    | RPTC_CNTR  | R/W    |  32   | This Register holds the count value that the counter provides to the <br> user |
| 0x04    | RPTC_HRC   | R/W    |  32   | This Register holds the `High Reference Capture Register` that captures <br> counter register data when this externally controlled signal is high <br> and it also holds Reference values for the Counter Register to compare |
| 0x08    | RPTC_LRC   | R/W    |  32   | This Register holds the `Low Reference Capture Register` that captures <br> counter register data when this externally controlled signal is low <br> and it also holds Reference values for the Counter Register to compare |
| 0x0C    | RPTC_CTRL  | R/W    |  9   | This Register holds the control signals to control the functionality <br> of the IP. For example, enabling external clock or capture behavior <br> or both! A better definition of this is discussed next table. |

Control bits in the `RPTC_CTRL` register control the operation of the PTC core.

| Bit     | Access         | Description                                                            |
|---------|----------------|------------------------------------------------------------------------|
| 0       | R/W            | EN   <br> This Register bit, When set, RPTC_CNTR can be incremented.   |
| 1       | R/W            | ECLK <br> This Register bit, When set, ptc_ecgt signal is used to <br> increment RPTC_CNTR. When cleared, the system <br> clock is used instead. |
| 2       | R/W            | NEC  <br> This Register bit, When set, ptc_ecgt signal is used to <br> increment RPTC_CNTR. When cleared, the system <br> clock is used instead. |


## How to test

Explain how to use your project

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
