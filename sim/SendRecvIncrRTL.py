#=========================================================================
# SendRecvIncrRTL
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.ifcs.SendRecvIfc import RecvIfcRTL, SendIfcRTL
from pymtl3.passes.backends.verilog import \
    VerilogPlaceholderConfigs, TranslationConfigs

class SendRecvIncrVRTL( Component, Placeholder ):
  def construct( s ):

    s.recv = RecvIfcRTL( Bits32 )
    s.send = SendIfcRTL( Bits32 )

    from os import path
    s.config_placeholder = VerilogPlaceholderConfigs(
      src_file = path.dirname(__file__) + '/SendRecvIncrVRTL.v',
      port_map = {
        'recv.rdy' : 'recv_rdy',
        'recv.en'  : 'recv_en',
        'recv.msg' : 'recv_msg',
        'send.rdy' : 'send_rdy',
        'send.en'  : 'send_en',
        'send.msg' : 'send_msg',
      }
    )
    s.config_verilog_translate = TranslationConfigs(
      translate = False,
      explicit_module_name = 'SendRecvIncrRTL',
    )

SendRecvIncrRTL = SendRecvIncrVRTL

