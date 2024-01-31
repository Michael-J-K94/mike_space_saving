
import math

params = [] # N_entry, RFM_th, Counter-bits
#params.append([19, 8, 5])
#params.append([22, 32, 7])
#params.append([24, 128, 9])
#params.append([38, 8, 6])
#params.append([46, 32, 8])
#params.append([50, 128, 10])
#params.append([78, 8, 6])
#params.append([93, 32, 8])
#params.append([107, 128, 10])
#params.append([157, 8, 6])
#params.append([194, 32, 8])
#params.append([254, 128, 10])
#params.append([320, 8, 6])
#params.append([422, 32, 8])
#params.append([981, 128, 10])
#params.append([698, 8, 6])
#params.append([1122, 32, 8])
#params.append([1024, 32, 8])

params.append([369, 16, 7])
params.append([522, 64, 9])
params.append([984, 128, 10])
params.append([177, 16, 7])
params.append([214, 64, 9])
params.append([254, 128, 10])
params.append([420, 256, 11])
params.append([87, 16, 7])
params.append([99, 64, 9])
params.append([107, 128, 10])
params.append([123, 256, 11])
params.append([53, 256, 11])
params.append([25, 256, 10])
params.append([415, 16, 7])
params.append([583, 64, 9])
params.append([1186, 128, 10])
params.append([187, 16, 7])
params.append([223, 64, 9])
params.append([264, 128, 10])
params.append([439, 256, 11])
params.append([89, 16, 7])
params.append([101, 64, 9])
params.append([108, 128, 10])
params.append([124, 256, 11])
params.append([53, 256, 11])
params.append([25, 256, 10])


for param in params:

  r_file = open('cnt_cam.v', 'r') 
  lines = r_file.readlines() 

  w_file = open('cnt_cam/cnt_cam_{}_{}_{}.v'.format(int(param[0]), int(param[1]), int(param[2])), 'w') 
 

  nRow = int(param[0])
   
  for line in lines:
    if line == "module cnt_cam (data_in, addr_in, read_en, write_en, search_en, reset, data_out, addr_out, match, clk, rstn, max_en, max);\n":
      line = "module cnt_cam_{}_{}_{} (data_in, addr_in, read_en, write_en, search_en, reset, data_out, addr_out, match, clk, rstn, max_en, max);\n".format(int(param[0]), int(param[1]), int(param[2]))
    if line == "parameter WORD_SIZE = 13;\n":
      line = "parameter WORD_SIZE = {};\n".format(int(param[2]))
    if line == "parameter ROW_NUM = 128;\n":
      line = "parameter ROW_NUM = {};\n".format(nRow)
    if line == "parameter ENTRY_WIDTH = 7; // [log2(ROW_NUM)]\n":
      line = "parameter ENTRY_WIDTH = {}; // [log2(ROW_NUM)]\n".format(math.ceil(math.log2(nRow)))

    w_file.write(line)
    
    if line == "reg [WORD_SIZE-1:0] temp_max_1_1;\n":
      break

  lines = '\n'

  if 16 < nRow:
    lines += 'wire [WORD_SIZE-1:0] max_2 [1:0];\n'
  if 32 < nRow:
    lines += 'wire [WORD_SIZE-1:0] max_4 [3:0];\n'
  if 64 < nRow:
    lines += 'wire [WORD_SIZE-1:0] max_8 [7:0];\n'
  if 128 < nRow:
    lines += 'wire [WORD_SIZE-1:0] max_16 [15:0];\n'
  if 256 < nRow:
    lines += 'wire [WORD_SIZE-1:0] max_32 [31:0];\n'
  if 512 < nRow:
    lines += 'wire [WORD_SIZE-1:0] max_64 [63:0];\n'
  if 1024 < nRow:
    lines += 'wire [WORD_SIZE-1:0] max_128 [127:0];\n'


  lines += '''
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

'''


  if 32 < nRow:
    lines += '''
generate for (i = 0; i < 2; i = i+1) begin
  assign max_2[i] = (max_4[2*i] > max_4[2*i+1]) ? max_4[2*i] : max_4[2*i+1];
end
endgenerate
'''
  if 64 < nRow:
    lines += '''
generate for (i = 0; i < 4; i = i+1) begin
  assign max_4[i] = (max_8[2*i] > max_8[2*i+1]) ? max_8[2*i] : max_8[2*i+1];
end
endgenerate
'''
  if 128 < nRow:
    lines += '''
generate for (i = 0; i < 8; i = i+1) begin
  assign max_8[i] = (max_16[2*i] > max_16[2*i+1]) ? max_16[2*i] : max_16[2*i+1];
end
endgenerate
'''
  if 256 < nRow:
    lines += '''
generate for (i = 0; i < 16; i = i+1) begin
  assign max_16[i] = (max_32[2*i] > max_32[2*i+1]) ? max_32[2*i] : max_32[2*i+1];
end
endgenerate
'''
  if 512 < nRow:
    lines += '''
generate for (i = 0; i < 32; i = i+1) begin
  assign max_32[i] = (max_64[2*i] > max_64[2*i+1]) ? max_64[2*i] : max_64[2*i+1];
end
endgenerate
'''
  if 1024 < nRow:
    lines += '''
generate for (i = 0; i < 64; i = i+1) begin
  assign max_64[i] = (max_128[2*i] > max_128[2*i+1]) ? max_128[2*i] : max_128[2*i+1];
end
endgenerate
'''

  lines += '\n'

  if 16 < nRow and nRow <= 32:
    lines += '''
generate for (i = 0; i < ({} >> 4); i = i+1) begin
  assign max_2[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate

generate for (i = ({} >> 4); i < 2; i = i+1) begin
  assign max_2[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate
'''.format(nRow, nRow)
  elif 32 < nRow and nRow <= 64:
    lines += '''
generate for (i = 0; i < ({} >> 4); i = i+1) begin
  assign max_4[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate

generate for (i = ({} >> 4); i < 4; i = i+1) begin
  assign max_4[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate
'''.format(nRow, nRow)
  elif 64 < nRow and nRow <= 128:
    lines += '''
generate for (i = 0; i < ({} >> 4); i = i+1) begin
  assign max_8[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate

generate for (i = ({} >> 4); i < 8; i = i+1) begin
  assign max_8[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate
'''.format(nRow, nRow)
  elif 128 < nRow and nRow <= 256:
    lines += '''
generate for (i = 0; i < ({} >> 4); i = i+1) begin
  assign max_16[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate

generate for (i = ({} >> 4); i < 16; i = i+1) begin
  assign max_16[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate
'''.format(nRow, nRow)
  elif 256 < nRow and nRow <= 512:
    lines += '''
generate for (i = 0; i < ({} >> 4); i = i+1) begin
  assign max_32[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate

generate for (i = ({} >> 4); i < 32; i = i+1) begin
  assign max_32[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate
'''.format(nRow, nRow)
  elif 512 < nRow and nRow <= 1024:
    lines += '''
generate for (i = 0; i < ({} >> 4); i = i+1) begin
  assign max_64[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate

generate for (i = ({} >> 4); i < 32; i = i+1) begin
  assign max_64[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate
'''.format(nRow, nRow)
  elif 1024 < nRow and nRow <= 2048:
    lines += '''
generate for (i = 0; i < ({} >> 4); i = i+1) begin
  assign max_128[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate

generate for (i = ({} >> 4); i < 128; i = i+1) begin
  assign max_128[i] = mode[1] ? (mode[0] ? data_array[4*i+3] : data_array[4*i+2]) : (mode[0] ? data_array[4*i+1] : data_array[4*i]);
end
endgenerate
'''.format(nRow, nRow)

  lines +='\nendmodule'

  w_file.write(lines)

  r_file.close()
  w_file.close()
