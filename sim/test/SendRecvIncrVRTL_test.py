#=========================================================================
# SendRecvIncrVRTL_test
#=========================================================================

import pytest

from pymtl3 import *
from pymtl3.stdlib.test import run_test_vector_sim
from pymtl3.stdlib.test import run_sim, config_model
from pymtl3.stdlib.test import mk_test_case_table
from pymtl3.stdlib.test.test_srcs  import TestSrcRTL
from pymtl3.stdlib.test.test_sinks import TestSinkRTL

from SendRecvIncrRTL import SendRecvIncrRTL

#-------------------------------------------------------------------------
# SendRecvIncrWrapper
#-------------------------------------------------------------------------
# Currently run_test_vector_sim does not support interfaces, so we can
# write a little wrapper to turn the interfaces into regular ports so we
# can use run_test_vector_sim

class SendRecvIncrWrapper( Component ):
  def construct( s ):

    s.recv_rdy = OutPort( Bits1 )
    s.recv_en  = InPort ( Bits1 )
    s.recv_msg = InPort ( Bits32 )

    s.send_rdy = InPort ( Bits1 )
    s.send_en  = OutPort( Bits1 )
    s.send_msg = OutPort( Bits32 )

    s.m = SendRecvIncrRTL()

    s.m.recv.rdy //= s.recv_rdy
    s.m.recv.en  //= s.recv_en
    s.m.recv.msg //= s.recv_msg

    s.m.send.rdy //= s.send_rdy
    s.m.send.en  //= s.send_en
    s.m.send.msg //= s.send_msg

  def line_trace( s ):
    return f"{s.recv_rdy}{s.recv_en} {s.recv_msg} > {s.send_rdy}{s.send_en} {s.send_msg}"

#-------------------------------------------------------------------------
# test_directed_basic
#-------------------------------------------------------------------------
# This illustrates how to test the DUT using the most basic test vector.
# We need to explicitly set the inputs and check the outputs every cycle.
# Here we send in a single message and then receive it the next cycle.

def test_directed_basic( dump_vcd, test_verilog ):
  run_test_vector_sim( SendRecvIncrWrapper(), [
    ( "recv_rdy* recv_en recv_msg         send_rdy send_en* send_msg*"      ),
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(1),  b32(0x00000001), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(1),   b1(1),   b32(0x00000002) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
  ], dump_vcd, test_verilog )

#-------------------------------------------------------------------------
# test_directed_stream
#-------------------------------------------------------------------------
# Now we send in three consecutive messages.

def test_directed_stream( dump_vcd, test_verilog ):
  run_test_vector_sim( SendRecvIncrWrapper(), [
    ( "recv_rdy* recv_en recv_msg         send_rdy send_en* send_msg*"      ),
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(1),  b32(0x00000001), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(1),  b32(0x00000002), b1(1),   b1(1),   b32(0x00000002) ],
    [  b1(1),    b1(1),  b32(0x00000003), b1(1),   b1(1),   b32(0x00000003) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(1),   b1(1),   b32(0x00000004) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
  ], dump_vcd, test_verilog )

#-------------------------------------------------------------------------
# test_directed_input_delay
#-------------------------------------------------------------------------
# Now we delay sending the three consecutive messages for a few cycles
# and send a new message every other cycle.

def test_directed_input_delay( dump_vcd, test_verilog ):
  run_test_vector_sim( SendRecvIncrWrapper(), [
    ( "recv_rdy* recv_en recv_msg         send_rdy send_en* send_msg*"      ),
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(1),  b32(0x00000001), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(1),   b1(1),   b32(0x00000002) ],
    [  b1(1),    b1(1),  b32(0x00000002), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(1),   b1(1),   b32(0x00000003) ],
    [  b1(1),    b1(1),  b32(0x00000003), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(1),   b1(1),   b32(0x00000004) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
  ], dump_vcd, test_verilog )

#-------------------------------------------------------------------------
# test_directed_output_delay
#-------------------------------------------------------------------------
# Now we delay receiving the three consecutive messages for a few cycles
# to test back pressure. This also fills up the input queue.

def test_directed_output_delay( dump_vcd, test_verilog ):
  run_test_vector_sim( SendRecvIncrWrapper(), [
    ( "recv_rdy* recv_en recv_msg         send_rdy send_en* send_msg*"      ),
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(1),  b32(0x00000001), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(1),    b1(1),  b32(0x00000002), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(0),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(0),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(0),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
    [  b1(0),    b1(0),  b32(0x00000000), b1(1),   b1(1),   b32(0x00000002) ],
    [  b1(1),    b1(1),  b32(0x00000003), b1(1),   b1(1),   b32(0x00000003) ],
    [  b1(1),    b1(1),  b32(0x00000004), b1(1),   b1(1),   b32(0x00000004) ],
    [  b1(1),    b1(1),  b32(0x00000005), b1(1),   b1(1),   b32(0x00000005) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(1),   b1(1),   b32(0x00000006) ],
    [  b1(1),    b1(0),  b32(0x00000000), b1(0),   b1(0),   b32(0x00000000) ],
  ], dump_vcd, test_verilog )

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------
# This test harness uses source sink testing so we no longer have to
# figure out exactly what should happen on every cycle.

class TestHarness( Component ):

  def construct( s, src_msgs, sink_msgs ):

    s.src  = TestSrcRTL ( Bits32, src_msgs  )
    s.dut  = SendRecvIncrRTL()
    s.sink = TestSinkRTL( Bits32, sink_msgs )

    s.src.send //= s.dut.recv
    s.dut.send //= s.sink.recv

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return f"{s.src.line_trace()} ({s.dut.line_trace()}) {s.sink.line_trace()}"

#-------------------------------------------------------------------------
# test_srcsink_basic
#-------------------------------------------------------------------------
# Most basic possible srcsink test ... we just send in a single message.

def test_srcsink_basic( dump_vcd, test_verilog ):
  th = TestHarness( [ b32(1) ], [ b32(2) ] )
  config_model( th, dump_vcd, test_verilog, ['dut'] )
  run_sim( th )

#-------------------------------------------------------------------------
# msgs
#-------------------------------------------------------------------------
# We might as well define some list of messages so we can reuse them.

stream_in_msgs  = [ b32(1), b32(2), b32(3), b32(4), b32(5) ]
stream_out_msgs = [ b32(2), b32(3), b32(4), b32(5), b36(6) ]

#-------------------------------------------------------------------------
# test_srcsink_stream
#-------------------------------------------------------------------------
# Now we try with a stream of five messages.

def test_srcsink_stream( dump_vcd, test_verilog ):
  th = TestHarness( stream_in_msgs, stream_out_msgs )
  config_model( th, dump_vcd, test_verilog, ['dut'] )
  run_sim( th )

#-------------------------------------------------------------------------
# test_srcsink_stream_input_delay
#-------------------------------------------------------------------------
# Now we try with a stream of five messages and input delays.

def test_srcsink_stream_input_delay( dump_vcd, test_verilog ):
  th = TestHarness( stream_in_msgs, stream_out_msgs )
  th.set_param("top.src.construct", initial_delay=5, interval_delay=1 )
  config_model( th, dump_vcd, test_verilog, ['dut'] )
  run_sim( th )

#-------------------------------------------------------------------------
# test_srcsink_stream_output_delay
#-------------------------------------------------------------------------
# Now we try with a stream of five messages and output delays.

def test_srcsink_stream_output_delay( dump_vcd, test_verilog ):
  th = TestHarness( stream_in_msgs, stream_out_msgs )
  th.set_param("top.sink.construct", initial_delay=5, interval_delay=1 )
  config_model( th, dump_vcd, test_verilog, ['dut'] )
  run_sim( th )

#-------------------------------------------------------------------------
# test_srcsink
#-------------------------------------------------------------------------
# Here we can use a single parameterized pytest function to basically do
# the same as the above srcsink tests.

basic_msgs  = [ b32(1), b32(2) ]
stream_msgs = [
# input msg  output msg
  b32(1),    b32(2),
  b32(2),    b32(3),
  b32(3),    b32(4),
  b32(4),    b32(5),
  b32(5),    b32(6),
]

test_case_table = mk_test_case_table([
  (               "msgs        src_delay  sink_delay"),
  [ "basic_0x0",  basic_msgs,  0,         0,         ],
  [ "stream_0x0", stream_msgs, 0,         0,         ],
  [ "stream_5x0", stream_msgs, 5,         0,         ],
  [ "stream_0x5", stream_msgs, 5,         5,         ],
  [ "stream_0x5", stream_msgs, 2,         7,         ],
])

@pytest.mark.parametrize( **test_case_table )
def test_srcsink( test_params, dump_vcd, test_verilog ):
  th = TestHarness( test_params.msgs[::2], test_params.msgs[1::2] )

  th.set_param("top.src.construct",
    initial_delay=test_params.src_delay,
    interval_delay=test_params.src_delay )

  th.set_param("top.sink.construct",
    initial_delay=test_params.sink_delay,
    interval_delay=test_params.sink_delay )

  config_model( th, dump_vcd, test_verilog, ['dut'] )
  run_sim( th )

