module addr_cam (data_in, addr_in, read_en, write_en, search_en, reset, data_out, addr_out, match);

parameter WORD_SIZE = 16;
parameter ENTRY_WIDTH = 7; // [log2(ROW_NUM)]
parameter ROW_NUM = 68;

input [WORD_SIZE-1:0] data_in;
input [ENTRY_WIDTH-1:0] addr_in;
input read_en, write_en, search_en;
input reset;

output [WORD_SIZE-1:0] data_out;
output [ENTRY_WIDTH-1:0] addr_out;
output match;

wire we_array [ROW_NUM-1:0];
wire [WORD_SIZE-1:0] data_array [0:ROW_NUM-1];
wire [ROW_NUM-1:0] match_array;

wire [WORD_SIZE-1:0] data_in_tmp;
assign data_in_tmp = reset ? 0 : data_in;

genvar i;
generate for (i = 0; i < ROW_NUM; i = i+1) begin: larray_inst
          assign we_array[i] = reset? 1 : write_en & (addr_in == i);
    latch_array #(.WORD_SIZE(WORD_SIZE)) latch_array_(.data_in(data_in_tmp), .write_en(we_array[i]), .search_en(search_en), .data_out(data_array[i]), .match(match_array[i]));
  end
endgenerate

assign data_out = read_en ? data_array[addr_in] : data_out;

encoder #(.ROW_NUM(ROW_NUM), .ENTRY_WIDTH(ENTRY_WIDTH)) encoder_ (match_array, match, addr_out);

endmodule

