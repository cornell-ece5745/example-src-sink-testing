
# Verilog Source/Sink Testing

This repo includes an example Verilog module which uses a send/recv
interface like this:

```
module SendRecvIncrVRTL
(
  input  logic        clk,
  input  logic        reset,

  output logic        recv_rdy,
  input  logic        recv_en,
  input  logic [31:0] recv_msg,

  input  logic        send_rdy,
  output logic        send_en,
  output logic [31:0] send_msg
);
```

The module has a receive queue and simply increments the values in the
queue and sends them out the send interface. We are using latency
insensitive en/rdy interfaces. The include test file in
`test/SendRecvIncrRTL_test.py` illustrates how to use both test vectors
and source/sink testing to test this Verilog module.

Here is how to run the exasmple:

```
  % git clone git@github.com:cornell-ece5745/example-src-sink-testing
  % mkdir -p example-src-sink-testing/sim/build
  % cd example-src-sink-testing/sim/build
  % pytest ../test/SendRecvIncrVRTL_test.py -sv
```

