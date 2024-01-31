module latch (s, r, en, q);

input s, r, en;
output q;
wire q_;

wire tmp_s, tmp_r;

nand (tmp_s, s, en);
nand (tmp_r, r, en);

nand (q, tmp_s, q_);
nand (q_, tmp_r, q);

endmodule


module latch_array (data_in, write_en, search_en, data_out, match);

parameter WORD_SIZE = 16;

input [WORD_SIZE-1:0] data_in;
input write_en, search_en;

output [WORD_SIZE-1:0] data_out;
output match;

wire s_array [0:WORD_SIZE-1];
wire r_array [0:WORD_SIZE-1];

genvar i;
generate for (i = 0; i < WORD_SIZE; i = i+1) begin: latch_inst
          assign s_array[i] = data_in[i];
            assign r_array[i] = ~data_in[i];

    latch latch_(.s(s_array[i]), .r(r_array[i]), .en(write_en), .q(data_out[i]));
  end
endgenerate

assign match = search_en ? (data_out == data_in) : match;

endmodule


module encoder (match_array, match, match_addr);

parameter ROW_NUM = 68;
parameter ENTRY_WIDTH = 7;

input [ROW_NUM-1:0] match_array;

output reg [ENTRY_WIDTH-1:0] match_addr;
output reg match;

integer i;
always @(*) begin
  match = 0;
  for (i = ROW_NUM - 1; i >= 0; i = i-1) begin
    if (match_array[i] == 1'b1) begin
      match_addr = i;
      match = 1;
    end
  end
end


endmodule


