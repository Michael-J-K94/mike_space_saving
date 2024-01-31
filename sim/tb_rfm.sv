`timescale 1ps/1ps

module rfm_tb();


localparam NUM_ENTRY = 512; 
localparam NUM_ENTRY_BITS = 9; // log2 (NUM_ENTRY)
localparam RFM_TH = 649; 
localparam ADDR_SIZE = 18; 
localparam CNT_SIZE = 32; 

reg clk;
reg rstn;
reg act_cmd;
reg [ADDR_SIZE-1:0] act_addr;
reg rfm_cmd;

wire nrr_cmd;
wire [ADDR_SIZE-1:0] nrr_addr;

integer f;
integer trace_file;
integer iter;
genvar i;
genvar j;
integer act_count=0;




// For Test
wire [ADDR_SIZE-1:0] addr_table [0:NUM_ENTRY-1];
wire [CNT_SIZE-1:0] cnt_table [0:NUM_ENTRY-1];
//wire [NUM_ENTRY-1:0] cnt_matches;




// Clock
initial begin
  clk = 1'b0;
  forever #5 clk = ~clk;
end


// Activation
initial begin
  trace_file = $fopen("trace.txt", "r");
  act_cmd = 1'b0;
  act_addr = {ADDR_SIZE{1'b0}};
  #20
  forever begin
    repeat (59) @(posedge clk);
    act_cmd <= 1'b1;
    act_count = act_count +1;
    $fscanf(trace_file, "%d\n", act_addr);
    repeat (1) @(posedge clk);
    act_cmd <= 1'b0;

    // RFM
    if((act_count % RFM_TH) == 0)
    repeat (60) @(posedge clk);
    rfm_cmd <= 1'b1;
    repeat (1) @(posedge clk);
    rfm_cmd <= 1'b0;
    repeat (200) @(posedge clk);

    if ($feof(trace_file)) begin
      repeat (300) @(posedge clk);
      $finish;
    end
  end
end



// Main Function
initial begin
  f = $fopen("result.txt","w");

  rstn = 1'b1;
  #10
  rstn = 1'b0;
  #10
  rstn = 1'b1;
  repeat (10000000) @(posedge clk);
  $fclose(f);
  $finish;
end

// Display
initial begin
  #20
  forever begin
    wait(act_cmd == 1'b0);
    wait(act_cmd == 1'b1);
    repeat (10) @(posedge clk);
    $fwrite(f,"////////  ACT %d ////////\n", act_count);
    $fwrite(f,"ACT Address : %d\n", act_addr);
    for(iter = 0; iter < NUM_ENTRY; iter = iter+1) begin
      $fwrite(f,"%d: %d, %d\n", iter, addr_table[iter], cnt_table [iter]);
    end
    $fwrite(f,"\n\n");
  end
end


generate
  for (i = 0; i < (NUM_ENTRY >> 2); i = i + 1) begin
    for (j = 0; j < ADDR_SIZE; j = j + 1) begin
      assign addr_table[i + 0 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.addr_cam_0.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
    for (j = 0; j < ADDR_SIZE; j = j + 1) begin
      assign addr_table[i + 1 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.addr_cam_1.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
    for (j = 0; j < ADDR_SIZE; j = j + 1) begin
      assign addr_table[i + 2 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.addr_cam_2.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
    for (j = 0; j < ADDR_SIZE; j = j + 1) begin
      assign addr_table[i + 3 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.addr_cam_3.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
    for (j = 0; j < CNT_SIZE; j = j + 1) begin
      assign cnt_table[i + 0 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.cnt_cam_0.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
    for (j = 0; j < CNT_SIZE; j = j + 1) begin
      assign cnt_table[i + 1 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.cnt_cam_1.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
    for (j = 0; j < CNT_SIZE; j = j + 1) begin
      assign cnt_table[i + 2 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.cnt_cam_2.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
    for (j = 0; j < CNT_SIZE; j = j + 1) begin
      assign cnt_table[i + 3 * (NUM_ENTRY >> 2)][j] = u_rfm_unit_bank.cnt_cam_3.larray_inst[i].latch_array_.latch_inst[j].latch_.q;
    end
  end
endgenerate



rfm_unit_bank
#(
  .NUM_ENTRY      (NUM_ENTRY),
  .NUM_ENTRY_BITS (NUM_ENTRY_BITS),
  .RFM_TH         (RFM_TH),
  .ADDR_SIZE      (ADDR_SIZE),
  .CNT_SIZE       (CNT_SIZE)
)
u_rfm_unit_bank
(
  .clk(clk),
  .rstn(rstn),
  .act_cmd(act_cmd),
  .act_addr(act_addr),
  .rfm_cmd(rfm_cmd),

  .nrr_cmd(nrr_cmd),
  .nrr_addr(nrr_addr)
);


`ifdef WAVE 
  initial begin
    $shm_open("WAVE");
    $shm_probe("ASM");
  end  
`endif


endmodule
