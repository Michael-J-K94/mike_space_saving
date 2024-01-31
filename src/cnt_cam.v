module cnt_cam (data_in, addr_in, read_en, write_en, search_en, reset, data_out, addr_out, match, clk, rstn, max_en, max);

parameter WORD_SIZE = 13;
parameter ENTRY_WIDTH = 7; // [log2(ROW_NUM)]
parameter ROW_NUM = 128;

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




/*  Find Max   */

input clk;
input rstn;
input max_en;
output [WORD_SIZE-1:0] max;

reg [1:0] mode;

wire [WORD_SIZE-1:0] temp_max;
wire [WORD_SIZE-1:0] temp_max_0;
wire [WORD_SIZE-1:0] temp_max_1;
reg [WORD_SIZE-1:0] temp_max_0_0;
reg [WORD_SIZE-1:0] temp_max_0_1;
reg [WORD_SIZE-1:0] temp_max_1_0;
reg [WORD_SIZE-1:0] temp_max_1_1;

wire [WORD_SIZE-1:0] max_2 [1:0];
wire [WORD_SIZE-1:0] max_4 [3:0];
wire [WORD_SIZE-1:0] max_8 [7:0];
wire [WORD_SIZE-1:0] max_16 [15:0];
wire [WORD_SIZE-1:0] max_32 [31:0];
wire [WORD_SIZE-1:0] max_64 [63:0];
wire [WORD_SIZE-1:0] max_128 [127:0];
//wire [WORD_SIZE-1:0] max_256 [255:0];


assign max = (temp_max_0 > temp_max_1) ? temp_max_0 : temp_max_1;
assign temp_max_0 = (temp_max_0_0 > temp_max_0_1) ? temp_max_0_0 : temp_max_0_1;
assign temp_max_1 = (temp_max_1_0 > temp_max_1_1) ? temp_max_1_0 : temp_max_1_1;


always @(posedge clk or negedge rstn) begin
  if (~rstn) begin
    mode <= 2'b00;
  end
  else if (max_en) begin
    mode <= mode + 2'b01;
  end
  else begin
    mode <= 2'b00;
  end
end

always @(posedge clk or negedge rstn) begin
  if (~rstn) begin
    temp_max_0_0 <= {WORD_SIZE{1'b0}};
  end
  else if (max_en && mode == 2'b00) begin
    temp_max_0_0 <= temp_max;
  end
  else begin
    temp_max_0_0 <= temp_max_0_0;
  end
end

always @(posedge clk or negedge rstn) begin
  if (~rstn) begin
    temp_max_0_1 <= {WORD_SIZE{1'b0}};
  end
  else if (max_en && mode == 2'b01) begin
    temp_max_0_1 <= temp_max;
  end
  else begin
    temp_max_0_1 <= temp_max_0_1;
  end
end

always @(posedge clk or negedge rstn) begin
  if (~rstn) begin
    temp_max_1_0 <= {WORD_SIZE{1'b0}};
  end
  else if (max_en && mode == 2'b10) begin
    temp_max_1_0 <= temp_max;
  end
  else begin
    temp_max_1_0 <= temp_max_1_0;
  end
end

always @(posedge clk or negedge rstn) begin
  if (~rstn) begin
    temp_max_1_1 <= {WORD_SIZE{1'b0}};
  end
  else if (max_en && mode == 2'b11) begin
    temp_max_1_1 <= temp_max;
  end
  else begin
    temp_max_1_1 <= temp_max_1_1;
  end
end


assign temp_max = (max_2[0] > max_2[1]) ? max_2[0] : max_2[1];

generate for (i = 0; i < 2; i = i+1) begin
  assign max_2[i] = (max_4[2*i] > max_4[2*i+1]) ? max_4[2*i] : max_4[2*i+1];
end
endgenerate

generate for (i = 0; i < 4; i = i+1) begin
  assign max_4[i] = (max_8[2*i] > max_8[2*i+1]) ? max_8[2*i] : max_8[2*i+1];
end
endgenerate

generate for (i = 0; i < 8; i = i+1) begin
  assign max_8[i] = (max_16[2*i] > max_16[2*i+1]) ? max_16[2*i] : max_16[2*i+1];
end
endgenerate

generate for (i = 0; i < 16; i = i+1) begin
  assign max_16[i] = (max_32[2*i] > max_32[2*i+1]) ? max_32[2*i] : max_32[2*i+1];
end
endgenerate


generate for (i = 0; i < 32; i = i+1) begin
  assign max_32[i] = (max_64[2*i] > max_64[2*i+1]) ? max_64[2*i] : max_64[2*i+1];
end
endgenerate


generate for (i = 0; i < 64; i = i+1) begin
  assign max_64[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate


endmodule

