//========================================================================
// SendRecvIncrVRTL
//========================================================================

`include "vc/queues.v"

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

  // Recv Queue

  logic        recvq_deq_en;
  logic        recvq_deq_rdy;
  logic [31:0] recvq_deq_ret;

  vc_Queue#(`VC_QUEUE_NORMAL,32,2) recvq
  (
    .clk     (clk),
    .reset   (reset),
    .num_free_entries(),
    .enq_rdy (recv_rdy),
    .enq_en  (recv_en),
    .enq_msg (recv_msg),
    .deq_rdy (recvq_deq_rdy),
    .deq_en  (recvq_deq_en),
    .deq_ret (recvq_deq_ret)
  );

  // Combinational logic to do increment

  always_comb begin

    // Default values

    recvq_deq_en = 0;
    send_en      = 0;
    send_msg     = 0;

    // Only fire if recvq_deq _and_ send interfaces are ready

    if ( send_rdy && recvq_deq_rdy ) begin
      recvq_deq_en = 1;
      send_en      = 1;
      send_msg     = recvq_deq_ret + 1;
    end

  end

endmodule

